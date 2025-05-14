import streamlit as st
import os
from crew import ChecklistCrew
from agents import StreamToExpander
import sys


os.environ["SERPER_API_KEY"] = "<serper_api_key>" # serper.dev API key
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o'


st.title("Checklist Template Generator")

# Create a form in the sidebar
with st.sidebar.form("template_form"):
    st.write("## Template Details")
    
    # Add text input fields
    template_description = st.text_input("Checklist Template Description")
    more_details = st.text_area("More Details")
    
    # Add submit button
    submitted = st.form_submit_button("Submit")
    
    # Handle form submission
    if submitted:
        st.sidebar.success("Form submitted successfully!")

# Display submitted data in the main area
if 'submitted' in locals() and submitted:
    st.write("### Submitted Information:")
    st.write("**Template Description:**", template_description)
    st.write("**More Details:**", more_details)

    # This line redirects the standard output (stdout) to a custom StreamToExpander object
    # StreamToExpander is a custom class that captures output and displays it in a Streamlit expander
    # It formats agent actions and progress with colors and toast notifications
    # This allows us to see the AI agents' work in real-time in the Streamlit UI
    sys.stdout = StreamToExpander(st)
    crew = ChecklistCrew(template_description, more_details)

    result = crew.run()

    st.subheader("Here is your Checklist Template", anchor=False, divider="rainbow")
    st.write(result.raw)


