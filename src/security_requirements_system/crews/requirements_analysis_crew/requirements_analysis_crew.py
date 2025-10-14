from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class RequirementsAnalysisCrew:
    """Requirements Analysis Crew - Parses and analyzes PM requirements"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def requirements_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["requirements_analyst"],
            verbose=True,
        )

    @task
    def analyze_requirements(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_requirements"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Requirements Analysis Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
