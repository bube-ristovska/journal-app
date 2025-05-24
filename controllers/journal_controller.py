from flask import Blueprint, render_template, request, jsonify, flash
from models.database import db
from models.journal import JournalEntry, JournalPrompt
from datetime import date, datetime, timedelta
import random
import json

journal_bp = Blueprint('journal', __name__, url_prefix='/journal')

DAILY_QUESTIONS = [
    "Што беше најдоброто нешто што ти се случи денес?",
    "Како се чувствуваш во моментов и зошто?",
    "За што си благодарен/на денес?",
    "Кое предизвик го совлада денес?",
    "Што ново научи за себе денес?",
    "Како можеш да се погрижиш за себе утре?",
    "Која активност те направи најсреќен/на денес?",
    "Што би сакал/а да промениш за утре?",
    "Кој човек влијаеше позитивно на твојот ден?",
    "Како се справи со стресот денес?",
    "Што те мотивираше денес?",
    "Каков комплимент би си го дал/а денес?",
    "Која цел постави за утре?",
    "Како покажа љубов кон себе денес?",
    "Што те прави горд/а на себе денес?",
    "Која емоција беше најсилна денес?",
    "Што те инспирира да продолжиш?",
    "Како можеш да помогнеш на некој утре?",
    "Што би сакал/а да си кажеш од минатата година?",
    "Каде се чувствуваш најбезбедно?"
]


@journal_bp.route('/')
def index():
    today = date.today()
    entry = JournalEntry.query.filter_by(date=today).first()

    if not entry:
        # Get daily question
        random.seed(today.toordinal())
        question = random.choice(DAILY_QUESTIONS)
        entry = JournalEntry(date=today, question=question)
        db.session.add(entry)
        db.session.commit()

    return render_template('journal/daily.html', entry=entry)


@journal_bp.route('/save', methods=['POST'])
def save_entry():
    try:
        data = request.get_json()
        today = date.today()
        entry = JournalEntry.query.filter_by(date=today).first()

        if entry:
            entry.answer = data.get('answer')
            entry.gratitude_1 = data.get('gratitude_1')
            entry.gratitude_2 = data.get('gratitude_2')
            entry.gratitude_3 = data.get('gratitude_3')
            entry.highlight = data.get('highlight')
            entry.challenge = data.get('challenge')
            entry.tomorrow_goal = data.get('tomorrow_goal')
            entry.energy_level = data.get('energy_level')
            entry.stress_level = data.get('stress_level')
            entry.updated_at = datetime.utcnow()

            db.session.commit()
            return jsonify({'success': True, 'message': 'Записот е зачуван успешно!'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Грешка при зачувувањето'})


@journal_bp.route('/history')
def history():
    entries = JournalEntry.query.order_by(JournalEntry.date.desc()).limit(30).all()
    return render_template('journal/history.html', entries=entries)


@journal_bp.route('/prompts')
def prompts():
    categories = ['Саморефлексија', 'Емоции', 'Цели', 'Односи', 'Благодарност']
    return render_template('journal/prompts.html', categories=categories, questions=DAILY_QUESTIONS)