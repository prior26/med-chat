from llm_base import Agent
from pydantic import BaseModel

class MedAgent(Agent):
    def __init__(self, base_llm, name, system_prompt, stream, temperature, top_p, one_shot_example, context_length_multiplier, logger):
        super().__init__(
            base_llm = base_llm, 
            name = name, 
            system_prompt = system_prompt, 
            is_judge = False,
            stream = stream, 
            temperature = temperature, 
            top_p = top_p, 
            one_shot_example = one_shot_example, 
            context_length_multiplier = context_length_multiplier, 
            logger = logger
        )
    
    def retrieve(self, prompt:tuple, context:tuple, rag_file_path:str):
        """
        Inputs:
            prompt: (type, prompt)
            context: (type, context)
            rag_file_path: str, path to the file from which the question is being asked.
            --
            type: Choose from ['text', 'image']
            if type is image, then the provided prompt/context should be the image opened by the provided function get_image()
        """
        pass

    def validate_response(self, response):
        """
        A method to valdiate response for the agent.
        Should be different for each agent.
        
        Input:
            response - Agent's output
        Output:
            (bool, error) - (True, None) if validated else (False, "Error: ...")
        """
        pass

    def validate_retrieval(self, retrieval):
        """
        return True if validated else False
        """
        pass

    def create_prompt_with_question(self, q):
        return f"Here is the question: '{q}'"
    
    def run(self, prompt:tuple, context:tuple, rag_file_path:str):
        """
        Inputs:
            prompt: (type, prompt)
            context: (type, context)
            --
            type: Choose from ['text', 'image']
            if type is image, then the provided prompt/context should be the image opened by the provided function get_image()
        """
        context:tuple = self.validate_retrieval(self.retrieve(prompt, context, rag_file_path))
        while not self.validate_retrieval:
            context:tuple = self.validate_retrieval(self.retrieve(prompt, context, rag_file_path))
        return super().run(prompt, context)

class JudgeAgent(Agent):
    def __init__(self, base_llm, name, system_prompt, stream, temperature, top_p, one_shot_example, context_length_multiplier, logger):
        super().__init__(
            base_llm = base_llm, 
            name = name, 
            system_prompt = system_prompt, 
            is_judge = True,
            stream = stream, 
            temperature = temperature, 
            top_p = top_p, 
            one_shot_example = one_shot_example, 
            context_length_multiplier = context_length_multiplier, 
            logger = logger,
        )
        self.set_format(format=Score.model_json_schema())
    
    def create_prompt_from_answers(self, answer_og, answer_gen):
        prompt =   "> Here is the ground truth and response -\n"
        prompt += f"ground truth: {answer_og}\n"
        prompt += f"response: {answer_gen}"
        # prompt += f""
        return prompt

    def validate_response(self, response):
        """
        A method to valdiate response for the agent.
        Should be different for each agent.
        
        Input:
            response - Agent's output
        Output:
            (bool, error) - (True, None) if validated else (False, "Error: ...")
        """
        return True

    def run(self, prompt:str, context:str):
        """
        Inputs:
            prompt: (type, prompt)
            context: (type, context)
            --
            type: Choose from ['text', 'image']
            if type is image, then the provided prompt/context should be the image opened by the provided function get_image()
        """
        response = super().run(prompt, context)
        while self.validate_response(response) == False:
            response = super().run(prompt, context)
        return response

class Score(BaseModel):
    score: int