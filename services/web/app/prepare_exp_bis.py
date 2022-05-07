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

# do not put [0,x] where [5, x] or [4, x] are the first relation
# change flip and rotation tasks to use only flips and rotations but not shape
trials = [
    [[0, 1], [0, 8], [1, 2], [3, 4], [3, 4, 5, 6, 7]], 
    [[0, 2], [0, 1], [2, 8], [5, 6], [3, 4, 5, 6, 7]], 
    [[0, 3], [0, 2], [1, 3], [5, 7], [4, 5, 6, 7, 8]], 
    [[0, 4], [0, 3], [4, 8], [1, 5], [1, 2, 5, 6, 7]], 
    [[0, 5], [0, 4], [1, 5], [7, 8], [2, 3, 6, 7, 8]], 
    [[0, 6], [0, 5], [6, 8], [4, 7], [1, 2, 3, 4, 7]], 
    [[0, 7], [0, 6], [1, 7], [2, 3], [2, 3, 4, 5, 8]], 
    [[0, 8], [0, 7], [2, 8], [1, 6], [1, 3, 4, 5, 6]], 
    [[1, 2], [0, 1], [2, 5], [3, 7], [3, 4, 6, 7, 8]], 
    [[1, 3], [1, 4], [2, 3], [6, 7], [0, 5, 6, 7, 8]], 
    [[1, 4], [1, 5], [0, 4], [3, 8], [2, 3, 6, 7, 8]], 
    [[1, 5], [1, 6], [0, 5], [4, 8], [2, 3, 4, 7, 8]], 
    [[1, 6], [1, 7], [0, 6], [4, 5], [2, 3, 4, 5, 8]], 
    [[1, 7], [1, 8], [2, 7], [0, 3], [0, 3, 4, 5, 6]], 
    [[1, 8], [1, 2], [0, 8], [4, 6], [3, 4, 5, 6, 7]], 
    [[2, 3], [0, 2], [3, 4], [1, 7], [1, 5, 6, 7, 8]], 
    [[2, 4], [2, 3], [1, 4], [0, 6], [0, 5, 6, 7, 8]], 
    [[2, 5], [2, 4], [3, 5], [0, 1], [0, 1, 6, 7, 8]], 
    [[2, 6], [2, 5], [1, 6], [0, 4], [0, 3, 4, 7, 8]], 
    [[2, 7], [2, 6], [3, 7], [0, 5], [0, 1, 4, 5, 8]], 
    [[2, 8], [2, 7], [1, 8], [3, 6], [0, 3, 4, 5, 6]], 
    [[3, 4], [3, 5], [2, 4], [6, 8], [0, 1, 6, 7, 8]], 
    [[3, 5], [1, 3], [4, 5], [0, 7], [0, 2, 6, 7, 8]], 
    [[3, 6], [3, 7], [2, 6], [0, 8], [0, 1, 4, 5, 8]], 
    [[3, 7], [0, 3], [4, 7], [5, 8], [1, 2, 5, 6, 8]], 
    [[3, 8], [3, 4], [7, 8], [2, 5], [0, 1, 2, 5, 6]], 
    [[4, 5], [4, 8], [5, 6], [2, 7], [0, 1, 2, 3, 7]], 
    [[4, 6], [4, 5], [3, 6], [2, 8], [0, 1, 2, 7, 8]], 
    [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    [[4, 8], [4, 7], [3, 8], [2, 6], [0, 1, 2, 5, 6]], 
    [[5, 6], [5, 7], [4, 6], [1, 3], [0, 1, 2, 3, 8]], 
    [[5, 7], [5, 8], [6, 7], [1, 4], [0, 1, 2, 3, 4]], 
    [[5, 8], [5, 6], [3, 8], [2, 4], [0, 1, 2, 4, 7]], 
    [[6, 7], [3, 6], [7, 8], [1, 2], [0, 1, 2, 4, 5]], 
    [[6, 8], [6, 7], [5, 8], [0, 2], [0, 1, 2, 3, 4]], 
    [[7, 8], [0, 7], [6, 8], [3, 5], [1, 2, 3, 4, 5]],
]


# elem=True
trials_pilot = [ # similar to the original setup
    [[0, 1], [0, 8], [1, 2], [3, 4], [3, 4, 5, 6, 7]], 
    [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
    [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    [[0, 3], [0, 2], [1, 4], [6, 7], [4, 5, 6, 7, 8]],
    [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    [[6, 8], [2, 6], [3, 8], [0, 7], [0, 1, 2, 3, 4]], 
    [[3, 7], [3, 6], [2, 7], [1, 5], [0, 1, 4, 5, 8]], 
]

#### fix after discussion with thomas and julien
trials_pilot = [ 
    [[2, 6], [0, 3]], # size_count vs shape_color
    [[0, 3], [2, 6]], 

    [[1, 2], [0, 3]], # pos_size vs shape_color
    [[0, 3], [1, 2]], 

    # 3, 6
]

# issue with this: a task available as ab isn't available as ac bd or ef
# what's the fix ? make 15 conditions where this is the case

# trials_pilot = [ # no elementary task repeats
#     [[1, 2], [3, 4], [5, 6], [7, 8]],
#     [[0, 2], [3, 8], [4, 5], [6, 7]],
#     [[0, 3], [1, 8], [4, 6], [5, 7]],
#     [[0, 5], [1, 6], [2, 7], [4, 8]],
#     [[0, 7], [2, 8], [3, 6], [1, 5]],
#     [[0, 1], [2, 3], [4, 7], [6, 8]],
#     [[0, 8], [1, 7], [2, 4], [3, 5]], 
#     [[0, 4], [1, 3], [5, 8], [2, 6]],
#     [[0, 6], [3, 7], [2, 5], [1, 4]],
# ]

# [1, 2] | [3, 4] | [5, 6] | [7, 8]
# [0, 2] | [3, 8] | [4, 5] | [6, 7]
# [0, 3] | [1, 8] | [4, 6] | [5, 7]
# [0, 5] | [1, 6] | [2, 7] | [4, 8]
# [0, 7] | [2, 8] | [3, 6] | [1, 5]
# [0, 1] | [2, 3] | [4, 7] | [6, 8]
# [0, 8] | [1, 7] | [2, 4] | [3, 5] 
# [0, 4] | [1, 3] | [5, 8] | [2, 6]
# [0, 6] | [3, 7] | [2, 5] | [1, 4]

# elem=False
# trials_pilot = [ # no elementary task repeats + shuffled
#     [[7, 8], [5, 6], [1, 2], [3, 4]], 
#     [[3, 8], [6, 7], [4, 5], [0, 2]], 
#     [[4, 6], [1, 8], [0, 3], [5, 7]], 
#     [[2, 7], [1, 6], [0, 5], [4, 8]], 
#     [[1, 5], [3, 6], [2, 8], [0, 7]], 
#     [[4, 7], [0, 1], [6, 8], [2, 3]], 
#     [[2, 4], [1, 7], [0, 8], [3, 5]], 
#     [[1, 3], [5, 8], [2, 6], [0, 4]], 
#     [[3, 7], [0, 6], [1, 4], [2, 5]]
# ]


conv_elem = {i:i for i in range(9)}

# -> set as 'train' 'test ab' 'test ac' 'test bd' 'test ef'
trials_ = {}
for i in range(len(trials)):
    a,b = trials[i][0]

    trials_[i] = {'train': [conv_elem[a], conv_elem[b]]}
    
    trials_[i]['test_ab'] = elem_comp['{}-{}'.format(conv_elem[a], conv_elem[b])]

    a,c = trials[i][1]
    trials_[i]['test_ac'] = elem_comp['{}-{}'.format(conv_elem[a], conv_elem[c])]

    b,d = trials[i][2]
    trials_[i]['test_bd'] = elem_comp['{}-{}'.format(conv_elem[b], conv_elem[d])]

    e,f = trials[i][3]
    trials_[i]['test_ef'] = elem_comp['{}-{}'.format(conv_elem[e], conv_elem[f])]

trial_combinations = trials_

seq_elements = ['test_ab', 'test_ac', 'test_bd', 'test_ef']

trial_sequence =[
    [0, 1, 2, 3],
    [0, 1, 3, 2],
    [0, 3, 1, 2],
    [3, 1, 2, 0],
    [3, 1, 0, 2],
    [3, 0, 1, 2],
    [1, 3, 2, 0],
    [1, 3, 0, 2],
    [1, 0, 3, 2],
    [1, 0, 2, 3],
]


trials_pilote_ = {}
for i in range(len(trials_pilot)):
    a,b = trials_pilot[i][0]

    trials_pilote_[i] = {'train': [conv_elem[a], conv_elem[b]]}
    
    trials_pilote_[i]['test_ab'] = elem_comp['{}-{}'.format(conv_elem[a], conv_elem[b])]

    a,c = trials_pilot[i][1]
    trials_pilote_[i]['test_ac'] = elem_comp['{}-{}'.format(conv_elem[a], conv_elem[c])]

    b,d = trials_pilot[i][2]
    trials_pilote_[i]['test_bd'] = elem_comp['{}-{}'.format(conv_elem[b], conv_elem[d])]

    e,f = trials_pilot[i][3]
    trials_pilote_[i]['test_ef'] = elem_comp['{}-{}'.format(conv_elem[e], conv_elem[f])]

trial_pilote_combinations = trials_pilote_


seq_elements_pilote = ['test_ab', 'test_ac', 'test_bd', 'test_ef']

# elem=True
trial_sequence_pilote =[
    [0, 1, 3, 2],
    [3, 2, 0, 1],
    [1, 0, 2, 3],
    [2, 3, 1, 0],
]

# # elem=False
# trial_sequence_pilote =[
#     [0, 1, 2, 3],
#     [3, 2, 1, 0],
#     [1, 0, 3, 2],
#     [1, 3, 0, 1],
# ]


# pilote_idx_cond_fix = [5, 10, 11, 12, 14, 15, 18, 21, 24, 28, 29, 30, 31, 32, 33, 34] 

trials_pilot_fix = [
    [[3, 4], [3, 5], [2, 4], [1, 6]],
    [[7, 8], [5, 8], [1, 7], [0, 4]],
    [[1, 7], [1, 6], [7, 8], [0, 5]],
    [[2, 5], [2, 3], [0, 5], [1, 7]],
    [[6, 7], [1, 6], [4, 7], [0, 1]],
    [[2, 8], [2, 3], [1, 8], [0, 6]],
    [[1, 4], [2, 4], [4, 8], [3, 5]], 
    [[4, 8], [5, 8], [2, 4], [0, 3]],
    [[1, 8], [1, 3], [0, 8], [5, 7]],
    [[0, 6], [0, 4], [5, 6], [1, 3]],
    [[0, 4], [0, 6], [4, 5], [2, 3]],        
    [[1, 2], [1, 3], [2, 5], [6, 8]],
    [[5, 8], [5, 6], [2, 8], [4, 7]], 
    [[5, 6], [5, 7], [4, 6], [4, 8]],
    [[0, 7], [0, 5], [7, 8], [0, 2]],
    [[4, 6], [4, 5], [2, 6], [3, 8]],
]

trials_pilote_fix_ = {}
for i in range(len(trials_pilot_fix)):
    a,b = trials_pilot_fix[i][0]

    trials_pilote_fix_[i] = {'train': [conv_elem[a], conv_elem[b]]}
    
    trials_pilote_fix_[i]['test_ab'] = elem_comp['{}-{}'.format(conv_elem[a], conv_elem[b])]

    a,c = trials_pilot_fix[i][1]
    trials_pilote_fix_[i]['test_ac'] = elem_comp['{}-{}'.format(conv_elem[a], conv_elem[c])]

    b,d = trials_pilot_fix[i][2]
    trials_pilote_fix_[i]['test_bd'] = elem_comp['{}-{}'.format(conv_elem[b], conv_elem[d])]

    e,f = trials_pilot_fix[i][3]
    trials_pilote_fix_[i]['test_ef'] = elem_comp['{}-{}'.format(conv_elem[e], conv_elem[f])]

trial_pilote_combinations_fix = trials_pilote_fix_


seq_elements_pilote = ['test_ab', 'test_ac', 'test_bd', 'test_ef']


trial_sequence_pilote_fix =[
    [0, 1, 3, 2],
    [3, 2, 0, 1],
    [3, 2, 0, 1],
    [3, 2, 0, 1],
    [3, 2, 0, 1],
    [3, 2, 0, 1],
    [1, 0, 2, 3],
    [1, 0, 2, 3],
    [1, 0, 2, 3],
    [2, 3, 1, 0],
    [2, 3, 1, 0],
    [2, 3, 1, 0],
    [2, 3, 1, 0],
    [2, 3, 1, 0],
    [2, 3, 1, 0],
    [2, 3, 1, 0],
]


def prepare_experiment(p_idx, pilote=False, elem=True):

    if pilote:
        if p_idx in pilote_idx_cond_fix:
            return prepare_experiment_pilote_fix(p_idx, elem)
        else:
            return prepare_experiment_pilote(p_idx, elem)
    else:
        return prepare_experiment_main(p_idx)

def prepare_experiment_main(p_idx):

    # if p_idx > N_CONDITIONS:
    #     p_idx = p_idx % N_CONDITIONS
    
    # ---------------------------------------------------------------------------------------------------------------------------- don't forget to change this 
    n_trials = 20

    trial_combs = copy.deepcopy(trial_combinations)
    trial_seq_idx = p_idx // len(trial_combs)
    trial_idx = p_idx % len(trial_combs)
    trial_seq_idx_all = trial_sequence[trial_seq_idx]
    trial_seq = [seq_elements[i] for i in trial_sequence[trial_seq_idx]]
    trial = trial_combs[trial_idx]
    
    tasks = trial['train']
    task_perm = [0, 1]
    task_perm_name = ['a', 'b']
    if trial_seq_idx%2 == 1:
        tasks = [tasks[1], tasks[0]]
        task_perm = [1, 0]
        task_perm_name = ['b', 'a']
    a_ = ['ab', 'ac', 'bd', 'ef']
    task_perm_name += [a_[ts] for ts in trial_seq_idx_all]
    task_perm += [ts+2 for ts in trial_seq_idx_all]
    tasks += [trial[trial_seq[0]], trial[trial_seq[1]], trial[trial_seq[2]], trial[trial_seq[3]]]
    
    tasks_names = [TASKS_NAMES[t] for t in tasks]
    
    return trial_idx, trial_seq_idx, task_perm, task_perm_name, tasks, tasks_names, n_trials

def prepare_experiment_pilote(p_idx, elem=False):

    # if p_idx > N_CONDITIONS_PILOTE:
    #     p_idx = p_idx % N_CONDITIONS_PILOTE

    # ---------------------------------------------------------------------------------------------------------------------------- don't forget to change this 
    n_trials = 20
    
    trial_combs = copy.deepcopy(trial_pilote_combinations)
    trial_seq_idx = p_idx // len(trial_combs)
    trial_idx = p_idx % len(trial_combs)
    trial_seq_idx_all = trial_sequence_pilote[trial_seq_idx]
    trial_seq = [seq_elements_pilote[i] for i in trial_sequence_pilote[trial_seq_idx]]
    trial = trial_combs[trial_idx]
    
    tasks = trial['train'] if elem else []
    task_perm = [0, 1]
    task_perm_name = ['a', 'b']
    if trial_seq_idx%2 == 1:
        tasks = [tasks[1], tasks[0]]
        task_perm = [1, 0]
        task_perm_name = ['b', 'a']
    a_ = ['ab', 'ac', 'bd', 'ef']
    task_perm_name += [a_[ts] for ts in trial_seq_idx_all]
    
    task_perm += [ts+2 for ts in trial_seq_idx_all]
    tasks += [trial[trial_seq[0]], trial[trial_seq[1]], trial[trial_seq[2]], trial[trial_seq[3]]]
    
    tasks_names = [TASKS_NAMES[t] for t in tasks]
    
    return trial_idx, trial_seq_idx, task_perm, task_perm_name, tasks, tasks_names, n_trials

pilote_idx_cond_fix = [5, 10, 11, 12, 14, 15, 18, 21, 24, 28, 29, 30, 31, 32, 33, 34] 

def prepare_experiment_pilote_fix(p_idx, elem=False):

    # if p_idx > N_CONDITIONS_PILOTE:
    #     p_idx = p_idx % N_CONDITIONS_PILOTE

    # ---------------------------------------------------------------------------------------------------------------------------- don't forget to change this 
    n_trials = 20
        
    trial_combs = copy.deepcopy(trial_pilote_combinations_fix)
    # trial_seq_idx = p_idx // len(trial_combs)
    # trial_idx = p_idx % len(trial_combs)
    trial_seq_idx = pilote_idx_cond_fix.index(p_idx)
    trial_idx = pilote_idx_cond_fix.index(p_idx)

    trial_seq_idx_all = trial_sequence_pilote_fix[trial_seq_idx]
    trial_seq = [seq_elements_pilote[i] for i in trial_sequence_pilote_fix[trial_seq_idx]]
    trial = trial_combs[trial_idx]
    
    tasks = trial['train'] if elem else []
    task_perm = [0, 1]
    task_perm_name = ['a', 'b']
    if trial_seq_idx%2 == 1:
        tasks = [tasks[1], tasks[0]]
        task_perm = [1, 0]
        task_perm_name = ['b', 'a']
    a_ = ['ab', 'ac', 'bd', 'ef']
    task_perm_name += [a_[ts] for ts in trial_seq_idx_all]
    
    task_perm += [ts+2 for ts in trial_seq_idx_all]
    tasks += [trial[trial_seq[0]], trial[trial_seq[1]], trial[trial_seq[2]], trial[trial_seq[3]]]
    
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
    # condition = np.zeros(N_CONDITIONS)
    if pilote:
        condition_counts = [0]*(N_CONDITIONS_PILOTE)
        # n_unique_conditions = len(trial_pilote_combinations)
    else:
        condition_counts = [0]*(N_CONDITIONS)
        # n_unique_conditions = len(trial_combinations)
    

    for c in all_conditions:
        # if c < n_unique_conditions:
        condition_counts[c] += 1
    exp_idx = condition_counts.index(min(condition_counts))
    return exp_idx, condition_counts[exp_idx]



N_CONDITIONS = len(trial_combinations) * len(trial_sequence)
N_CONDITIONS_PILOTE = len(trial_pilote_combinations) * len(trial_sequence_pilote)


# def test_unqueue():
#     print(N_CONDITIONS_PILOTE)
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

# from PIL import Image
# import numpy as np
# images = [
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/00_0.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/00_1.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/00_2.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/00_3.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/01_0.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/01_1.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/01_2.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/01_3.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/02_0.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/02_1.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/02_2.png',
#     '/home/aimen/projects/nivturk/services/web/app/static/human_exp_images/practice_img/02_3.png',
# ]
# for im_path in images:
#     im = Image.open(im_path)
#     im = np.array(im)
#     a = im[:,:,3]
#     a[a>0] = 255
#     im[:,:,:3] = a[:,:,None]
#     im = im[:,:,:3]
#     im = im/255
#     im = im /im.max()
#     im = 1-im
#     im = (im*255).astype(np.uint8)
#     im = Image.fromarray(im)
#     im.save(im_path)

    # im = Image.fromarray(im[:,:,:3])




# current conditions pilot

    # [[0, 1], [0, 8], [1, 2], [3, 4], [3, 4, 5, 6, 7]], 
    # [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    # [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [[0, 3], [0, 2], [1, 4], [6, 7], [4, 5, 6, 7, 8]],
    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [[6, 8], [2, 6], [3, 8], [0, 7], [0, 1, 2, 3, 4]], 
    # [[3, 7], [3, 6], [2, 7], [1, 5], [0, 1, 4, 5, 8]], 
    # [[0, 1], [0, 8], [1, 2], [3, 4], [3, 4, 5, 6, 7]], 
    # [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    # [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [[0, 3], [0, 2], [1, 4], [6, 7], [4, 5, 6, 7, 8]],
    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [[6, 8], [2, 6], [3, 8], [0, 7], [0, 1, 2, 3, 4]], 
    # [[3, 7], [3, 6], [2, 7], [1, 5], [0, 1, 4, 5, 8]], 
    # [[0, 1], [0, 8], [1, 2], [3, 4], [3, 4, 5, 6, 7]], 
    # [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    # [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [[0, 3], [0, 2], [1, 4], [6, 7], [4, 5, 6, 7, 8]],
    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [[6, 8], [2, 6], [3, 8], [0, 7], [0, 1, 2, 3, 4]], 
    # [[3, 7], [3, 6], [2, 7], [1, 5], [0, 1, 4, 5, 8]], 
    # [[0, 1], [0, 8], [1, 2], [3, 4], [3, 4, 5, 6, 7]], 
    # [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    # [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [[0, 3], [0, 2], [1, 4], [6, 7], [4, 5, 6, 7, 8]],
    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [[6, 8], [2, 6], [3, 8], [0, 7], [0, 1, 2, 3, 4]], 
    # [[3, 7], [3, 6], [2, 7], [1, 5], [0, 1, 4, 5, 8]], 

###################################################

# 0 0
# 1
# 2
# 3
# 4 4
# 6
# 7
# 8
# 9
# 13
# 16
# 17
# 19
# 20
# 22
# 23
# 25
# 26
# 27
# 35
# sum -> 20



###################################################

# 5 
    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [0, 1, 3, 2],
# 10 
    # [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    # [3, 2, 0, 1],
# 11 
    # [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
    # [3, 2, 0, 1],
# 12 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [3, 2, 0, 1],
# 14 
    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [3, 2, 0, 1],
# 15 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [3, 2, 0, 1],
# 18 
    # [[0, 1], [0, 8], [1, 2], [3, 4], [3, 4, 5, 6, 7]], 
    # [1, 0, 2, 3],
# 21 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [1, 0, 2, 3],
# 24 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [1, 0, 2, 3],
# 28
    # [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    # [2, 3, 1, 0],
# 29 
    # [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
    # [2, 3, 1, 0],
# 30 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [2, 3, 1, 0],
# 31 
    # [[0, 3], [0, 2], [1, 4], [6, 7], [4, 5, 6, 7, 8]],
    # [2, 3, 1, 0],
# 32 
    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [2, 3, 1, 0],
# 33 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [2, 3, 1, 0],
# 34 
    # [[6, 8], [2, 6], [3, 8], [0, 7], [0, 1, 2, 3, 4]], 
    # [2, 3, 1, 0],


###################

    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    # [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [[0, 1], [0, 8], [1, 2], [3, 4], [3, 4, 5, 6, 7]], 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [[4, 7], [4, 6], [5, 7], [1, 8], [0, 1, 2, 3, 8]], 
    # [[3, 5], [1, 3], [4, 5], [2, 8], [0, 2, 6, 7, 8]], 
    # [[0, 5], [0, 4], [2, 5], [7, 8], [2, 3, 6, 7, 8]], 
    # [[0, 3], [0, 2], [1, 4], [6, 7], [4, 5, 6, 7, 8]],
    # [[1, 6], [1, 7], [0, 6], [5, 8], [2, 3, 4, 5, 8]], 
    # [[2, 4], [2, 3], [4, 8], [5, 6], [0, 5, 6, 7, 8]],  
    # [[6, 8], [2, 6], [3, 8], [0, 7], [0, 1, 2, 3, 4]], 


# 15 conditions


#################################################################
# pos shape

### (ab, ac/bd) -> easier
### too difficult 
# 24 ac     pos_inside_3
# 73 ac     rot_count
# 88 ac     rot_contact
# 94 ab     flip_color
# 103 ab    size_rot

### (ab, ac/bd) -> easier
### mildly difficulty
# 55 ef     pos_contact
# 60 ef     size_contact
# 82 ac     size_color

### (ab) -> easier (ef) -> more difficult
### just good
# 13 ab     pos_count
# 20 ac/bd  shape_contact
# 47 ac/bd  pos_size
# 49 ab     pos_shape
# 53 ac     pos_col
# 56 ac     size_shape
# 61 ac     size_count
# 63 ab     shape_color
# 77 ac     color_count
# 91 ef     flip_count
# 96 bd     rot_flip
# 99 ef     pos_flip
# 101 ef    flip_contact
# 104 ab    rot_inside
# 105 bd    flip_inside

# 47 ac/bd  pos_size
# 56 ac     size_shape
# 61 ac     size_count
# 63 ab     shape_color
# 77 ac     color_count
# 99 ef     pos_flip

# pos_size shape_color
# pos_size color_count

# size_shape color_count
# size_shape pos_flip

# size_count shape_color
# size_count pos_flip

# shape_color pos_flip

# color_count pos_flip


### (ef, ac/bd) -> more difficult
### mildly easy
# 17 ef     inside_count
# 59 ac/bd  size_inside
# 66 ef     shape_inside
# 68 ac     shape_count
# 70 ef     rot_color
# 76 ac     color_contact
# 95 ab     shape_flip
# 97 bd     size_flip

### (ef, ac/bd) -> more difficult
### too easy
# 51 ac/bd  pos_rot
# 74 ab     color_inside
# 79 ef     inside_contact
# 80 ab     contact_count
# 86 ac     shape_rot

###################

###### AB tasks that are too difficult
### priority
# 94 ab     flip_color DONE -> regen
# 103 ab    size_rot DONE -> regen
### if possible
# 24 ac     pos_inside_3
# 73 ac     rot_count
# 82 ac     size_color
# 88 ac     rot_contact
### optional
# 13 ab     pos_count
# 49 ab     pos_shape
# 63 ab     shape_color
# 104 ab    rot_inside


###### EF tasks that are too easy
### priority
# 79 ef     inside_contact DONE -> regen
# 51 ac/bd  pos_rot DONE -> regen
# 86 ac     shape_rot DONE -> regen
### if possible
# 17 ef     inside_count DONE-> regen
# 59 ac/bd  size_inside
# 66 ef     shape_inside DONE-> regen (and replace in prepare_exp.py)
# 68 ac     shape_count
# 70 ef     rot_color TODO
# 76 ac     color_contact
# 97 bd     size_flip
### optional
# 91 ef     flip_count
# 99 ef     pos_flip
# 101 ef    flip_contact


#################################################################
# ensure each task appears once as AB and once as CD

    # [[0, 1], [3, 4]], 
    # [[0, 1], [3, 4]], 
    # [[0, 1], [3, 4]], 

    # [[4, 7], [1, 8]], 
    # [[4, 7], [1, 8]], 

    # [[6, 8], [0, 7]], 
    # [[6, 8], [0, 7]], 
    # [[6, 8], [0, 7]], 

    # [[3, 5], [2, 8]], 
    # [[3, 5], [2, 8]], 

    # [[0, 3], [6, 7]],
    # [[0, 3], [6, 7]],
    # [[0, 3], [6, 7]],

    # [[0, 5], [7, 8]], 

    # [[3, 7], [1, 5]], 
    # [[3, 7], [1, 5]], 

    # [[2, 4], [5, 6]],  

    # [[1, 6], [5, 8]], 










################################
# possibility 1
# do less experiments A, B, AB, CD

# conditions DONE
    # [[0, 1], [3, 4]], 3
    # [[4, 7], [1, 8]], 2
    # [[6, 8], [0, 7]], 3
    # [[3, 5], [2, 8]], 2
    # [[0, 3], [6, 7]], 3
    # [[0, 5], [7, 8]], 1
    # [[3, 7], [1, 5]], 2
    # [[2, 4], [5, 6]], 1
    # [[1, 6], [5, 8]], 1

# conditions TODO 25 AB CD, 15 minutes total = 87.5 $
# reduce A and B time to 10 trials (5 minutes less = 5.83 $)

    # A, B, AB, CD

    #   A  B    C  D

    # [[0, 1], [3, 4]], 3
    # [[4, 7], [1, 8]], 2
    # [[6, 8], [0, 7]], 3
    # [[3, 5], [2, 8]], 2
    # [[0, 3], [6, 7]], 3
    # [[0, 5], [7, 8]], 1
    # [[3, 7], [1, 5]], 2
    # [[2, 4], [5, 6]], 1
    # [[1, 6], [5, 8]], 1

    # [[7, 8], [5, 7]], 
    # [[2, 5], [4, 8]],
    # [[1, 7], [4, 5]],
    # [[1, 8], [3, 7]],
    # [[5, 8], [1, 3]],
    # [[0, 2], [1, 7]]
    # [[3, 8], [1, 2]],
    # [[0, 4], [2, 3]], 
    # [[2, 6], [1, 4]], 
    # [[3, 4], [1, 6]]
    # [[0, 8], [2, 5]],
    # [[1, 5], [4, 7]],
    # [[2, 3], [0, 5]],
    # [[6, 7], [0, 1]],
    # [[2, 8], [0, 6]],
    # [[0, 6], [2, 4]],
    # [[1, 4], [3, 5]], 
    # [[4, 8], [0, 3]],
    # [[5, 7], [4, 6]],
    # [[4, 6], [3, 8]],
    # [[1, 3], [0, 8]],
    # [[5, 6], [0, 4]],
    # [[4, 5], [2, 6]],
    # [[1, 2], [6, 8]],
    # [[0, 7], [0, 2]],

################################
# possibility 2
# do less experiments A, B, AB, CD
# reduce A and B time to 10 trials (15 minutes = 5.83 $)
# and take new changes into account:

# conditions TODO 36 AB CD, 15 minutes total = 126 $

################################
# possibility 3
# finish the 16 conditions left from AB AC BD EF total = 112 $
# reduce A and B time to 10 trials (25 minutes = 5.83 $) = 93$

################################
# possibility 4
# reduce the number of elementary tasks (would like to avoid)
# if this is chosen remove flip 36-8 relations = 28

# 28 conditions AB CD = 98 $ # once
# 28 conditions AB EF = 197 $


# finish the 16 conditions left from AB AC BD EF total = 112 $
# reduce A and B time to 10 trials (25 minutes = 5.83 $) = 93$


################################


    # [[1, 6], [7, 8]], 
    # [[2, 5], [1, 7]],
    # [[2, 3], [0, 5]],
    # [[6, 7], [0, 1]],
    # [[1, 6], [4, 7]],
    # [[2, 8], [0, 6]],
    # [[2, 3], [1, 8]],
    # [[1, 4], [3, 5]], 
    # [[2, 4], [4, 8]],
    # [[4, 8], [0, 3]],
    # [[5, 8], [2, 4]],
    # [[1, 8], [5, 7]],
    # [[1, 3], [0, 8]],
    # [[0, 6], [1, 3]],
    # [[0, 4], [5, 6]],
    # [[0, 4], [2, 3]], 
    # [[0, 6], [4, 5]],
    # [[1, 2], [6, 8]],
    # [[1, 3], [2, 5]],
    # [[5, 8], [4, 7]], 
    # [[5, 6], [2, 8]],
    # [[5, 6], [4, 8]],
    # [[5, 7], [4, 6]],
    # [[0, 7], [0, 2]],
    # [[0, 5], [7, 8]],
    # [[4, 6], [3, 8]],
    # [[4, 5], [2, 6]],


# [0, 1]
