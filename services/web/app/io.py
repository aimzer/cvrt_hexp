import os
import json
from datetime import datetime

def write_metadata(session, keys, mode='w'):
    """Write metadata to disk.

    Parameters
    ----------
    session : flask session
        Current user session.
    keys : list
        Session keys to write to file.
    mode : r | w | a
        Open file mode.
    """

    ## Define timestamp.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ## Write metadata to disk.
    fout = os.path.join(session['metadata'], session['workerId'])
    with open(fout, mode) as f:
        for k in keys:
            f.write(f'{timestamp}\t{k}\t{session[k]}\n')


def write_data(session, json, method='pass'):
    """Write jsPsych output to disk.

    Parameters
    ----------
    session : flask session
        Current user session.
    json : object
        Data object returned by jsPsych.
    method : pass | reject
        Designates target folder for data.
    """

    ## Write data to disk.
    if method == 'pass':
        fout = os.path.join(session['data'], '%s.json' %session['subId'])
    elif method == 'reject':
        fout = os.path.join(session['reject'], '%s.json' %session['subId'])

    with open(fout, 'w') as f: f.write(json)

def append_data(session, json):
    """Write jsPsych output to disk.

    Parameters
    ----------
    session : flask session
        Current user session.
    json : object
        Data object returned by jsPsych.
    method : pass | reject
        Designates target folder for data.
    """

    idx = len([f for f in os.listdir(session['data']) if session['subId'] in f])
    # Write data to disk.
    fout = os.path.join(session['data'], '{}_{}.json'.format(session['subId'], idx))
    print(fout)
    with open(fout, 'w') as f: f.write(json)



def write_exp_db(session, keys, mode='w'):
    """Write metadata to disk.

    Parameters
    ----------
    session : flask session
        Current user session.
    keys : list
        Session keys to write to file.
    mode : r | w | a
        Open file mode.
    """

    ## Define timestamp.
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ## Write metadata to disk.
    fout = os.path.join(session['exp_db'], '{}_{}'.format(session['exp_idx'], session['exp_count']))
    with open(fout, mode) as f:
        for k in keys:
            f.write(f'{timestamp}\t{k}\t{session[k]}\n')

def remove_exp(session):
    file = os.path.join(session['exp_db'], '{}_{}'.format(session['exp_idx'], session['exp_count']))

    if os.path.exists(file):
        os.remove(file)