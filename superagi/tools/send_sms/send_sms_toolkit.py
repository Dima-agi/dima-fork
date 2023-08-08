from abc import ABC
from typing import Type, List
from superagi.tools.base_tool import BaseToolkit, BaseTool
from superagi.tools.send_sms.tools import SMSTool


class SMSToolkit(BaseToolkit, ABC):
    name: str = "DIMA SMS"
    description: str = "SMS Tool to send sms messages on the phone numbers"
 
    def get_tools(self) -> List[BaseTool]:
        return [SMSTool()]
    
    def get_env_keys(self) -> List[str]:
        return []