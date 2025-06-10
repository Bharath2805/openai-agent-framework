from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from cybersecuritythreatintelligencesystem.tools.custom_tool import WhatsAppTool
from typing import List

@CrewBase
class Cybersecuritythreatintelligencesystem():
    """Cybersecurity Threat Intelligence System crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Agent definitions
    @agent
    def threat_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['threat_researcher'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def malware_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['malware_analyst'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def phishing_watcher(self) -> Agent:
        return Agent(
            config=self.agents_config['phishing_watcher'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def news_monitor(self) -> Agent:
        return Agent(
            config=self.agents_config['news_monitor'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def security_report_compiler(self) -> Agent:
        return Agent(
            config=self.agents_config['security_report_compiler'],
            tools=[WhatsAppTool()],
            verbose=True
        )

    # Task definitions
    @task
    def cyber_threat_research(self) -> Task:
        return Task(
            config=self.tasks_config['cyber_threat_research']
        )

    @task
    def malware_summary(self) -> Task:
        return Task(
            config=self.tasks_config['malware_summary'],
            output_file='output/malware_summary.md'
        )

    @task
    def phishing_campaigns_report(self) -> Task:
        return Task(
            config=self.tasks_config['phishing_campaigns_report'],
            output_file='output/phishing_report.md'
        )

    @task
    def cyber_news_summary(self) -> Task:
        return Task(
            config=self.tasks_config['cyber_news_summary'],
            output_file='output/cyber_news.md'
        )

    @task
    def daily_security_bulletin(self) -> Task:
        return Task(
            config=self.tasks_config['daily_security_bulletin'],
            output_file='output/final_security_bulletin.md'
        )

    # Crew definition
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )