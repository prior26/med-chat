from logger import TheLogger
from llm_base import Agent
from config import MyConfig
from med_agent import MedAgent
import json



if __name__ == "__main__":
    config = MyConfig("config.json")
    logger = TheLogger(modelName=config.model_name,saveToFolder=config.dir_logs)
    model = MedAgent(
        base_llm = config['model'],
        name = config.model_name,
        system_prompt = config.system_prompt,
        stream = False,
        temperature = config.model_params['temperature'],
        top_p = config.model_params['top_p'],
        one_shot_example = config.one_shot_example,
        context_length_multiplier = config.model_params['context_length_multiplier'],
        logger = logger
    )
    gen_QA = {}
    for file_path in config.QA.keys():
        questions = config.QA[file_path]['questions']
        answers = config.QA[file_path]['answers']
        item = []
        for i in range(len(questions)):
            q = questions[i]
            prompt = model.create_prompt_with_question(q=q)
            response = model.run(prompt=prompt, rag_file_path=file_path)
            item.append({
                "question": q,
                "answer_act": answers[i],
                "answer_gen": response
            })

        gen_QA[file_path] = item
    
    # save generated QA's
    with open(config.path_output_qa_save, 'w') as f:
        json.dump(gen_QA, f, indent=4)

    