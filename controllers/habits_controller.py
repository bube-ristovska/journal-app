from flask import Blueprint, render_template, request, jsonify
from models.database import db
from models.habits import Habit, HabitEntry
from datetime import date, datetime, timedelta
from sqlalchemy import func

habits_bp = Blueprint('habits', __name__, url_prefix='/habits')

DEFAULT_HABITS = [
    {'name': 'Пиев доволно вода (8+ чаши)', 'category': 'Физичко здравје', 'icon': '💧'},
    {'name': 'Спиев 8+ часа', 'category': 'Физичко здравје', 'icon': '😴'},
    {'name': 'Се движев/вежбав 30+ минути', 'category': 'Физичко здравје', 'icon': '🏃'},
    {'name': 'Јадев здрава храна', 'category': 'Физичко здравје', 'icon': '🥗'},
    {'name': 'Медитирав/се релаксирав', 'category': 'Ментално здравје', 'icon': '🧘'},
    {'name': 'Читав книга/едукативен материјал', 'category': 'Личен развој', 'icon': '📚'},
    {'name': 'Се дружев со пријатели/семејство', 'category': 'Социјални', 'icon': '👥'},
    {'name': 'Работев на хоби', 'category': 'Креативност', 'icon': '🎨'},
    {'name': 'Излегов надвор во природа', 'category': 'Благосостојба', 'icon': '🌳'},
    {'name': 'Се грижев за лична хигиена', 'category': 'Самогрижа', 'icon': '🧼'},
    {'name': 'Поминав време без телефон', 'category': 'Дигитална детоксикација', 'icon': '📵'},
    {'name': 'Напишав во дневник', 'category': 'Саморефлексија', 'icon': '📝'},
    {'name': 'Слушав музика која ме опушта', 'category': 'Благосостојба', 'icon': '🎵'},
    {'name': 'Помогнав на некого', 'category': 'Пријателство', 'icon': '🤝'},
    {'name': 'Се израдував за мали работи', 'category': 'Позитивност', 'icon': '😊'}
]


@habits_bp.route('/')
def index():
    # Initialize default habits if none exist
    if Habit.query.count() == 0:
        for habit_data in DEFAULT_HABITS:
            habit = Habit(**habit_data)
            db.session.add(habit)
        db.session.commit()

    habits = Habit.query.filter_by(is_active=True).all()
    today = date.today()

    # Get today's entries
    entries = {}
    for habit in habits:
        entry = HabitEntry.query.filter_by(habit_id=habit.id, date=today).first()
        entries[habit.id] = entry

    return render_template('habits/tracker.html', habits=habits, entries=entries, today=today)


@habits_bp.route('/toggle', methods=['POST'])
def toggle_habit():
    try:
        data = request.get_json()
        habit_id = data.get('habit_id')
        completed = data.get('completed')
        notes = data.get('notes', '')

        today = date.today()
        entry = HabitEntry.query.filter_by(habit_id=habit_id, date=today).first()

        if entry:
            entry.completed = completed
            entry.notes = notes
        else:
            entry = HabitEntry(habit_id=habit_id, date=today, completed=completed, notes=notes)
            db.session.add(entry)

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@habits_bp.route('/analytics')
def analytics():
    habits = Habit.query.filter_by(is_active=True).all()
    today = date.today()

    # Get last 30 days data
    analytics_data = {}
    for habit in habits:
        entries = HabitEntry.query.filter(
            HabitEntry.habit_id == habit.id,
            HabitEntry.date >= today - timedelta(days=30)
        ).all()

        total_days = 30
        completed_days = len([e for e in entries if e.completed])
        completion_rate = (completed_days / total_days) * 100 if total_days > 0 else 0

        analytics_data[habit.id] = {
            'habit': habit,
            'completion_rate': completion_rate,
            'completed_days': completed_days,
            'total_days': total_days,
            'streak': calculate_streak(habit.id)
        }

    return render_template('habits/analytics.html', analytics_data=analytics_data)


def calculate_streak(habit_id):
    today = date.today()
    streak = 0
    current_date = today

    while True:
        entry = HabitEntry.query.filter_by(habit_id=habit_id, date=current_date).first()
        if entry and entry.completed:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break

    return streak