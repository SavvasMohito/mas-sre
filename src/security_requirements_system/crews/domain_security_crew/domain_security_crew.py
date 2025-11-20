from typing import List

from crewai import LLM, Agent, Crew, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from security_requirements_system.data_models import DomainSecurityOutput
from security_requirements_system.tools.weaviate_tool import WeaviateQueryTool


@CrewBase
class DomainSecurityCrew:
    """Domain Security Crew - Maps requirements to security standards"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def domain_security_expert(self) -> Agent:
        # Using GPT-5-mini for security control mapping with tool-based database queries
        # Agent queries database directly for each requirement
        # Reduced query limit to 4 per requirement to avoid overcrowding
        # Complex multi-step task: analyze → query → map → explain
        # Must ensure completeness (no skipped requirements)
        # Increased timeout and added retry configuration for connection stability
        llm = LLM(
            model="openai/gpt-5-mini",
            timeout=1200,  # 20 minutes for large requirement sets
            max_retries=3,  # Retry on connection errors
        )
        # Tool for querying security standards database
        tool = WeaviateQueryTool(name="Query Security Standards Database")
        return Agent(
            config=self.agents_config["domain_security_expert"],
            tools=[tool],
            llm=llm,
            verbose=True,
        )

    @task
    def map_security_controls(self) -> Task:
        return Task(
            name="map_security_controls",
            config=self.tasks_config["map_security_controls"],
            output_pydantic=DomainSecurityOutput,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Domain Security Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True,
        )
