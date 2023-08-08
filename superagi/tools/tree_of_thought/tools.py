from typing import Type, Optional, List
import os
from pydantic import BaseModel, Field

from superagi.agent.agent_prompt_builder import AgentPromptBuilder
from superagi.helper.prompt_reader import PromptReader
from superagi.lib.logger import logger
from superagi.llms.base_llm import BaseLlm
from superagi.tools.base_tool import BaseTool
from superagi.tools.tool_response_query_manager import ToolResponseQueryManager
 
from superagi.tools.tree_of_thought.t_o_t.openaiModels import OpenAILanguageModel
from superagi.tools.tree_of_thought.t_o_t.treeofthoughts import MonteCarloTreeofThoughts


class ToTSchema(BaseModel):
    task_description: str = Field(
        ...,
        description="Task reasearch that needs more details and do a great market research analysis on the topics given.",
    )

class ToTTool(BaseTool):
    
    """
    Thinking tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
        llm: LLM used for thinking.
    """ 
    llm: Optional[BaseLlm] = None
    name = "DIMA-ToT-Research"
    description = (
        "Intelligent journalist and good at problem-solving assistant that takes a more journalistic approach on the tasks,makes sure to double-check the sources,and can generate a market research report and make efficient decisions.All while providing detailed, self-driven reasoning for its choices. Do not assume anything, take the details from given data only."
    )
    args_schema: Type[ToTSchema] = ToTSchema
    
    permission_required: bool = False
    tool_response_manager: Optional[ToolResponseQueryManager] = None
    goals: List[str] = []
    class Config:
        arbitrary_types_allowed = True
        


    def _execute(self, task_description: str):
        """
        Execute the Thinking tool.

        Args:
            task_description : The task description.

        Returns:
            Thought process of llm for the task
        """
        try:
            api_model= "gpt-3.5-turbo"
            model = OpenAILanguageModel(api_key='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', api_model=api_model)
        # Initialize the MonteCarloTreeofThoughts class with the model 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
            tree_of_thoughts = MonteCarloTreeofThoughts(model)
            
            prompt = PromptReader.read_tools_prompt(__file__, "tot_research.txt")
            prompt = prompt.replace("{goals}", AgentPromptBuilder.add_list_items_to_string(self.goals))
            prompt = prompt.replace("{task_description}", task_description)
            last_tool_response = self.tool_response_manager.get_last_response()
            prompt = prompt.replace("{last_tool_response}", last_tool_response)
            
            # return result["content"]
            
            initial_prompt = " ".join(last_tool_response) + " Dat fiind task-ul acesta (Think of a plan on how to properly engage customers of a clothing brand from Polland on social media), urmatorii pasi posibili ar putea fi:"
            num_thoughts = 3
            max_steps = 2
            max_states = 2
            pruning_threshold = 0.5

            prompt = tree_of_thoughts.solve(
                initial_prompt=initial_prompt,
                num_thoughts=num_thoughts, 
                max_steps=max_steps, 
                max_states=max_states, 
                pruning_threshold=pruning_threshold,
                )
            # print(f"Solution: {prompt}")
            
            messages = [{"role": "system", "content": prompt}]
            result = self.llm.chat_completion(messages, max_tokens=self.max_token_limit)
            # return result["content"]
            return result
        
        except Exception as e:
            logger.error(e)
            return f"Error generating text: {e}"
        
        
        




# # Note to reproduce the same results from the tree of thoughts paper if not better, 
# # craft an 1 shot chain of thought prompt for your task below


# print(f"Solution: {solution}")