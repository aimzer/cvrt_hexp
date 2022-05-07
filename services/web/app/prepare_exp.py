import os
import copy
import numpy as np

# from app.prepare_exp import TASKS_NAMES

# each task is reapeated 4 times in the entire experiment


# -> 45 conditions should be done by participants 10 times each

# trial sequence: 10 types (1 per participant)
# ab ac bd ef
# ab ac ef bd
# ab ef ac bd
# ef ac bd ab
# ef ac ab bd
# ef ab ac bd
# ac ef bd ab
# ac ef ab bd
# ac ab ef bd
# ac ab bd ef

# participant idx p_idx 
# condition number (45) x trial types (10)
# t_type = p_idx//45
# con_n = p_idx%45
# this means that we do all 45 conditions before moving to a new trial type (in order to get as many conditions as possible)



TASKS_NAMES={
    ### elementary
    0: "task_shape",
    1: "task_pos",
    2: "task_size",
    3: "task_color",
    4: "task_rot",
    5: "task_flip",
    6: "task_count",
    7: "task_inside",
    8: "task_contact",
    9: "task_sym_rot",
    10: "task_sym_mir",
    ### compositions
    11: "task_pos_pos_1",
    12: "task_pos_pos_2",
    13: "task_pos_count_2",
    14: "task_pos_count_1",
    15: "task_pos_pos_4",
    16: "task_pos_count_3",
    17: "task_inside_count_1",
    18: "task_count_count",
    19: "task_shape_shape",
    20: "task_shape_contact_2",
    21: "task_contact_contact_1",
    22: "task_inside_inside_1",
    23: "task_inside_inside_2",
    24: "task_pos_inside_3",
    25: "task_pos_inside_1",
    26: "task_pos_inside_2",
    27: "task_pos_inside_4",
    28: "task_rot_rot_1",
    29: "task_rot_rot_2",
    30: "task_rot_rot_3",
    31: "task_pos_pos_3",
    32: "task_pos_count_4",
    33: "task_size_size_1",
    34: "task_size_size_2",
    35: "task_size_size_3",
    36: "task_size_size_4",
    37: "task_size_size_5",
    38: "task_size_sym_1",
    39: "task_size_sym_2",
    40: "task_color_color_1",
    41: "task_color_color_2",
    42: "task_sym_sym_1",
    43: "task_sym_sym_2",
    44: "task_shape_contact_3",
    45: "task_shape_contact_4",
    46: "task_contact_contact_2",
    47: "task_pos_size_1",
    48: "task_pos_size_2",
    49: "task_pos_shape_1",
    50: "task_pos_shape_2",
    51: "task_pos_rot_1",
    52: "task_pos_rot_2",
    53: "task_pos_col_1",
    54: "task_pos_col_2",
    55: "task_pos_contact",
    56: "task_size_shape_1",
    57: "task_size_shape_2",
    58: "task_size_rot",
    59: "task_size_inside_1",
    60: "task_size_contact",
    61: "task_size_count_1",
    62: "task_size_count_2",
    63: "task_shape_color",
    64: "task_shape_color_2",
    65: "task_shape_color_3",
    66: "task_shape_inside",
    67: "task_shape_inside_1",
    68: "task_shape_count_1",
    69: "task_shape_count_2",
    70: "task_rot_color",
    71: "task_rot_inside_1",
    72: "task_rot_inside_2",
    73: "task_rot_count_1",
    74: "task_color_inside_1",
    75: "task_color_inside_2",
    76: "task_color_contact",
    77: "task_color_count_1",
    78: "task_color_count_2",
    79: "task_inside_contact",
    80: "task_contact_count_1",
    81: "task_contact_count_2",
    ##### new
    82: "task_size_color_1",
    83: "task_size_color_2",
    84: "task_color_sym_1",
    85: "task_color_sym_2",
    86: "task_shape_rot_1",
    87: "task_shape_contact_2",
    88: "task_rot_contact_1",
    89: "task_rot_contact_2",
    90: "task_inside_sym_mir",
    91: "task_flip_count_1",
    92: "task_flip_inside_1",
    93: "task_flip_inside_2",
    94: "task_flip_color_1",
    95: "task_shape_flip_1",
    96: "task_rot_flip_1",
    97: "task_size_flip_1",
    98: "task_pos_rot_3",
    99: "task_pos_flip_1",
    100: "task_pos_flip_2",
    101: "task_flip_contact_1",
    102: "task_flip_contact_2",    

    103: "task_size_rot_2",
    104: "task_rot_inside_3",
    105: "task_flip_inside_3",
}

