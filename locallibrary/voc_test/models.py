from .vocabulary_models import *
import random
class Quiz:
    num_choice = 4
    name = ''
    def __init__(self, state_dict):
        self.answer_state = state_dict['answer_state']
        self.vocs = state_dict['vocs']
        self.problem_idx = state_dict['problem_idx']
        self.choices_idx = state_dict['choices_idx']

    @classmethod
    def initialize_with_vocabulary_list(cls, voc_objects):
        voc_dict = { str(voc.id):
                        {
                            'question': str(voc.question),
                            'answer': str(voc.answer),
                        } 
            for voc in voc_objects
        }

        problem_idx = None
        choices_idx = None
        answer_state = None
        state_dict = {
            'answer_state': answer_state,
            'vocs': voc_dict,
            'problem_idx': problem_idx,
            'choices_idx': choices_idx
            }
        self = cls(state_dict)
        self.load_new_problem()
        return self


    @classmethod
    def randomized_initialize(cls, num_voc):
        if num_voc is None:
            return
        
        vocs_obj = vocabulary.objects.order_by('?').values()[:num_voc]
        vocs_obj = list(vocs_obj)
        return cls.initialize_with_vocabulary_list(vocs_obj)
    
    @classmethod
    def load_from_index_list(cls, idx_list):#idx_list will be a list of string, each element is str(UUID)
        vocs_obj = vocabulary.objects.filter(id__in=idx_list)
        return cls.initialize_with_vocabulary_list(vocs_obj)
    

    def load_state_dict(self, state_dict):
        self.answer_state = state_dict['answer_state']
        self.vocs = state_dict['vocs']
        self.problem_idx = state_dict['problem_idx']
        self.choices_idx = state_dict['choices_idx']

    def load_new_problem(self):
        print('calling load_new_problem')
        self.choices_idx = random.sample(list(self.vocs.keys()), self.num_choice)
        self.problem_idx = random.sample(self.choices_idx, 1)[0]

    def get_problem_view(self):
        # self.load_new_problem()
        question = self.vocs[ self.problem_idx ]['question']
        options = [  self.vocs[i]['answer'] for i in self.choices_idx]
        return question, options

    def answering(self, answer):
        if(not self.problem_idx in self.vocs.keys()):
            print("ERR")
            print(self.problem_idx)
            print(self.vocs.keys())
            return
        
        if answer != self.vocs[self.problem_idx]['answer']:
            return False
        else:
            # self.vocs.remove(self.problem)
            print('set to true')
            self.answer_state = True
            return True
    
    @property
    def remain_vocs(self):
        return len(self.vocs)

    # when user answering correct, this function remove problem from problemset and load a new problem
    def update_problem(self):
        print(self.answer_state)
        if self.answer_state is True:
            print('delete problem')
            self.vocs.pop(self.problem_idx, None)

        self.answer_state = None
        if len(self.vocs) <= 1:
            return False
        else:
            self.load_new_problem()
            return True

    def state_dict(self):
        # question_dict = {  str(k):str(self.vocs['question'][k]) for k in self.vocs['question'].keys()}
        # answer_dict = {  str(k):str(self.vocs['answer'][k]) for k in self.vocs['answer'].keys()}
        return {
            'answer_state': self.answer_state,
            'vocs':self.vocs,
            'problem_idx': self.problem_idx,
            'choices_idx': self.choices_idx
            }
