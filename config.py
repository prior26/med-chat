import json
import os

class MyConfig:
    
    def __init__(self, path):
        with open(path, 'r') as f:
            self.main_config = json.load(f)

        self.model_name = self.main_config['model'].replace('/','_')
        self.model_params = self.main_config['params']
        self.paths = self.main_config['paths']
        
        # Loading The main system prompt for evaluator LLM 
        with open(self.paths['system_prompt']) as f:
            self.system_prompt = str(f.read())
        self.dir_logs = self.paths['logs_folder']
        self.dir_data = self.paths['data_folder']
        self.dir_output = self.paths['output_folder']

        self.experiment_num = len(list(os.listdir(self.dir_output)))
        self.path_output_qa_save = f"{self.dir_output}/gen_QA_exp{self.experiment_num: 02d}"
        
        #  One shot example if there is any
        self.one_shot_example = None
        if self.paths['one_shot_example'] != "":
            with open(self.paths['one_shot_example'], 'r') as f:
                self.one_shot_example = str(f.read())
        
        # Loading QA pairs for testing
        with open(self.paths['test_QA'], 'r') as f:
            QA_file:dict = json.load(f)
        
        self.QA = {}
        for f_path in QA_file.keys():
            file_path = os.path.join(self.dir_data, f_path)
            questions = list(QA_file[f_path].keys())
            answers = list(QA_file[f_path].values())
            self.QA[file_path] = {
                "questions": questions,
                "answers": answers
            }
        