COMP_TO_ELEM = {
    49: [0,1], # "task_pos_shape_1"
    56: [0,2], # "task_size_shape_1"
    63: [0,3], # "task_shape_color"
    86: [0,4], # "task_shape_rot_1"
    95: [0,5], # "task_shape_flip_1"
    68: [0,6], # "task_shape_count_1"
    66: [0,7], # "task_shape_inside"
    20: [0,8], # "task_shape_contact_2"

    # 87: [0,8],
    47: [1,2], # "task_pos_size_1"
    53: [1,3], # "task_pos_col_1"
    51: [1,4], # "task_pos_rot_1"
    # 98: [1,4],
    99: [1,5], # "task_pos_flip_1"
    13: [1,6], # "task_pos_count_2"
    24: [1,7], # "task_pos_inside_3"
    55: [1,8], # "task_pos_contact"

    82: [2,3], # "task_size_color_1"
    103: [2,4], # "task_size_rot_2" # was previously 58: "task_size_rot"
    97: [2,5], # "task_size_flip_1"
    61: [2,6], # "task_size_count_1"
    59: [2,7], # "task_size_inside_1"
    60: [2,8], # "task_size_contact"

    70: [3,4], # "task_rot_color"
    94: [3,5], # "task_flip_color_1"
    77: [3,6], # "task_color_count_1"
    74: [3,7], # "task_color_inside_1"
    76: [3,8], # "task_color_contact"

    96: [4,5], # "task_rot_flip_1"
    73: [4,6], # "task_rot_count_1"
    104: [4,7], # 104 "task_rot_inside_3" # was previously 71:"task_rot_inside_1"
    88: [4,8], # "task_rot_contact_1"

    91: [5,6], # "task_flip_count_1" 
    105: [5,7], # "task_flip_inside_3" # was previously 92: "task_flip_inside_1"
    101: [5,8],# "task_flip_contact_1"

    17: [6,7], # "task_inside_count_1"
    80: [6,8], # "task_contact_count_1"
    79: [7,8], # "task_inside_contact"

}

elem_comp = {'{}-{}'.format(*v):k for k,v in COMP_TO_ELEM.items()}

#### fix after discussion with thomas and julien
trials = [
    [[1, 2], [0, 3]], # pos_size vs shape_color
    [[0, 3], [1, 2]], 
]
    # [[2, 6], [0, 3]], # size_count vs shape_color
    # [[0, 3], [2, 6]], 


conv_elem = {i:i for i in range(9)}

# -> set as 'train' 'test ab' 'test ac' 'test bd' 'test ef'
trials_ = {}
for i in range(len(trials)):
    a,b = trials[i][0]

    trials_[i] = {'train': [conv_elem[a], conv_elem[b]]}
    
    trials_[i]['test_ab'] = elem_comp['{}-{}'.format(conv_elem[a], conv_elem[b])]

    e,f = trials[i][1]
    trials_[i]['test_cd'] = elem_comp['{}-{}'.format(conv_elem[e], conv_elem[f])]

trial_combinations = trials_

# seq_elements = ['test_ab', 'test_ac', 'test_bd', 'test_ef']
seq_elements = ['test_ab', 'test_cd']

trial_sequence =[
    [0, 0, 1], # 0, 
    [0, 1, 0], # 0, 
    [1, 0, 1], # 1, 
    [1, 1, 0], # 1, 
]
# 

