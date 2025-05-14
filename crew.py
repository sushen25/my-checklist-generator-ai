from crewai import Crew
from agents import Agents, Tasks

class ChecklistCrew():
    def __init__(self, task_description, details):
        self.agents = Agents()
        self.tasks = Tasks()
        self.task_description = task_description
        self.details = details

    def run(self):
        research_agent = self.agents.expert_research_agent()
        checklist_agent = self.agents.checklist_generator_agent()

        research_task = self.tasks.expert_research_task(research_agent, self.task_description, self.details)
        checklist_task = self.tasks.generate_checklist(checklist_agent, self.task_description, self.details, research_task)

        crew = Crew(
            agents=[research_agent, checklist_agent],
            tasks=[research_task, checklist_task],
        )
        result = crew.kickoff()
        return result

