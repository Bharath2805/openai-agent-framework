from typing import Annotated, List, Any, Optional, Dict
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from research_tools import get_research_tools
from dotenv import load_dotenv
import uuid
import asyncio
from datetime import datetime

# Load environment variables from root .env file
load_dotenv("../.env", override=True)

class ResearchState(TypedDict):
    messages: Annotated[List[Any], add_messages]
    research_objective: str
    quality_criteria: str
    feedback_on_work: Optional[str]
    research_complete: bool
    user_input_needed: bool
    
class ResearchEvaluatorOutput(BaseModel):
    feedback: str = Field(description="Detailed feedback on the research quality and completeness")
    research_complete: bool = Field(description="Whether the research meets the specified criteria")
    user_input_needed: bool = Field(description="True if more input/clarification is needed from the user")

class ResearchAssistant:
    def __init__(self):
        self.researcher_llm_with_tools = None
        self.evaluator_llm_with_output = None
        self.tools = None
        self.graph = None
        self.assistant_id = str(uuid.uuid4())
        self.memory = MemorySaver()
        self.browser = None
        self.playwright = None
        
    async def setup(self):
        """Initialize the research assistant with all necessary tools and models"""
        self.tools, self.browser, self.playwright = await get_research_tools()
        
        # Researcher LLM - does the actual research work
        researcher_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        self.researcher_llm_with_tools = researcher_llm.bind_tools(self.tools)
        
        # Evaluator LLM - evaluates research quality
        evaluator_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.evaluator_llm_with_output = evaluator_llm.with_structured_output(ResearchEvaluatorOutput)
        
        await self.build_research_graph()
        
    def researcher_agent(self, state: ResearchState) -> Dict[str, Any]:
        """Main research agent that conducts research using available tools"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        system_message = f"""You are an expert Research Assistant specialized in conducting thorough, academic-quality research.

Your current research objective: {state['research_objective']}
Quality criteria to meet: {state['quality_criteria']}

Current date and time: {current_time}

RESEARCH METHODOLOGY:
1. Start with broad searches to understand the topic landscape
2. Use multiple sources: web search, Wikipedia, direct website analysis
3. Create comprehensive summaries with proper information
4. Save all findings to files in the research_outputs directory
5. Send WhatsApp notifications for major milestones

AVAILABLE TOOLS:
- research_web_search: For finding current information
- Wikipedia: For foundational knowledge and references
- Browser tools: For direct website analysis
- File tools: For saving research outputs, creating reports
- Python: For data analysis, creating charts
- WhatsApp notifications: For updating the user on progress

RESPONSE GUIDELINES:
- If you need clarification, ask specific questions
- When research is complete, provide a comprehensive summary
- Create structured outputs (reports, summaries, data files)
- Send notifications at key milestones
"""

        if state.get("feedback_on_work"):
            system_message += f"""
            
PREVIOUS FEEDBACK TO ADDRESS:
{state['feedback_on_work']}

Please address this feedback and improve your research accordingly."""

        # Update or add system message
        messages = state["messages"]
        found_system = False
        for message in messages:
            if isinstance(message, SystemMessage):
                message.content = system_message
                found_system = True
                break
                
        if not found_system:
            messages = [SystemMessage(content=system_message)] + messages
            
        # Get response from researcher
        response = self.researcher_llm_with_tools.invoke(messages)
        
        return {"messages": [response]}
    
    def research_router(self, state: ResearchState) -> str:
        """Route based on whether the researcher wants to use tools or is done"""
        last_message = state["messages"][-1]
        
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        else:
            return "evaluator"
            
    def format_research_conversation(self, messages: List[Any]) -> str:
        """Format the conversation for evaluation"""
        conversation = "Research Session History:\n\n"
        for message in messages:
            if isinstance(message, HumanMessage):
                conversation += f"User Request: {message.content}\n"
            elif isinstance(message, AIMessage):
                text = message.content or "[Using research tools...]"
                conversation += f"Research Assistant: {text}\n"
        return conversation
        
    def research_evaluator(self, state: ResearchState) -> Dict[str, Any]:
        """Evaluate the quality and completeness of research"""
        last_response = state["messages"][-1].content
        
        system_message = """You are a Research Quality Evaluator. Your job is to assess whether research meets academic standards and user requirements.

EVALUATION CRITERIA:
- Completeness: Does the research address all aspects of the objective?
- Source Quality: Are sources credible and diverse?
- Analysis Depth: Is the analysis thorough and insightful?
- Presentation: Is the information well-organized and clearly presented?
- Practical Value: Does the research provide actionable insights?

