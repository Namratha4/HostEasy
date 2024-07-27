import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_json_agent
from langchain.agents.agent_toolkits import JsonToolkit
from langchain.tools.json.tool import  JsonSpec
import json
import streamlit as st
from langchain.prompts import PromptTemplate


openai_api_key = ''

# Load JSON data
file = "californias-iconic-case-study-house.json"
with open(file, "r") as f:
    data = json.load(f)

# Initialize the toolkit and agent
spec = JsonSpec(dict_=data, max_value_length=4000)
toolkit = JsonToolkit(spec=spec)
agent = create_json_agent(
    llm=ChatOpenAI(temperature=0, model="gpt-4", openai_api_key=openai_api_key),
    toolkit=toolkit,
    max_iterations=1000,
    verbose=False
)

# Streamlit application
st.title('Airbnb Co-Host Query Assistant')

# Input fields
host_name = "AK"
cohost_name = "Alfred"
user_query = st.text_area("Enter your query:")

if st.button('Submit'):
    if user_query:
        # Create and format the prompt
        prompt = """
        You have access to a JSON dataset which contains detailed information. Based on this data, please answer the following question:
        You are {cohost_name} an AirBNB co-host. {host_name} is the host of this building. You are a kind, helpful assistant. If you do not know any answer, tell the guests that you will reach out to the host & revert as soon as you can.
        User Query: {user_query}

        Use the information available in the JSON data to provide a detailed and accurate response.
        """
        prompt = PromptTemplate(
            input_variables=["host_name", "cohost_name", "user_query"],
            template=prompt
        )
        filled_prompt = prompt.format(host_name=host_name, cohost_name=cohost_name, user_query=user_query)
        
        # Generate response
        response = agent.run(filled_prompt)
        st.write("Response:", response)
    else:
        st.error("Please enter a query before submitting.")
