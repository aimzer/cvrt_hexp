from itertools import combinations

from flask import (Blueprint, redirect, render_template, request, session, url_for)
from .io import write_data, write_metadata, write_exp_db, remove_exp, append_data
# from prepare_exp import prepare_experiment
from .prepare_exp import unqueue_experiment, prepare_experiment


## Initialize blueprint.
bp = Blueprint('experiment', __name__)

@bp.route('/experiment')
def experiment():
    """Present jsPsych experiment to participant."""

    ## Error-catching: screen for missing session.
    if not 'workerId' in session:
        print('exp case 0')

        ## Redirect participant to error (missing workerId).
        return redirect(url_for('error.error', errornum=1000))

    ## Case 1: previously completed experiment.
    elif 'complete' in session:
        print('exp case 1')
        ## Update metadata.
        session['WARNING'] = "Revisited experiment page."
        write_metadata(session, ['WARNING'], 'a')

        ## Redirect participant to complete page.
        return redirect(url_for('complete.complete'))

    ## Case 2: repeat visit.
    elif 'experiment' in session:
        print('exp case 2')

        ## Update participant metadata.
        session['ERROR'] = "1004: Revisited experiment."
        session['complete'] = 'error'
        write_metadata(session, ['ERROR','complete'], 'a')
        
        ## Redirect participant to error (previous participation).
        return redirect(url_for('error.error', errornum=1004))

    ## Case 3: first visit.
    else:
        print('exp case 3')

        ## Update participant metadata.
        session['experiment'] = True
        
        # print(session['exp_db'])
        exp_idx, count = unqueue_experiment(session['exp_db'], pilote=session['pilote'])
        session['exp_idx'] = exp_idx
        session['exp_count'] = count

        trial_idx, trial_seq_idx, task_perm, task_perm_names, tasks, tasks_names, n_trials = prepare_experiment(session['exp_idx'], pilote=session['pilote'])

        session['trial_idx'] = trial_idx
        session['trial_seq_idx'] = trial_seq_idx

        session['task_perm'] = ' '.join([str(s) for s in task_perm])
        session['task_perm_names'] = ' '.join(task_perm_names)
        session['task_idx'] = ' '.join([str(s) for s in tasks])
        session['task_names'] = ' '.join(tasks_names)

        ## write resolve exeriment data
        write_metadata(session, ['experiment', 'exp_idx', 'trial_idx', 'trial_seq_idx', 'task_perm', 'task_perm_names', 'task_idx', 'task_names'], 'a')

        write_exp_db(session, ['workerId', 'exp_idx', 'exp_count', 'task_perm', 'task_perm_names', 'task_idx', 'task_names'], 'w')

        if session['experiment_debug']:
            # tasks_names = tasks_names[0:1]
            n_trials = [1 for n in n_trials]

        content = {
            "workerId": session['workerId'], 
            "assignmentId": session['assignmentId'], 
            "hitId": session['hitId'], 
            "code_success": session['code_success'], 
            "code_reject": session['code_reject'],
            "trial_idx": trial_idx, 
            "trial_seq_idx": trial_seq_idx, 
            "tasks_names": tasks_names, 
            "n_trials": n_trials,
        }

        ## Present experiment.
        return render_template('experiment.html', **content)
        # return render_template('experiment.html', workerId=session['workerId'], assignmentId=session['assignmentId'], hitId=session['hitId'], code_success=session['code_success'], code_reject=session['code_reject'])

@bp.route('/experiment', methods=['POST'])
def pass_message():
    """Write jsPsych message to metadata."""

    if request.is_json:

        ## Retrieve jsPsych data.
        msg = request.get_json()

        ## Update participant metadata.
        session['MESSAGE'] = msg
        write_metadata(session, ['MESSAGE'], 'a')

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)


@bp.route('/save_block', methods=['POST'])
def save_block():
    """Write jsPsych message to metadata."""

    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        # write_data(session, ['MESSAGE'], 'a')
        append_data(session, JSON)
        

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)


@bp.route('/redirect_success', methods = ['GET', 'POST'])
def redirect_success():
    """Save complete jsPsych dataset to disk."""

    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        ## Save jsPsch data to disk.
        write_data(session, JSON, method='pass')

    ## Flag experiment as complete.
    session['complete'] = 'success'
    write_metadata(session, ['complete','code_success'], 'a')

    # # print(session['workerId'])
    # if 'test' in session['workerId']:
    #     print(session['workerId'])

    #     return redirect(url_for('complete.complete'))
    
    # else:
    #     url = "https://app.prolific.co/submissions/complete?cc=" + session['code_success']
    #     return redirect(url)
    
    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## The corresponding jsPsych function handles the redirect.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)


@bp.route('/discard_experiment', methods = ['POST'])
def discard_experiment():
    """Save complete jsPsych dataset to disk."""

    # print('discarded experiment')

    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        ## Save jsPsch data to disk.
        write_data(session, JSON, method='reject')

    ## Flag experiment as complete.
    session['complete'] = 'reject'
    write_metadata(session, ['complete','code_reject'], 'a')

    if 'experiment' in session and session['experiment']:
        remove_exp(session)

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## The corresponding jsPsych function handles the redirect.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)


@bp.route('/redirect_reject', methods = ['POST'])
def redirect_reject():
    """Save rejected jsPsych dataset to disk."""

    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        ## Save jsPsch data to disk.
        write_data(session, JSON, method='reject')

    
    ## Flag experiment as complete.
    session['complete'] = 'reject'
    write_metadata(session, ['complete','code_reject'], 'a')

    if 'experiment' in session and session['experiment']:
        remove_exp(session)

    # if 'test' in session['workerId']:
    #     return redirect(url_for('complete.complete'))
    #     # return render_template('exit.html')
    
    # else:
    #     url = "https://app.prolific.co/submissions/complete?cc=" + session['code_reject']
    #     return redirect(url)

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## The corresponding jsPsych function handles the redirect.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)

@bp.route('/redirect_error', methods = ['POST'])
def redirect_error():
    """Save rejected jsPsych dataset to disk."""

    if request.is_json:

        ## Retrieve jsPsych data.
        JSON = request.get_json()

        ## Save jsPsch data to disk.
        write_data(session, JSON, method='reject')

    if 'experiment' in session and session['experiment']:
        remove_exp(session)
    
    ## Flag experiment as complete.
    session['complete'] = 'error'
    write_metadata(session, ['complete'], 'a')

    ## DEV NOTE:
    ## This function returns the HTTP response status code: 200
    ## Code 200 signifies the POST request has succeeded.
    ## The corresponding jsPsych function handles the redirect.
    ## For a full list of status codes, see:
    ## https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
    return ('', 200)