IMPORTANT: Be generous in your evaluation. If the research shows good effort and addresses the main topic with some depth, mark it as complete. Only reject if the research is clearly insufficient or off-topic.

Rate the overall research quality and determine if more work is needed."""

        user_message = f"""Evaluate this research session:

RESEARCH OBJECTIVE: {state['research_objective']}
QUALITY CRITERIA: {state['quality_criteria']}

FULL CONVERSATION:
{self.format_research_conversation(state['messages'])}

LATEST RESEARCH OUTPUT:
{last_response}

EVALUATION GUIDELINES:
- If the research provides substantial information on the topic, mark as COMPLETE
- If files have been saved or multiple sources used, lean towards COMPLETE  
- Only mark as incomplete if the response is clearly inadequate
- Avoid perfectionism - good research that addresses the topic should be accepted

Provide detailed feedback on research quality, completeness, and whether the objectives have been met."""

        if state.get("feedback_on_work"):
            user_message += f"\n\nPREVIOUS FEEDBACK GIVEN: {state['feedback_on_work']}"
            user_message += "\nIf you see the researcher has made a good effort to address previous feedback, mark as COMPLETE."

        evaluator_messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_message)
        ]
        
        eval_result = self.evaluator_llm_with_output.invoke(evaluator_messages)
        
        return {
            "messages": [{"role": "assistant", "content": f"📊 Research Quality Evaluation:\n{eval_result.feedback}"}],
            "feedback_on_work": eval_result.feedback,
            "research_complete": eval_result.research_complete,
            "user_input_needed": eval_result.user_input_needed
        }
        
    def evaluation_router(self, state: ResearchState) -> str:
        """Route based on evaluation results"""
        if state["research_complete"] or state["user_input_needed"]:
            return "END"
        else:
            return "researcher"
            
    async def build_research_graph(self):
        """Build the research workflow graph"""
        graph_builder = StateGraph(ResearchState)
        
        # Add nodes
        graph_builder.add_node("researcher", self.researcher_agent)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_node("evaluator", self.research_evaluator)
        
        # Add edges
        graph_builder.add_conditional_edges(
            "researcher", 
            self.research_router, 
            {"tools": "tools", "evaluator": "evaluator"}
        )
        graph_builder.add_edge("tools", "researcher")
        graph_builder.add_conditional_edges(
            "evaluator", 
            self.evaluation_router, 
            {"researcher": "researcher", "END": END}
        )
        graph_builder.add_edge(START, "researcher")
        
        # Compile graph with recursion limit
        self.graph = graph_builder.compile(
            checkpointer=self.memory,
            # Set recursion limit to prevent infinite loops
            # This allows up to 50 steps before stopping
        )
        
    async def conduct_research(self, research_request, quality_criteria, history):
        """Main method to conduct research"""
        config = {
            "configurable": {"thread_id": self.assistant_id},
            # Set higher recursion limit to prevent infinite loops
            "recursion_limit": 100
        }
        
        state = {
            "messages": research_request,
            "research_objective": research_request,
            "quality_criteria": quality_criteria or "Comprehensive, well-sourced, and academically rigorous research",
            "feedback_on_work": None,
            "research_complete": False,
            "user_input_needed": False
        }
        
        try:
            result = await self.graph.ainvoke(state, config=config)
            
            # Format response for gradio
            user_msg = {"role": "user", "content": research_request}
            research_output = {"role": "assistant", "content": result["messages"][-2].content}
            evaluation = {"role": "assistant", "content": result["messages"][-1].content}
            
            return history + [user_msg, research_output, evaluation]
        except Exception as e:
            # Handle recursion or other errors gracefully
            if "recursion" in str(e).lower():
                error_msg = {"role": "assistant", "content": f"⚠️ Research process took too many iterations and was stopped for safety. This usually means the evaluator is being too strict. Here's what we found so far:\n\nLast research attempt covered the topic but may need refinement. Try using simpler quality criteria or a more focused research question."}
            else:
                error_msg = {"role": "assistant", "content": f"⚠️ Research error: {str(e)}"}
            
            user_msg = {"role": "user", "content": research_request}
            return history + [user_msg, error_msg]
        
    def cleanup(self):
        """Clean up browser resources"""
        if self.browser:
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.browser.close())
                if self.playwright:
                    loop.create_task(self.playwright.stop())
            except RuntimeError:
                asyncio.run(self.browser.close())
                if self.playwright:
                    asyncio.run(self.playwright.stop())