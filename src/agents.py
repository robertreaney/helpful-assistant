from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseOutputParser
from langchain.agents import load_tools, initialize_agent, AgentType, AgentExecutor
from langchain.llms import OpenAI
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser

import logging

from tools import add, get, delete

# class OrganizedListOutputParser(BaseOutputParser):
#     """Parse the output of an LLM call to a comma-separated list."""

#     def parse(self, text: str):
#         """Parse the output of an LLM call."""
#         return text.strip().split(", ")

class RecordKeeper:
    template = """You are a helpful assistant who helps users interact with a list to help them remember.
    You will either ingest new things to add to the list or retreive the list for the user.
    """

    def __init__(self):
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", self.template),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])   

        self.llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
        self.tools=[add, get, delete]

        self.llm_with_tools = self.llm.bind(functions=[format_tool_to_openai_function(t) for t in self.tools])

    def __call__(self, input):
        logging.info(f'calling RecordKeeper agent with input={input}')
        agent = self._get_agent(input)
        executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True, max_execution_time=15)
        return executor.invoke({'input': input})

    def _get_agent(self, input):
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(x["intermediate_steps"]),
            }
            | self.prompt
            | self.llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )
        return agent
    
    def _test(self, input):
        agent = self._get_agent(input)
        return agent.invoke({"input": input, "intermediate_steps": []})


class Organizer:
    template = """You are a helpful assistant who organizes events and things people need to remember.
    A user will pass in a list things, and you should group them into similar categories.
    Example categories are: groceries, hardware store, chores, movies, other.

    It extremely important nothing from the unorganized list is forgotten from the result. It is better to misclassify than to forget.
    """

    def __call__(self, unorganized_list):
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.template),
            ("user", "{text}"),
        ])

        chain = prompt | ChatOpenAI()
        response = chain.invoke({"text": unorganized_list})

        return response
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # agent = Organizer()
    # response = agent("cabbot cheese\nmilk\nchange oil in truck\nflashlight\nsmall wrenches\nShrek\nscrews")
    # print(response)

    agent = RecordKeeper()
    response = agent._test('remember to buy the following:\ncheese, milk, eggs')
    print(response)
    response = agent._test('what is on my list?')
    print(response)