import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	ScrapeWebsiteTool
)
from ngrok_endpoint_fetcher.tools.fetch_ngrok import FetchNgrokTool




@CrewBase
class NgrokEndpointFetcherCrew:
    """NgrokEndpointFetcher crew"""

    
    @agent
    def command_executor(self) -> Agent:
        
        return Agent(
            config=self.agents_config["command_executor"],
            
            
            tools=[				FetchNgrokTool(),
				ScrapeWebsiteTool()],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def execute_web_request(self) -> Task:
        return Task(
            config=self.tasks_config["execute_web_request"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the NgrokEndpointFetcher crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            chat_llm=LLM(model="openai/gpt-4o-mini"),
        )


