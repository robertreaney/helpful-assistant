from langchain.tools import tool
import logging
from fuzzywuzzy import fuzz
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
def delete(items:str) -> str:
    """Removes items from a users list. Useful for when an item on the list has been accomplished. Items should be separated by a newline character."""
    try:
        logging.info('triggered `delete` tool')
        file = ListFile()
        cached_items = file.content.split('\n')
        incoming_items = [x.strip() for x in items.split('\n')]
        # new list is all the items from the original minus anything that matched the incoming items
        new_list = '\n'.join([x for x in cached_items if all([fuzz.ratio(x, y) < 80 for y in incoming_items])])
        logging.info(f'new={new_list} incoming={incoming_items} cached={cached_items}')
        file.write(new_list)
    except:
        ToolException('delete tool call failed')

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
        return f"Succesfully wrote to list file these items: {items}"
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