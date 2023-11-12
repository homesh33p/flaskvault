from flask import render_template,url_for,request,redirect,request, jsonify
from flask_login import login_required
from . import status_bp
from celery.result import AsyncResult

@status_bp.route('/task_status/<task_id>', methods=['GET', 'POST'])
@login_required
def task_status(task_id):
    if request.method == 'POST':
        # Get the task status (replace this with your logic to retrieve the status)
        task_status = get_task_status(task_id)
        return jsonify({'task_status': task_status})

    return render_template('status/task_status.html', task_id=task_id)

def get_task_status(task_id):
    try:
        task_result = AsyncResult(task_id)
    except:
        return "unknown"
    return task_result.status