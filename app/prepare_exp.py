import numpy as np
import os

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
    82: "",
    83: "",
    84: "",
    85: "",
    86: "",
    87: "",
    88: "",
    101: "task_shape_color",
    103: "task_shape_color_2",
    104: "task_shape_color_3",
    106: "task_shape_inside",
    107: "task_shape_inside_1",
    108: "task_shape_count_1",
    112: "task_shape_count_2",
    113: "task_rot_color",
    115: "task_rot_inside_1",
    116: "task_rot_inside_2",
    117: "task_rot_count_1",
    118: "task_color_inside_1",
    119: "task_color_inside_2",
    121: "task_color_contact",
    122: "task_color_count_1",
    123: "task_color_count_2",
    124: "task_inside_contact",
    125: "task_contact_count_1",
    126: "task_contact_count_2",
}


COMP_TO_ELEM = {
    # 19: [0],
    # 11: [1],
    # # 12: [1],
    # # 15: [1],
    # # 31: [1],
    # 33: [2],
    # # 34: [2],
    # # 35: [2],
    # # 36: [2],
    # # 37: [2],
    # 40: [3],
    # # 41: [3],
    # 28: [4],
    # # 29: [4],
    # # 30: [4],
    # 18: [6],
    # 22: [7],
    # # 23: [7],
    # 21: [8],
    # # 46: [8],
    # 43: [9],
    # 42: [10],
    49: [0,1],
    # 50: [0,1],
    56: [0,2],
    # 57: [0,2],
    63: [0,3],
    # 64: [0,3],
    # 65: [0,3],
    68: [0,6],
    # 69: [0,6],
    66: [0,7],
    # 67: [0,7],
    20: [0,8],
    # 44: [0,8],
    # 45: [0,8],
    47: [1,2],
    # 48: [1,2],
    53: [1,3],
    # 54: [1,3],
    51: [1,4],
    # 52: [1,4],
    13: [1,6],
    # 14: [1,6],
    # 16: [1,6],
    # 32: [1,6],
    24: [1,7],
    # 25: [1,7],
    # 26: [1,7],
    # 27: [1,7],
    55: [1,8],
    58: [2,4],
    61: [2,6],
    # 62: [2,6],
    59: [2,7],
    60: [2,8],
    # 39: [2,9],
    # 38: [2,10],
    70: [3,4],
    77: [3,6],
    # 78: [3,6],
    74: [3,7],
    # 75: [3,7],
    76: [3,8],
    73: [4,6],
    71: [4,7],
    # 72: [4,7],
    17: [6,7],
    80: [6,8],
    # 81: [6,8],
    79: [7,8],
    ################ Done
    
    82: [2,3],
    # 83: [2,3],
    # 84: [3,9],
    # 85: [3,10],
    86: [0,4],
    87: [0,8],
    88: [4,8],
    # 89: [4,8],
    # 90: [7,10],
    # 91: [5,6],
    92: [5,7],
    # 93: [5,7],
    94: [3,5],
    95: [0,5],
    96: [4,5],
    97: [2,5],
    98: [1,4],
    99: [1,5],
    # 100: [1,5],
    101: [5,8],
    # 102: [5,8], 

    ################ useless

    # 101: [0, 4],
    # # 102: [0, 5],
    # 103: [0, 9],
    # 104: [0, 10],
    # # 105: [1, 5],
    # 106: [1, 9],
    # 107: [1, 10],
    # 108: [2, 3],
    # # 109: [2, 5],
    # # 111: [3, 5],
    # 112: [3, 9],
    # 113: [3, 10],
    # # 114: [4, 5],
    # 115: [4, 8],
    # 116: [4, 9],
    # 117: [4, 10],
    # 118: [6, 8],
    # 119: [6, 9],
    # 121: [6, 10],
    # 122: [7, 9],
    # 123: [7, 10],
    # 124: [8, 9],
    # 125: [8, 10],
    # 126: [9, 10],
    # 127: [],
    # 128: [],
    # 129: [],
}

elem_comp = {'{}-{}'.format(*v):k for k,v in COMP_TO_ELEM.items()}

def elementary_to_comp(comp_to_elem):
    out = {
        0:  [],
        1:  [],
        2:  [],
        3:  [],
        4:  [],
        5:  [],
        6:  [],
        7:  [],
        8:  [],
        # 9:  [],
        # 10: [],
    }
    for k,v in COMP_TO_ELEM.items():
        for v_ in v:
            out[v_].append(k)
    return out

ELEM_TO_COMP = elementary_to_comp(COMP_TO_ELEM)

# for comp in COMP_TO_ELEM:
# unique_conditions = np.unique([sorted(v) for _,v in COMP_TO_ELEM.items()])
unique_conditions = [v for _,v in COMP_TO_ELEM.items()]

