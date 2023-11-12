from langchain.tools import tool
from pydantic import BaseModel, Field
import logging
from langchain.tools.base import ToolException

# custom code
from helpers import ListFile

# class AddInput(BaseModel):
#     items: str = Field(description="items should be separated by a newline char to be individually added to the list.")

def _handle_error(error: ToolException) -> str:
    return (
        "The following errors occurred during tool execution:"
        + error.args[0]
        + "Please try another tool."
    )

@tool()
def add(items:str) -> str:
    """Helps user remember things. Adds items of a string to the user's list . Items should be separated by a newline character."""
    try:
        logging.info('triggered `add` tool')
        file = ListFile()
        if hasattr(file, 'content'):
            logging.info(f'items={items} old_content={file.content}')
            new_list = file.content + "\n" + items
        else:
            logging.info(f'items={items}')
            new_list = items

        file.write(new_list)
        return f"Succesfully wrote to list file\n\nYour List:\n\n{new_list}"
    except:
        raise ToolException("add tool call failed")

@tool
def get(x:str) -> str:
    """Retrieves the user's list."""
    try:
        logging.info('triggered `get` tool')
        file = ListFile()
        return file.content
    except:
        raise ToolException('get tool call failed')