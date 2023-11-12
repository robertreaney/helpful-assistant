from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

# class OrganizedListOutputParser(BaseOutputParser):
#     """Parse the output of an LLM call to a comma-separated list."""

#     def parse(self, text: str):
#         """Parse the output of an LLM call."""
#         return text.strip().split(", ")

class HelpfulReminder:
    template = """You are a helpful assistant who organizes events and things people need to remember.
    A user will pass in a list things, and you should group them into similar categories.
    Example categories are: groceries, hardware store, chores, movies, other.

    It extremely important nothing from the unorganized list is forgotten from the result. It is better to misclassify than to forget.
    """

    def __call__(self, unorganized_list):
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", self.template),
            ("human", "{text}"),
        ])

        chain = chat_prompt | ChatOpenAI()
        response = chain.invoke({"text": unorganized_list})

        return response
    
if __name__ == '__main__':
    agent = HelpfulReminder()
    response = agent("cabbot cheese\nmilk\nchange oil in truck\nflashlight\nsmall wrenches\nShrek\nscrews")
    print(response)