def prepare_experiment(p_idx, pilote=False, elem=True):
    # if pilote:
    #     if p_idx in pilote_idx_cond_fix:
    #         return prepare_experiment_pilote_fix(p_idx, elem)
    #     else:
    #         return prepare_experiment_pilote(p_idx, elem)
    # else:
    #     return prepare_experiment_main(p_idx)
    
    return prepare_experiment_main(p_idx)

def prepare_experiment_main(p_idx):

    # if p_idx > N_CONDITIONS:
    #     p_idx = p_idx % N_CONDITIONS
    
    # ---------------------------------------------------------------------------------------------------------------------------- don't forget to change this 
    n_trials = [10, 10, 20, 20]

    trial_combs = copy.deepcopy(trial_combinations)
    trial_seq_idx = p_idx // len(trial_combs)
    trial_idx = p_idx % len(trial_combs)
    trial_seq_idx_all = trial_sequence[trial_seq_idx][1:]
    p_ab = trial_sequence[trial_seq_idx][0]
    trial_seq = [seq_elements[i] for i in trial_sequence[trial_seq_idx][1:]]
    trial = trial_combs[trial_idx]
    
    # print(trial)

    tasks = trial['train']
    task_perm = [0, 1]
    task_perm_name = ['a', 'b']
    if p_ab == 1:
        tasks = [tasks[1], tasks[0]]
        task_perm = [1, 0]
        task_perm_name = ['b', 'a']
    
    # a_ = ['ab', 'ac', 'bd', 'ef']
    a_ = ['ab', 'cd']
    task_perm_name += [a_[ts] for ts in trial_seq_idx_all]
    task_perm += [ts+2 for ts in trial_seq_idx_all]
    tasks += [trial[trial_seq[0]], trial[trial_seq[1]]]
    
    tasks_names = [TASKS_NAMES[t] for t in tasks]
    
    return trial_idx, trial_seq_idx, task_perm, task_perm_name, tasks, tasks_names, n_trials


# how to avoid interference between trials ? 
# experiments are registered with workerID
# the experiment chosen is that with the minimum number of occurances and first in order
# def unqueue_experiment(exp_db, pilote=False):
#     pass

def unqueue_experiment(exp_db, pilote=False):
    all_sessions = os.listdir(exp_db)
    all_conditions = [int(l.split('_')[0]) for l in all_sessions]
    # # condition = np.zeros(N_CONDITIONS)
    # if pilote:
    #     condition_counts = [0]*(N_CONDITIONS_PILOTE)
    #     # n_unique_conditions = len(trial_pilote_combinations)
    # else:
    #     condition_counts = [0]*(N_CONDITIONS)
    #     # n_unique_conditions = len(trial_combinations)
  
    condition_counts = [0]*(N_CONDITIONS)
    

    for c in all_conditions:
        # if c < n_unique_conditions:
        condition_counts[c] += 1
    exp_idx = condition_counts.index(min(condition_counts))
    return exp_idx, condition_counts[exp_idx]



N_CONDITIONS = len(trial_combinations) * len(trial_sequence)
# N_CONDITIONS_PILOTE = len(trial_pilote_combinations) * len(trial_sequence_pilote)


# def test_unqueue():
#     # print(N_CONDITIONS_PILOTE)
#     print(N_CONDITIONS)
#     exp_db = '../user_data/exp_db_p'
#     # for pilote in [False, True]:
#     for pilote in [True]:
#         for _ in range(36):
#             exp_idx, j = unqueue_experiment(exp_db, pilote=pilote)
#             trial_idx, trial_seq_idx, task_perm, task_perm_name, tasks, tasks_names, n_trials = prepare_experiment(exp_idx, pilote=pilote, elem=True)
#             print(exp_idx, j, trial_idx, trial_seq_idx, task_perm, task_perm_name, tasks, tasks_names, n_trials)
#             with open(exp_db + '/{}_{}'.format(exp_idx, j), 'w') as f:
#                 f.write('x')
#             # exp_idx, i

# test_unqueue()

# import json
# with open("/home/aimen/projects/nivturk/services/web/user_data/data_p/qbrgjkxu59n2uv3ntcrzon0s_0.json", 'r') as f:
#     d = json.load(f)

