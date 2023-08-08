from abc import ABC
from typing import Type, List
from superagi.tools.base_tool import BaseToolkit, BaseTool
from superagi.tools.make_call.tools import CALLTool


class SMSToolkit(BaseToolkit, ABC):
    name: str = "DIMA Call"
    description: str = "Phone Call Tool to call a phone number and make phone calls."
 
    def get_tools(self) -> List[BaseTool]:
        return [CALLTool()]
    
    def get_env_keys(self) -> List[str]:
        return []