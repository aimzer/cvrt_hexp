from flask import (Blueprint, redirect, render_template, request, session, url_for)
from .io import write_metadata

## Initialize blueprint.
bp = Blueprint('alert', __name__)

@bp.route('/alert')
def alert():
    """Present alert to participant."""

    ## Error-catching: screen for missing session.
    if not 'workerId' in session:
        print('alert case 0')

        ## Redirect participant to error (missing workerId).
        return redirect(url_for('error.error', errornum=1000))

    ## Case 1: previously completed experiment.
    elif 'complete' in session:
        print('alert case 1')

        ## Update metadata.
        session['WARNING'] = "Revisited alert page."
        write_metadata(session, ['WARNING'], 'a')

        ## Redirect participant to complete page.
        return redirect(url_for('complete.complete'))

    ## Case 2: repeat visit.
    elif 'alert' in session:
        print('alert case 2')

        ## Update participant metadata.
        session['WARNING'] = "Revisited alert page."
        write_metadata(session, ['WARNING'], 'a')

        ## Redirect participant to error (previous participation).
        return redirect(url_for('experiment.experiment'))

    ## Case 3: first visit.
    else:
        print('alert case 3')

        ## Update participant metadata.
        session['alert'] = True
        write_metadata(session, ['alert'], 'a')

        ## Present alert page.
        return render_template('alert.html')

@bp.route('/alert', methods=['POST'])
def alert_post():
    """Process participant repsonse to alert page."""
    print('alert response')
    alert_check = int(request.form['alert_check'])

    ## Redirect participant to experiment.
    return redirect(url_for('experiment.experiment'))
    # return redirect(url_for('consent.consent'))
