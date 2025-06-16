from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import json
from pathlib import Path
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

# Pydantic models for structured outputs
class IngredientCombination(BaseModel):
    """A valid ingredient combination for a dish"""
    name: str = Field(description="Name of the combination")
    ingredients: List[str] = Field(description="List of ingredients")
    dish_type: str = Field(description="Type of dish (MAIN_COURSE, STARTER, etc.)")
    description: str = Field(description="Description of the combination")

class CuisineCombinations(BaseModel):
    """All combinations for a specific cuisine"""
    cuisine: str = Field(description="Cuisine type")
    compatible_combinations: Dict[str, List[IngredientCombination]] = Field(
        description="Compatible combinations grouped by dish type"
    )
    incompatible_combinations: List[Dict[str, str]] = Field(
        description="Incompatible ingredient combinations with reasons"
    )
    all_ingredients: List[str] = Field(description="All available ingredients for this cuisine")

class ValidationResult(BaseModel):
    """Result of ingredient validation"""
    is_valid: bool = Field(description="Whether the ingredients are valid")
    can_generate_recipe: bool = Field(description="Whether we can generate a recipe")
    validation_message: str = Field(description="Clear message to user")
    suggested_dish_types: List[str] = Field(description="Suggested dish types")
    missing_ingredients: List[str] = Field(description="Ingredients that would complete the dish")
    closest_valid_combinations: List[Dict] = Field(description="Closest valid combinations")

class RecipeOutput(BaseModel):
    """Final recipe output structure"""
    title: str
    subtitle: str
    titleImages: List[str]
    urls: List[str]
    author: str = Field(default="AI Generated")
    source: str = Field(default="AI Recipe Generator")
    access: str = Field(default="isPublic")
    servings: str
    mealType: str
    dishType: str
    cuisine: str
    cookingMethod: List[str]
    ingredients: List[Dict]
    preparationDesc: str
    preparationLink: str
    preparationTimeMin: str
    cookingTimeMin: str
    otherInfo: str
    allergies: List[str]
    foodIntolerances: List[str]
    nutrients: List[Dict]

