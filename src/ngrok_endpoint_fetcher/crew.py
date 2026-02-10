import os
import sys
from pathlib import Path

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.mcp import MCPServerStdio




@CrewBase
class NgrokEndpointFetcherCrew:
    """NgrokEndpointFetcher crew"""

    
    @agent
    def command_executor(self) -> Agent:
        # Get path to the MCP server script
        mcp_server_path = Path(__file__).parent / "mcp_server.py"
        
        return Agent(
            config=self.agents_config["command_executor"],
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
            mcps=[
                MCPServerStdio(
                    command=sys.executable,  # Python interpreter
                    args=[str(mcp_server_path)],
                )
            ]
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


