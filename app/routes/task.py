from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import Task, User


task = Blueprint('task', __name__)


# タスク作成
@task.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')

    if not title:
        return jsonify({"msg": "Title is required"}), 400

    user_id = get_jwt_identity()['user_id']

    new_task = Task(
        user_id=user_id,
        title=title,
        description=description,
        due_date=due_date
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"msg": "Task created successfully", "task_id": new_task.id}), 201


# タスク取得
@task.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():

    user_id = get_jwt_identity()['user_id']
    tasks = Task.query.filter(Task.user_id == user_id).all()

    if not tasks:
        return jsonify({"msg": "No tasks found"}), 404

    tasks_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.strftime('%Y-%m-%d'),
            "completed": task.completed
        }
        for task in tasks
    ]
    return jsonify(tasks_list), 200