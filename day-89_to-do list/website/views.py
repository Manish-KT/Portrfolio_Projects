# this file will act as blueprint of our website where all routes will be stored
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .model import Task, Subtask
from . import db

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    all_tasks = Task.query.filter_by(user_id=current_user.id)
    return render_template("home.html", user=current_user, tasks=all_tasks)


@views.route('/create-task', methods=['GET', 'POST'])
@login_required
def create_task():
    if request.method == 'POST':
        task_heading = request.form.get('task_heading')
        task_description = request.form.get('task_description')

        if len(task_heading) < 1:
            flash("Task name is too short!", category="error")
        else:
            new_task = Task(task_heading=task_heading, task_description=task_description, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added!", category="success")
            return redirect(url_for("views.home"))
    return render_template('create_task.html', user=current_user)


# add a edit task functionalty which task id is recieved
@views.route("/edit-task/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    current_task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        current_task.task_heading = request.form.get("task_heading")
        current_task.task_description = request.form.get("task_description")
        current_task.subtasks.subtask_description = request.form.get("subtasks")

        # Commit the changes to the database
        db.session.commit()

        flash("Task updated successfully", "success")
        return redirect(url_for("views.home"))

    return render_template("edit_task.html", task_data=current_task, user=current_user)


@views.route("/delete-task/<int:task_id>", methods=["POST", "GET"])
@login_required
def delete_task(task_id):
    # Retrieve the task to delete based on task_id
    task_to_delete = Task.query.get_or_404(task_id)

    # Delete the task from the database
    db.session.delete(task_to_delete)
    db.session.commit()

    flash("Task deleted successfully", "success")
    return redirect(url_for("views.home"))
