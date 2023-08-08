from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool, BaseToolkit
from superagi.tools.tree_of_thought.tools import ToTTool


class ToTToolkit(BaseToolkit, ABC):
    name: str = "DIMA-Tree-of-Thought"
    description: str = "Toolkit containing tools for intelligent and detailed market research and studies on multiple fields."

    def get_tools(self) -> List[BaseTool]:
        return [
            ToTTool(),
        ]

    def get_env_keys(self) -> List[str]:
        return []