trials = []
n_elem_r = 10
from itertools import combinations
arrs = [np.delete(np.arange(n_elem_r), i).tolist() for i in range(n_elem_r)]
sign = [-1,1]
# keep 0, choose from arrs[a][arrs[a].index(b) + sign[a%2]]
# [0, 1], sorted([a, arrs[a][arrs[a].index(b) + sign[a%2]]]), sorted([b, arrs[b][arrs[b].index(a) + sign[b%2]]])
combs = [list(c) for c in combinations(np.arange(n_elem_r),2)]
trials = [
    [c, 
    sorted([c[0], arrs[c[0]][(arrs[c[0]].index(c[1]) + sign[c[0]%2])%(n_elem_r-1)]]), 
    sorted([c[1], arrs[c[1]][(arrs[c[1]].index(c[0]) + sign[c[1]%2])%(n_elem_r-1)]])
    ] for c in combs]

efs = [[3, 7],[5, 6],[5, 8],[1, 2],[2, 3],[4, 8],[2, 5],[1, 4],[2, 7],[6, 7],[0, 5],[6, 8],[0, 3],[3, 8],[4, 6],[3, 5],[7, 8],[6, 9],[7, 9],[0, 1],[4, 7],[0, 4],[3, 9],[0, 6],[8, 9],[0, 2],[1, 9],[1, 6],[1, 7],[5, 7],[1, 8],[2, 9],[0, 8],[5, 9],[0, 7],[2, 8],[0, 9],[3, 6],[2, 4],[4, 9],[1, 3],[1, 5],[3, 4],[2, 6],[4, 5]]

all_can = []
for i in range(len(trials)):
    # candidates = [c for c in combs if c[0] not in trials[i][0]+trials[i][1]+trials[i][2] and c[1] not in trials[i][0]+trials[i][1]+trials[i][2]]
    trials[i].append(efs[i])

print(trials)
##### -> retrieve task numbers from [a,b]

## temporary
conv_elem = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 6,
    6: 7,
    7: 8,
    8: 9,
    9: 10,
}

conv_elem = {i:i for i in range(10)}

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


print(len(trial_combinations))

def prepare_experiment(p_idx):

    n_trials = 3

    trial_seq_idx = p_idx // len(trial_combinations)
    trial_idx = p_idx % len(trial_combinations)
    
    trial_seq = [seq_elements[i] for i in trial_sequence[trial_seq_idx]]
    trial = trial_combinations[trial_idx]
    
    tasks = trial['train'] 
    tasks += [trial[trial_seq[0]], trial[trial_seq[1]], trial[trial_seq[2]], trial[trial_seq[3]]]
    tasks_names = [TASKS_NAMES[t] for t in tasks]
    
    return trial_idx, trial_seq_idx, tasks_names, n_trials

# how to avoid interference between trials ? 
# experiments are registered with workerID
# the experiment chosen is that with the minimum number of occurances and first in order
def unqueue_experiment(exp_db):
    all_sessions = os.listdir(exp_db)
    all_conditions = [int(l.split('_')[0]) for l in all_sessions]
    # condition = np.zeros(N_CONDITIONS)
    condition_counts = [0]*(N_CONDITIONS)
    for c in all_conditions:
        condition_counts[c] += 1
    exp_idx = condition_counts.index(min(condition_counts))
    return exp_idx, condition_counts[exp_idx]


N_CONDITIONS = len(trial_combinations) * len(trial_sequence)



# print(unqueue_experiment('../exp_db'))
# print(unqueue_experiment('exp_db'))

# print(prepare_experiment(10))

# for i in range(len(trials)):
#     print(list(set(trials[i][0] + trials[i][1] + trials[i][2])))
#     # print(all_can[i])

# combinations = {
#     1:  {'train': [0, 1],  'test_ab': [49, 50]},
#     2:  {'train': [0, 2],  'test_ab': [56, 57]},
#     3:  {'train': [0, 3],  'test_ab': [63, 64, 65]},
#     4:  {'train': [0, 6],  'test_ab': [68, 69]},
#     5:  {'train': [0, 7],  'test_ab': [66, 67]},
#     6:  {'train': [0, 8],  'test_ab': [20, 44, 45]},
#     7:  {'train': [1, 2],  'test_ab': [47, 48]},
#     8:  {'train': [1, 4],  'test_ab': [51, 52]},
#     9:  {'train': [1, 3],  'test_ab': [53, 54]},
#     10: {'train': [1, 6],  'test_ab': [13, 14, 16, 32]},
#     11: {'train': [1, 7],  'test_ab': [24, 25, 26, 27]},
#     12: {'train': [1, 8],  'test_ab': [55]},
#     13: {'train': [2, 4],  'test_ab': [58]},
#     14: {'train': [2, 6],  'test_ab': [61, 62]},
#     15: {'train': [2, 7],  'test_ab': [59]},
#     16: {'train': [2, 8],  'test_ab': [60]},
#     17: {'train': [2, 9],  'test_ab': [39]},
#     18: {'train': [2, 10], 'test_ab': [38]},
#     19: {'train': [3, 4],  'test_ab': [70]},
#     20: {'train': [3, 6],  'test_ab': [77, 78]},
#     21: {'train': [3, 7],  'test_ab': [74, 75]},
#     22: {'train': [3, 8],  'test_ab': [76]},
#     23: {'train': [4, 6],  'test_ab': [73]},
#     24: {'train': [4, 7],  'test_ab': [71, 72]},
#     25: {'train': [6, 7],  'test_ab': [17]},
#     26: {'train': [6, 8],  'test_ab': [80, 81]},
#     27: {'train': [7, 8],  'test_ab': [79]},
# }


