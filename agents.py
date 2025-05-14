import streamlit as st
from crewai import Agent, Task
from textwrap import dedent
from crewai_tools import (
    SerperDevTool,
    WebsiteSearchTool,
    ScrapeWebsiteTool
)
import re


# def streamlit_callback(agent_action):
#     # This function will be called after each step of the agent's execution
#     print("STEP OUTPUT ---------")
#     print(agent_action.__dict__)

#     st.markdown("---")
#     if isinstance(step, tuple) and len(step) == 2:
#         action, observation = step
#         if isinstance(action, dict) and "tool" in action and "tool_input" in action and "log" in action:
#             st.markdown(f"# Action")
#             st.markdown(f"**Tool:** {action['tool']}")
#             st.markdown(f"**Tool Input** {action['tool_input']}")
#             st.markdown(f"**Log:** {action['log']}")
#             st.markdown(f"**Action:** {action['Action']}")
#             st.markdown(
#                 f"**Action Input:** ```json\n{action['tool_input']}\n```")
#         elif isinstance(action, str):
#             st.markdown(f"**Action:** {action}")
#         else:
#             st.markdown(f"**Action:** {str(action)}")

#         st.markdown(f"**Observation**")
#         if isinstance(observation, str):
#             observation_lines = observation.split('\n')
#             for line in observation_lines:
#                 if line.startswith('Title: '):
#                     st.markdown(f"**Title:** {line[7:]}")
#                 elif line.startswith('Link: '):
#                     st.markdown(f"**Link:** {line[6:]}")
#                 elif line.startswith('Snippet: '):
#                     st.markdown(f"**Snippet:** {line[9:]}")
#                 elif line.startswith('-'):
#                     st.markdown(line)
#                 else:
#                     st.markdown(line)
#         else:
#             st.markdown(str(observation))
#     else:
#         st.markdown(step)

class Agents():
    def expert_research_agent(self):
        return Agent(
            role='Expert Researcher',
            goal='Research the required task and all the necessary steps to complete it',
            backstory='An expert in researching the required task with an exceptional ability to find the necessary information and attention to detail',
            # step_callback=streamlit_callback,
            verbose=True,
        )

    def checklist_generator_agent(self):
        return Agent(
            role='Checklist Generator',
            goal='Generate a checklist for the required task',
            backstory='An expert in generating checklist for the required task',
            # step_callback=streamlit_callback,
            verbose=True,
        )
    
    

class Tasks():
    def __init__(self):
        self.serper_tool = SerperDevTool()
        self.website_search_tool = WebsiteSearchTool()
        self.scrape_website_tool = ScrapeWebsiteTool()

    def expert_research_task(self, agent, task_description, details):
        return Task(
            agent=agent,
            description=dedent(f"""
            You are an expert researcher. You are given a task description and details. You need to research the task and all the necessary steps to complete it.
            Task Description: {task_description}
            Details: {details}
            """),
            expected_output="A list of steps to complete the task",
            tools=[self.serper_tool, self.website_search_tool, self.scrape_website_tool],
        )
    
    def generate_checklist(self, agent, task_description, details, context_task):
        return Task(
            agent=agent,
            description=dedent(f"""
            You are a checklist generator. You are given a task description and details. You need to generate a checklist for the task.
            The checklist should be in a question and answer format.
            It can contain text fields, multiple choice fields, select fields and any other appropriate fields needed to do the checklist.
            Use a variety of fields to make the checklist comprehensive and easy to use.

            Task Description: {task_description}
            Details: {details}
            """),
            expected_output="A checklist for the task",
            context=[context_task],
            output_file = "./test/checklist.md"
        )
    
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "Expert Researcher" in cleaned_data:
            # Apply different color 
            cleaned_data = cleaned_data.replace("Expert Researcher", f":{self.colors[self.color_index]}[Expert Researcher]")
        if "Checklist Generator" in cleaned_data:
            cleaned_data = cleaned_data.replace("Checklist Generator", f":{self.colors[self.color_index]}[Checklist Generator]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []
