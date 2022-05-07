import os
import json
import argparse
from signal import pause
import numpy as np
import pandas as pd




def cat_lists(lists):
    o = []
    for l in lists:
        o += l
    return o

class DictFile:
    def __init__(self, data):
        self.data = data

    def filter(self, kwargs):
        if isinstance(kwargs, dict):
            result = list(filter(lambda x: all([x[k]==v for k,v in kwargs.items()]), self.data))
        elif isinstance(kwargs, list):
            result = list(filter(lambda x: all([k in x for k in kwargs]), self.data))
        elif isinstance(kwargs, str):
            result = list(filter(lambda x: kwargs in x, self.data))
            
        return DictFile(result)
    
    def select(self, arg):
        return self.data[arg]       

    def __getitem__(self, i):
        return DictFile(self.data[i])
    
    def __len__(self):
        return len(self.data)



def parse_data(data):
    
    # def load_instruction_data(k, data):
    #     n = k
    #     rt_instruction = []
    #     while data[n]['trial_type'] == 'html-keyboard-response' and n < len(data):
    #         rt_instruction.append(data[n]['rt'])
    #         n+=1
    #     return rt_instruction, k 
       
    # def load_comp_check_data(k, data):
    #     n = k
    #     rt_instruction_repeat = []
    #     n_comp_checks = 0
    #     while data[n]['trial_type'] == 'html-keyboard-response' or data[n]['trial_type'] == 'survey-multi-select' and n < len(data):
    #         if data[n]['trial_type'] == 'html-keyboard-response':
    #             rt_instruction_repeat.append(data[n]['rt'])
    #         if data[n]['trial_type'] == 'survey-multi-select':
    #             n_comp_checks += 1
    #     return rt_instruction_repeat, n_comp_checks

    n = 0
    ############ load instruction data
    rt_instruction = []
    while n<len(data) and data[n]['trial_type'] != 'survey-multi-select':
        if 'rt' in data[n]:
            rt_instruction.append(data[n]['rt'])
        n+=1

    ############ load comprehension checks data
    rt_instruction_repeat = []
    n_comp_checks = 0
    while n<len(data) and (data[n]['trial_type'] == 'html-keyboard-response' or data[n]['trial_type'] == 'survey-multi-select'):
        if data[n]['trial_type'] == 'html-keyboard-response':
            rt_instruction_repeat.append(data[n]['rt'])
        if data[n]['trial_type'] == 'survey-multi-select':
            n_comp_checks += 1

        n+=1

    ############ load attention checks data
    att_checks_idx = [i for i,x in enumerate(data) if 'catch_trial' in x and x['catch_trial']]
    att_checks_acc = [data[i]['correct']*1 for i in att_checks_idx]
    ############ load practice block data
    block_idx = -1
    accuracy = []
    response_rt = []
    feedback_rt = []
    mouse_data = []
    confidence_score = []

    trial_idx = []
    trial_idx_c = 0
    while n<len(data) and data[n]['trial_type'] == 'image-click':
        if data[n+1]['catch_trial']:
            n+=4
            continue
        seq = data[n:n+4]
        # fixation, choice, confidence, feedback

        if 'stim_idx' in seq[1]:
            trial_idx.append(seq[1]['stim_idx'])
        else:
            trial_idx.append(trial_idx_c)
        trial_idx_c +=1        

        response_rt.append(seq[1]['rt'])
        accuracy.append(seq[1]['correct']*1)
        feedback_rt.append(seq[3]['rt'])
        confidence_score.append(seq[2]['response'])

        mouse = []
        for s in seq[1]['mouse_tracking_data']:
            mouse.append([s['x'], s['y'], s['t']])
        
        mouse_data.append([seq[1]['document_dims'], mouse])
        n+=4

    block = {
        'block_idx': -1,
        'response': accuracy,
        'response_rt': response_rt,
        'feedback_rt': feedback_rt,
        'mouse_data': mouse_data,
        'confidence_score': confidence_score,
        'accuracy': np.mean(accuracy),
        'response_rt_avg': np.mean(response_rt),
        'feedback_rt': np.mean(feedback_rt),
    }

    practice_block_data = block

    exp_blocks = []
    block_idx = 0
    while n<len(data):
        pause_time = 0
        while n<len(data) and (data[n]['trial_type'] == 'html-keyboard-response' or data[n]['trial_type'] == 'preload'):
            pause_time += data[n]["rt"] if ("rt" in data[n] and data[n]['rt'] is not None) else 0
            n+=1

        
        accuracy = []
        response_rt = []
        feedback_rt = []
        mouse_data = []
        confidence_score = []
        task_desc = ""

        trial_idx = []
        trial_idx_c = 0
        while n<len(data) and data[n]['trial_type'] == 'image-click':
            if data[n+1]['catch_trial']:
                n+=4
                continue
            seq = data[n:n+4]
            # fixation, choice, confidence, feedback

            if 'stim_idx' in seq[1]:
                trial_idx.append(seq[1]['stim_idx'])
            else:
                trial_idx.append(trial_idx_c)
            trial_idx_c +=1        

            response_rt.append(seq[1]['rt'])
            accuracy.append(seq[1]['correct']*1)
            feedback_rt.append(seq[3]['rt'])
            confidence_score.append(seq[2]['response'])

            mouse = []
            for s in seq[1]['mouse_tracking_data']:
                mouse.append([s['x'], s['y'], s['t']])
            
            mouse_data.append([seq[1]['document_dims'], mouse])
            n+=4

        if n<len(data) and data[n]['trial_type'] == 'survey-text':
            task_desc = data[n]["response"]["Q0"]
            n+=1
        
        block = {
            'block_idx': block_idx,
            'pause_time': pause_time,
            'task_desc': task_desc,
            'response': accuracy,
            'response_rt': response_rt,
            'feedback_rt': feedback_rt,
            'mouse_data': mouse_data,
            'confidence_score': confidence_score,
            'trial_idx': trial_idx,
            'confidence_score_min': np.min(confidence_score) if len(confidence_score)>0 else None,
            'confidence_score_max': np.max(confidence_score) if len(confidence_score)>0 else None,
            'confidence_score_avg': np.mean(confidence_score),
            'accuracy': np.mean(accuracy),
            'response_rt_avg': np.mean(response_rt),
            'feedback_rt_avg': np.mean(feedback_rt),
            'attention_check': att_checks_acc[block_idx] if block_idx<len(att_checks_acc) else None,
        }
        block_idx += 1
        exp_blocks.append(block)

    exp_data = {
        'rt_instruction': np.sum(rt_instruction), 
        'rt_instruction_repeat': np.mean(rt_instruction_repeat),
        'n_comp_checks': n_comp_checks, 
        'att_checks': att_checks_idx,
        'att_checks_n': len(att_checks_acc),
        'att_checks_acc': sum(att_checks_acc),
        'practice_block': practice_block_data,
        'blocks': exp_blocks,
        'accuracy': np.mean(cat_lists([b['response'] for b in exp_blocks])),
        'response_rt_avg': np.mean(cat_lists([b['response_rt'] for b in exp_blocks])),
        'response_rt_min': np.min(cat_lists([b['response_rt'] for b in exp_blocks])),
        'confidence_score_avg': np.mean(cat_lists([b['confidence_score'] for b in exp_blocks])),
        'confidence_score_std': np.std(cat_lists([b['confidence_score'] for b in exp_blocks])),
        'n_empty_task_desc': len([b for b in exp_blocks if b['task_desc']=='']),
    }

    return exp_data


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # parser.add_argument('--data_path', type=str, default='services/web/user_data/', help='path to human data')
    parser.add_argument('--data_path', type=str, default='services/web/user_data/', help='path to human data')
    parser.add_argument('--summary_path', type=str, default='summary_data.csv', help='csv file to generate')
    parser.add_argument('--block_summary_path', type=str, default='block_summary_data.csv', help='csv file to generate')
    parser.add_argument('--trial_summary_path', type=str, default='trial_summary_data.csv', help='csv file to generate')
    parser.add_argument('--out_data_path', type=str, default='data.npy', help='csv file to generate')

    args = parser.parse_args()

    # experiment db
    exp_db_path = os.path.join(args.data_path, 'exp_db')
    user_db_path = os.path.join(args.data_path, 'metadata')
    data_db_path = os.path.join(args.data_path, 'data')

    exp_db_path = os.path.join(args.data_path, 'exp_db_p')
    user_db_path = os.path.join(args.data_path, 'metadata_p')
    data_db_path = os.path.join(args.data_path, 'data_p')

    # load the experiments
    conditions = os.listdir(exp_db_path)

    # worker_ID, success, exp_id, task names, avg reaction time for each, min rt time for each, average accuracy for each, comprehension checks, attention checks, empty descriptions

    info_list = []
    summary_list = []
    block_summary_list = []
    trial_summary_list = []

    # load users and data associated
    # sbjs = []
    for i in range(len(conditions)):
        info = {}
        info['exp_id'] = conditions[i]
        with open(os.path.join(exp_db_path, conditions[i]), 'r') as f:
            # sbj = f.readline().split(' ')[-1]
            exp_lines = {l.rstrip('\n').split('\t')[1]: l.rstrip('\n').split('\t')[2].split(' ')  for l in f.readlines() }
        sbj = exp_lines['workerId'][0]

        info['worker_id'] = sbj

        with open(os.path.join(user_db_path, sbj), 'r') as f:
            usr_lines = {l.rstrip('\n').split('\t')[1]: l.rstrip('\n').split('\t')[2].split(' ')  for l in f.readlines() }
            # data_file = f.readlines()[3]
        info['success'] = 'complete' in usr_lines and usr_lines['complete']=='success'

        if 'subId' in usr_lines and os.path.exists(os.path.join(data_db_path, usr_lines['subId'][0]+'.json')):
            data_file = usr_lines['subId'][0]
            info['data_file'] = data_file

            with open(os.path.join(data_db_path, data_file+'.json'), 'rb') as f:
                data = json.load(f)

        else:
            continue
        

        # parse data
        info.update(parse_data(data))

        # task_perm = [int(i) for i in exp_lines['task_perm']]
        tasks = [pn+'_'+n.replace('task_','') for n, pn in zip(exp_lines['task_names'], exp_lines['task_perm_names'])]
        info.update({
            't_0': tasks[0],
            't_1': tasks[1],
            't_2': tasks[2],
            't_3': tasks[3],
            't_4': tasks[4],
            't_5': tasks[5],
            'acc_0': info['blocks'][0]['accuracy'],
            'acc_1': info['blocks'][1]['accuracy'],
            'acc_2': info['blocks'][2]['accuracy'],
            'acc_3': info['blocks'][3]['accuracy'],
            'acc_4': info['blocks'][4]['accuracy'],
            'acc_5': info['blocks'][5]['accuracy'],
        })
        info_list.append(info)

        # data_file
        summary = {
            # location
            'exp_id': info['exp_id'],
            'worker_id': info['worker_id'],
            'data_file': info['data_file'],
            # task details
            't_0': tasks[0],
            't_1': tasks[1],
            't_2': tasks[2],
            't_3': tasks[3],
            't_4': tasks[4],
            't_5': tasks[5],
            # success, rejection criterias
            'success': info['success'],
            'mean_rt': info['response_rt_avg'],
            'min_rt': info['response_rt_min'],
            'failed_comp_check': info['n_comp_checks'],
            'failed_att_check': info['att_checks_n'] - info['att_checks_acc'],
            'empty_desc': info['n_empty_task_desc'],
            # evalation
            'acc': info['accuracy'],
            'acc_0': info['blocks'][0]['accuracy'],
            'acc_1': info['blocks'][1]['accuracy'],
            'acc_2': info['blocks'][2]['accuracy'],
            'acc_3': info['blocks'][3]['accuracy'],
            'acc_4': info['blocks'][4]['accuracy'],
            'acc_5': info['blocks'][5]['accuracy'],
        }

        summary_list.append(summary)

        for j in range(6):
            
            # sort by blocks
            # task_id, task_name, exp_id, participant, data_file, ab, block_idx, accuracy, avg_rt, avg_confidence
            
            block_summary = {
                'exp_id': info['exp_id'],
                'worker_id': info['worker_id'],
                'data_file': info['data_file'],
                'task_idx': exp_lines['task_idx'][j],
                'task_names': exp_lines['task_names'][j],
                'task_perm': exp_lines['task_perm'][j],
                'task_perm_name': exp_lines['task_perm_names'][j],
                'acc': info['blocks'][j]['accuracy'],
                'conf_min': info['blocks'][j]['confidence_score_min'],
                'conf_max': info['blocks'][j]['confidence_score_max'],
                'conf_avg': info['blocks'][j]['confidence_score_avg'],
                'rt_avg': info['blocks'][j]['response_rt_avg'],
                'fb_rt_avg': info['blocks'][j]['feedback_rt_avg'],
                'att_check': info['blocks'][j]['attention_check'],
            }
            block_summary_list.append(block_summary)


            for k in range(len(info['blocks'][i]['response'])):
                
                # sort by blocks
                # task_id, task_name, exp_id, participant, data_file, ab, block_idx, accuracy, avg_rt, avg_confidence
                
                trial_summary = {
                    'exp_id': info['exp_id'],
                    'worker_id': info['worker_id'],
                    'data_file': info['data_file'],
                    'task_idx': exp_lines['task_idx'][j],
                    'task_names': exp_lines['task_names'][j],
                    'task_perm': exp_lines['task_perm'][j],
                    'task_perm_name': exp_lines['task_perm_names'][j],

                    'response': info['blocks'][j]['response'][k],
                    'rt': info['blocks'][j]['response_rt'][k],
                    'fb_rt': info['blocks'][j]['feedback_rt'][k],
                    'conf': info['blocks'][j]['confidence_score'][k],
                    'trial_idx': info['blocks'][j]['trial_idx'][k],
                }
                trial_summary_list.append(trial_summary)

    np.save(args.out_data_path, info_list)
    
    pd.DataFrame(summary_list).to_csv(args.summary_path)
    pd.DataFrame(block_summary_list).to_csv(args.block_summary_path)
    pd.DataFrame(trial_summary_list).to_csv(args.trial_summary_path)






# analyse mouse movements later when combined with metadata
        

### think of plotting and tests for this experiment
# ab are solved with a significantly higher accuracy/lower rt than ef, ac or bd  



########### 
 


# trials_pilot = [ # similar to the original setup
#     [[0, 1], [0, 8], [1, 2], [3, 4], [3, 4, 5, 6, 7]], 
#     [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
#     [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
#     [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
#     [[0, 3], [0, 2], [1, 4], [6, 7], [4, 5, 6, 7, 8]],
#     [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
#     [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
#     [[6, 8], [2, 6], [3, 8], [0, 7], [0, 1, 2, 3, 4]], 
#     [[3, 7], [3, 6], [2, 7], [1, 5], [0, 1, 4, 5, 8]], 
# ]
# trial_sequence_pilote =[
#     [0, 1, 3, 2],
#     [3, 2, 0, 1],
#     [1, 0, 2, 3],
#     [2, 3, 1, 0],
# ]

# COMP_TO_ELEM = {
#     0: [0],
#     1: [1],
#     2: [2],
#     3: [3],
#     4: [4],
#     5: [5],
#     6: [6],
#     7: [7],
#     8: [8],

#     49: [0,1], # "task_pos_shape_1"
#     56: [0,2], # "task_size_shape_1"
#     63: [0,3], # "task_shape_color"
#     86: [0,4], # "task_shape_rot_1"
#     95: [0,5], # "task_shape_flip_1"
#     68: [0,6], # "task_shape_count_1"
#     66: [0,7], # "task_shape_inside"
#     20: [0,8], # "task_shape_contact_2"

#     # 87: [0,8],
#     47: [1,2], # "task_pos_size_1"
#     53: [1,3], # "task_pos_col_1"
#     51: [1,4], # "task_pos_rot_1"
#     # 98: [1,4],
#     99: [1,5], # "task_pos_flip_1"
#     13: [1,6], # "task_pos_count_2"
#     24: [1,7], # "task_pos_inside_3"
#     55: [1,8], # "task_pos_contact"

#     82: [2,3], # "task_size_color_1"
#     103: [2,4], # "task_size_rot_2" # was previously 58: "task_size_rot"
#     97: [2,5], # "task_size_flip_1"
#     61: [2,6], # "task_size_count_1"
#     59: [2,7], # "task_size_inside_1"
#     60: [2,8], # "task_size_contact"

#     70: [3,4], # "task_rot_color"
#     94: [3,5], # "task_flip_color_1"
#     77: [3,6], # "task_color_count_1"
#     74: [3,7], # "task_color_inside_1"
#     76: [3,8], # "task_color_contact"

#     96: [4,5], # "task_rot_flip_1"
#     73: [4,6], # "task_rot_count_1"
#     104: [4,7], # 104 "task_rot_inside_3" # was previously 71:"task_rot_inside_1"
#     88: [4,8], # "task_rot_contact_1"

#     91: [5,6], # "task_flip_count_1" 
#     105: [5,7], # "task_flip_inside_3" # was previously 92: "task_flip_inside_1"
#     101: [5,8],# "task_flip_contact_1"

#     17: [6,7], # "task_inside_count_1"
#     80: [6,8], # "task_contact_count_1"
#     79: [7,8], # "task_inside_contact"

# }
# #  '{}-{}'.format(*v):k
# elem_comp = {'-'.join(str(v_) for v_ in v) for k,v in COMP_TO_ELEM.items()}

# for i in range(len(trials_pilot)):
# block 1 