combinations = {
    0:  {'train': [0, 1],  'test_ab': [49, 50]},
    1:  {'train': [0, 2],  'test_ab': [56, 57]},
    2:  {'train': [0, 3],  'test_ab': [63, 64, 65]},
    3:  {'train': [0, 4],  'test_ab': [83]},
    4:  {'train': [0, 5],  'test_ab': [95]},
    5:  {'train': [0, 6],  'test_ab': [68, 69]},
    6:  {'train': [0, 7],  'test_ab': [66, 67, 99]},
    7:  {'train': [0, 8],  'test_ab': [20, 44, 45]},
    8:  {'train': [1, 2],  'test_ab': [47, 48]},
    9:  {'train': [1, 3],  'test_ab': [53, 54]},
    10: {'train': [1, 4],  'test_ab': [51, 52]},
    11: {'train': [1, 5],  'test_ab': [51, 52]},
    12: {'train': [1, 6],  'test_ab': [13, 14, 16, 32]},
    13: {'train': [1, 7],  'test_ab': [24, 25, 26, 27]},
    14: {'train': [1, 8],  'test_ab': [55]},
    15: {'train': [2, 3],  'test_ab': [82, 83]},
    16: {'train': [2, 4],  'test_ab': [58]},
    17: {'train': [2, 5],  'test_ab': [97]},
    18: {'train': [2, 6],  'test_ab': [61, 62]},
    19: {'train': [2, 7],  'test_ab': [59]},
    20: {'train': [2, 8],  'test_ab': [60]},
    21: {'train': [3, 4],  'test_ab': [70]},
    22: {'train': [3, 5],  'test_ab': [94]},
    23: {'train': [3, 6],  'test_ab': [77, 78]},
    24: {'train': [3, 7],  'test_ab': [74, 75]},
    25: {'train': [3, 8],  'test_ab': [76]},
    26: {'train': [4, 5],  'test_ab': [96]},
    27: {'train': [4, 6],  'test_ab': [73]},
    28: {'train': [4, 7],  'test_ab': [71, 72]},
    29: {'train': [4, 8],  'test_ab': [88, 89]},
    30: {'train': [5, 6],  'test_ab': [91]},
    31: {'train': [5, 7],  'test_ab': [92, 93]},
    32: {'train': [5, 8],  'test_ab': [101, 102]},
    33: {'train': [6, 7],  'test_ab': [17]},
    34: {'train': [6, 8],  'test_ab': [80, 81]},
    35: {'train': [7, 8],  'test_ab': [79]},
}
#     17: {'train': [2, 9],  'test_ab': [39]},
#     18: {'train': [2, 10], 'test_ab': [38]},



# take all compositions of index i
# shift position by -1 and add to trial
# shift position by 1 and add to trial
# shift position by -1 and add to trial
# shift position by 1 and add to trial
#  
# 0-1 : -0_5 +1_2 
# 0-2 : -0_1 -2_5
# 0-3 : -0_2 +1_3
# 0-4 : -0_3 -4_5
# 0-5 : -0_4 +1_5
# 1-2 : 1_3 0_2
# 1-3 : 1_4 2_3
# 1-4 : 1_5 0_4
# 1-5 : 0_1 2_5
# 2-3 : 1_2 3_4
# 2-4 : 2_3 1_4
# 2-5 : 2_4 3_5
# 3-4 : 3_5 2_4
# 3-5 : 0_3 4_5
# 4-5 : 3_4 0_5



    # print(cond)
    # comp_a = ELEM_TO_COMP[cond[0]]
    # comp_b = ELEM_TO_COMP[cond[1]]
    
    # # train_ab = np.unique(comp_a + comp_b).tolist()[0]
    # train_ab = [v for v in comp_a if v in comp_b][0]
    # # train_ac = [c for c in comp_a if c not in comp_b]
    # # train_bc = [c for c in comp_b if c not in comp_a]
    # comps.append(train_ab)
    # trials.append({
    #     'train': cond,
    #     'test_ab': train_ab,
    #     'test_ac': None,
    #     'test_bd': None,
    #     'test_ef': None,
    # })
    
# for c in comps:
#     # a,b = COMP_TO_ELEM[c]
#     cond_ = COMP_TO_ELEM[c]
    
#     k1 = True
#     k2 = True
#     k3 = True
#     for i in range(len(unique_conditions)):
#         # cond_ = unique_conditions[i]
#         a,b = unique_conditions[i]
        
#         if k1 and (a in cond_) and (b not in cond_) and trials[i]['test_ac'] is None:
#             trials[i]['test_ac'] = c
#             k1=False
#         elif k2 and (a not in cond_) and (b in cond_) and trials[i]['test_bd'] is None:
#             trials[i]['test_bd'] = c
#             k2=False
#         elif k3 and (a not in cond_) and (b not in cond_) and trials[i]['test_ef'] is None:
#             trials[i]['test_ef'] = c
#             k3=False

#     if k1 or k2 or k3:
#         print('issue')
