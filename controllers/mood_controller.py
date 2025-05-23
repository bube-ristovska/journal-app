from flask import Blueprint, render_template, request, jsonify
from models.database import db
from models.mood import MoodEntry, MoodPattern
from datetime import date, datetime, timedelta
import json

mood_bp = Blueprint('mood', __name__, url_prefix='/mood')

MOOD_OPTIONS = [
    {'score': 1, 'emoji': '😢', 'name': 'Многу тажно', 'color': '#ef4444'},
    {'score': 2, 'emoji': '😕', 'name': 'Тажно', 'color': '#f97316'},
    {'score': 3, 'emoji': '😐', 'name': 'Неутрално', 'color': '#eab308'},
    {'score': 4, 'emoji': '😊', 'name': 'Среќно', 'color': '#22c55e'},
    {'score': 5, 'emoji': '😄', 'name': 'Многу среќно', 'color': '#16a34a'}
]

COMMON_TRIGGERS = [
    'Училиште/Работа', 'Семејство', 'Пријатели', 'Романтичен партнер',
    'Финансии', 'Здравје', 'Социјални медиуми', 'Вести',
    'Времето', 'Спиење', 'Храна', 'Сообраќај'
]

COPING_STRATEGIES = [
    'Длабоко дишење', 'Медитација', 'Музика', 'Вежбање',
    'Разговор со пријател', 'Пишување', 'Прошетка', 'Туш',
    'Читање', 'Цртање', 'Играње', 'Спиење'
]


@mood_bp.route('/')
def index():
    today = date.today()
    entry = MoodEntry.query.filter_by(date=today).first()

    return render_template('mood/tracker.html',
                           entry=entry,
                           mood_options=MOOD_OPTIONS,
                           triggers=COMMON_TRIGGERS,
                           strategies=COPING_STRATEGIES)


@mood_bp.route('/save', methods=['POST'])
def save_mood():
    try:
        data = request.get_json()
        today = date.today()

        entry = MoodEntry.query.filter_by(date=today).first()
        if not entry:
            entry = MoodEntry(date=today)
            db.session.add(entry)

        entry.mood_score = data.get('mood_score')
        entry.mood_emoji = data.get('mood_emoji')
        entry.mood_name = data.get('mood_name')
        entry.anxiety_level = data.get('anxiety_level')
        entry.energy_level = data.get('energy_level')
        entry.sleep_quality = data.get('sleep_quality')
        entry.notes = data.get('notes')
        entry.triggers = json.dumps(data.get('triggers', []))
        entry.coping_strategies = json.dumps(data.get('coping_strategies', []))

        db.session.commit()
        return jsonify({'success': True, 'message': 'Расположението е зачувано!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@mood_bp.route('/trends')
def trends():
    # Get last 30 days of mood data
    today = date.today()
    start_date = today - timedelta(days=30)

    entries = MoodEntry.query.filter(
        MoodEntry.date >= start_date
    ).order_by(MoodEntry.date.asc()).all()

    # Prepare data for charts
    mood_data = []
    anxiety_data = []
    energy_data = []

    for entry in entries:
        mood_data.append({
            'date': entry.date.strftime('%Y-%m-%d'),
            'score': entry.mood_score,
            'emoji': entry.mood_emoji
        })
        if entry.anxiety_level:
            anxiety_data.append({
                'date': entry.date.strftime('%Y-%m-%d'),
                'level': entry.anxiety_level
            })
        if entry.energy_level:
            energy_data.append({
                'date': entry.date.strftime('%Y-%m-%d'),
                'level': entry.energy_level
            })

    return render_template('mood/trends.html',
                           mood_data=mood_data,
                           anxiety_data=anxiety_data,
                           energy_data=energy_data)