@CrewBase
class RecipeAppCrew():
    """Recipe Generation and Validation Crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    def __init__(self, user_inputs: Dict = None):
        """Initialize with user inputs for dynamic agent configuration"""
        self.user_inputs = user_inputs or {}
        self.knowledge_path = Path("knowledge")
        
    # Agent definitions with memory for key agents
    @agent
    def ingredient_suggester(self) -> Agent:
        return Agent(
            config=self.agents_config['ingredient_suggester'],
            tools=[SerperDevTool()],
            verbose=True,
            memory=True  # Remember successful combinations
        )
    
    @agent
    def ingredient_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['ingredient_validator'],
            tools=[SerperDevTool()],
            verbose=True,
            memory=True  # Remember validation patterns
        )
    
    @agent
    def recipe_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['recipe_generator'],
            tools=[SerperDevTool()],
            verbose=True,
            memory=True  # Remember successful recipes
        )
    
    @agent
    def nutritionist(self) -> Agent:
        return Agent(
            config=self.agents_config['nutritionist'],
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def cultural_validator(self) -> Agent:
        return Agent(
            config=self.agents_config['cultural_validator'],
            tools=[SerperDevTool()],
            verbose=True,
            memory=True  # Remember cultural rules
        )
    
    @agent
    def recipe_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['recipe_optimizer'],
            tools=[SerperDevTool()],
            verbose=True
        )
    
    @agent
    def quality_assurance(self) -> Agent:
        return Agent(
            config=self.agents_config['quality_assurance'],
            tools=[],
            verbose=True
        )
    
    @agent
    def recipe_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['recipe_formatter'],
            tools=[],
            verbose=True
        )
    
    # Task definitions with Pydantic models for structured output
    @task
    def suggest_ingredient_combinations(self) -> Task:
        return Task(
            config=self.tasks_config['suggest_ingredient_combinations'],
            agent=self.ingredient_suggester(),
            output_pydantic=CuisineCombinations
        )
    
    @task
    def validate_ingredients(self) -> Task:
        return Task(
            config=self.tasks_config['validate_ingredients'],
            agent=self.ingredient_validator(),
            output_pydantic=ValidationResult
        )
    
    @task
    def generate_recipe(self) -> Task:
        return Task(
            config=self.tasks_config['generate_recipe'],
            agent=self.recipe_generator(),
            context=[self.validate_ingredients()]
        )
    
    @task
    def calculate_nutrition(self) -> Task:
        return Task(
            config=self.tasks_config['calculate_nutrition'],
            agent=self.nutritionist(),
            context=[self.generate_recipe()]
        )
    
    @task
    def validate_authenticity(self) -> Task:
        return Task(
            config=self.tasks_config['validate_authenticity'],
            agent=self.cultural_validator(),
            context=[self.generate_recipe()]
        )
    
    @task
    def optimize_recipe(self) -> Task:
        return Task(
            config=self.tasks_config['optimize_recipe'],
            agent=self.recipe_optimizer(),
            context=[self.generate_recipe(), self.validate_authenticity()]
        )
    
    @task
    def quality_check(self) -> Task:
        return Task(
            config=self.tasks_config['quality_check'],
            agent=self.quality_assurance(),
            context=[
                self.generate_recipe(),
                self.calculate_nutrition(),
                self.optimize_recipe()
            ]
        )
    
    @task
    def format_final_recipe(self) -> Task:
        return Task(
            config=self.tasks_config['format_final_recipe'],
            agent=self.recipe_formatter(),
            context=[self.quality_check()],
            output_pydantic=RecipeOutput,
            output_file='output/final_recipe.json'
        )
    
    # Crew with memory for suggestions
    @crew
    def suggestion_crew(self) -> Crew:
        """Crew for suggesting ingredient combinations with memory"""
        return Crew(
            agents=[self.ingredient_suggester()],
            tasks=[self.suggest_ingredient_combinations()],
            process=Process.sequential,
            verbose=True,
            memory=True,
            # Long-term memory for storing successful combinations
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/recipe_combinations.db"
                )
            ),
            # Short-term memory for current session
            short_term_memory=ShortTermMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/suggestions/"
                )
            )
        )
    
    # Main crew with comprehensive memory
    @crew
    def recipe_generation_crew(self) -> Crew:
        """Main crew for validating and generating recipes with memory"""
        return Crew(
            agents=[
                self.ingredient_validator(),
                self.recipe_generator(),
                self.nutritionist(),
                self.cultural_validator(),
                self.recipe_optimizer(),
                self.quality_assurance(),
                self.recipe_formatter()
            ],
            tasks=[
                self.validate_ingredients(),
                self.generate_recipe(),
                self.calculate_nutrition(),
                self.validate_authenticity(),
                self.optimize_recipe(),
                self.quality_check(),
                self.format_final_recipe()
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,
            # Long-term memory for recipes and patterns
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/recipe_history.db"
                )
            ),
            # Short-term memory for current recipe generation
            short_term_memory=ShortTermMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="short_term",
                    path="./memory/generation/"
                )
            ),
            # Entity memory for ingredients and cuisines
            entity_memory=EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {
                            "model": 'text-embedding-3-small'
                        }
                    },
                    type="entities",
                    path="./memory/entities/"
                )
            )
        )
    
    def run_suggestion_flow(self, cuisine_type: str) -> CuisineCombinations:
        """Run the suggestion flow for a cuisine"""
        inputs = {
            "cuisine_type": cuisine_type
        }
        result = self.suggestion_crew().kickoff(inputs=inputs)
        return result
    
    def run_recipe_generation(self, inputs: Dict) -> RecipeOutput:
        """Run the full recipe generation flow"""
        # Add default values if not provided
        defaults = {
            "servings": "4",
            "meal_type": "DINNER",
            "cooking_methods": ["ROASTING", "GRILLING"],
            "dietary_restrictions": [],
            "allergies": []
        }
        
        # Merge with user inputs
        final_inputs = {**defaults, **inputs}
        
        result = self.recipe_generation_crew().kickoff(inputs=final_inputs)
        
        # Save the final recipe
        if result:
            self._save_recipe(result)
            
        return result
    
    def _save_recipe(self, recipe_data: RecipeOutput):
        """Save the generated recipe to the knowledge base"""
        recipes_path = self.knowledge_path / "recipes"
        recipes_path.mkdir(exist_ok=True)
        
        # Load existing recipes
        recipes_file = recipes_path / "generated_recipes.json"
        if recipes_file.exists():
            with open(recipes_file, 'r') as f:
                recipes = json.load(f)
        else:
            recipes = []
        
        # Add new recipe
        if isinstance(recipe_data, RecipeOutput):
            recipes.append(recipe_data.model_dump())
        else:
            recipes.append(recipe_data)
        
        # Save back
        with open(recipes_file, 'w') as f:
            json.dump(recipes, f, indent=2)