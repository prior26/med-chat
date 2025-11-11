"""
This contains the main agent class.
All agents will use this class as the parent class.
"""

import ollama
import json
from logger import TheLogger
from PIL import Image
import requests

class LLM:
    _instance = None
    
    @classmethod
    def getInstance(cls, model_name:str):
        if cls._instance is None:
            cls._instance = ollama.Client()
        return cls._instance

class Agent:
    def __init__(
            self,
            base_llm:str,
            name:str, 
            system_prompt:str,
            is_judge:bool, 
            stream:bool, 
            temperature:int, 
            top_p:int,
            one_shot_example: list,
            context_length_multiplier:int,
            logger: TheLogger
        ):
        self.llm_client = LLM.getInstance(base_llm)
        self.llm = base_llm
        self.name = f"{name}"
        self.system_prompt = system_prompt
        self.one_shot_example = one_shot_example
        self.is_judge = is_judge
        self.stream = stream
        self.FORMAT = None
        self.TEMPERATURE = temperature
        self.TOP_P = top_p
        self.CONTEXT_LENGTH = 2048*context_length_multiplier
        self.logger = logger
    
    def set_format(self, format):
        self.FORMAT = format

    def run(self, prompt:tuple, context:tuple = None):
        """
        """
        response = self.llm_client.chat(
            model=self.llm, 
            messages=self._get_msgs(prompt=prompt, context=context),
            options={"temperature": self.TEMPERATURE, "top_p": self.TOP_P, "num_ctx": self.CONTEXT_LENGTH},
            format=self.FORMAT
        )
        return response['message']['content']
    
    def validate_response(self, response):
        """
        A method to valdiate response for the agent.
        Should be different for each agent.
        
        Input:
            response - Agent's output
        Output:
            (bool, error) - (True, None) if validated else (False, "Error: ...")
        """
        return
    
    def get_image(self, image_path):
        """
        Modify as needed for Anything RAG
        """
        return Image.open(image_path)
    
    def _get_msgs(self, prompt:tuple|str, context:tuple|str = None):
        """
        Inputs: for med-agent
            prompt: (type, prompt)
            context: (type, context)
            --
            type: Choose from ['text', 'image']
            if type is image, then the provided prompt/context should be the image opened by the provided function get_image()
        Inputs: for judge-llm
            prompt: str
            context: str
        """
        if not self.is_judge:
            msgs:list = [
                {
                "role": "system", 
                "content": [
                    {"type": "text", "text": self.system_prompt}
                ]
                },
            ]
            if len(self.one_shot_example) > 0: msgs.extend(self.one_shot_example)

            if context is not None:
                _type, _context = context
                msgs.append(
                    {
                        "role": "user",
                        "content": [
                            {"type": _type, _type: _context}
                        ]
                    }
                )
            _type, _prompt = prompt
            msgs.append(
                {
                "role": "user", 
                "content": [
                    {"type": _type, _type: _prompt}
                ]
                }
            )
        else:
            msgs:list = [
            {
              "role": "system", # "system" is a prompt to define how the model should act.
              "content": self.systemPrompt # system prompt should be written here
            },
            ]
            if len(self.oneShotLearningExample) > 0: msgs.extend(self.oneShotLearningExample)

            if context != "":
                msgs.append(
                    {
                        "role": "user",
                        "content": context
                    }
                )
            
            msgs.append(
                {
                "role": "user", # "user" is a prompt provided by the user.
                "content": prompt # user prompt should be written here
                }
            )
            
        return msgs