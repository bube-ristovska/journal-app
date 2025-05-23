from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models.database import db
from models.goals import Goal, GoalMilestone
from datetime import date, datetime

goals_bp = Blueprint('goals', __name__, url_prefix='/goals')

GOAL_CATEGORIES = [
    'Ментално здравје', 'Физичко здравје', 'Образование',
    'Социјални односи', 'Хобија', 'Лично развитие',
    'Финансии', 'Кариера', 'Креативност', 'Духовност'
]


@goals_bp.route('/')
def index():
    goals = Goal.query.filter_by(status='active').order_by(Goal.created_at.desc()).all()
    return render_template('goals/progress.html', goals=goals)


@goals_bp.route('/set')
def set_goal():
    return render_template('goals/set.html', categories=GOAL_CATEGORIES)


@goals_bp.route('/create', methods=['POST'])
def create_goal():
    try:
        data = request.get_json()

        goal = Goal(
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category'),
            target_date=datetime.strptime(data.get('target_date'), '%Y-%m-%d').date() if data.get(
                'target_date') else None,
            priority=data.get('priority', 'medium')
        )
        db.session.add(goal)
        db.session.flush()

        # Add milestones
        milestones = data.get('milestones', [])
        for milestone_data in milestones:
            milestone = GoalMilestone(
                goal_id=goal.id,
                title=milestone_data.get('title'),
                description=milestone_data.get('description'),
                due_date=datetime.strptime(milestone_data.get('due_date'), '%Y-%m-%d').date() if milestone_data.get(
                    'due_date') else None
            )
            db.session.add(milestone)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Целта е креирана успешно!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@goals_bp.route('/update_progress', methods=['POST'])
def update_progress():
    try:
        data = request.get_json()
        goal_id = data.get('goal_id')
        progress = data.get('progress')

        goal = Goal.query.get(goal_id)
        if goal:
            goal.progress = progress
            if progress >= 100:
                goal.status = 'completed'
            db.session.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@goals_bp.route('/complete_milestone', methods=['POST'])
def complete_milestone():
    try:
        data = request.get_json()
        milestone_id = data.get('milestone_id')

        milestone = GoalMilestone.query.get(milestone_id)
        if milestone:
            milestone.completed = True
            milestone.completed_date = date.today()

            # Update goal progress
            goal = milestone.goal
            total_milestones = len(goal.milestones)
            completed_milestones = len([m for m in goal.milestones if m.completed])
            goal.progress = int((completed_milestones / total_milestones) * 100) if total_milestones > 0 else 0

            db.session.commit()
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
