from flask import Flask, render_template, session
from config import Config
from models.database import db
from controllers.journal_controller import journal_bp
from controllers.habits_controller import habits_bp
from controllers.mood_controller import mood_bp
from controllers.goals_controller import goals_bp
from controllers.resources_controller import resources_bp
from controllers.analytics_controller import analytics_bp
from datetime import date
import random


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(journal_bp)
    app.register_blueprint(habits_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(analytics_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()

MOTIVATIONAL_QUOTES = [
    "Секој ден е нова можност да станеш подобра верзија од себе.",
    "Твоите чувства се валидни и важни.",
    "Малите чекори секогаш водат кон големи промени.",
    "Ти си посилен/на отколку што мислиш.",
    "Грешките се дел од учењето и растењето.",
    "Твојата ментална здравје е приоритет.",
    "Секој ден донесува нови можности.",
    "Ти заслужуваш љубов и грижа, особено од себе.",
    "Прогресот е поважен од совршенството.",
    "Твојот глас и мислењето се важни.",
    "Храброста не е отсуството на страв, туку дејствувањето покрај стравот.",
    "Твојата вредност не зависи од мислењето на другите.",
    "Секоја тешкотија е можност за раст.",
    "Ти си единствен/на и тоа е твојата суперсила.",
    "Самогрижата не е себичност, туку потреба."
]


@app.route('/')
def index():
    # Get today's quote
    today = date.today()
    random.seed(today.toordinal())
    daily_quote = random.choice(MOTIVATIONAL_QUOTES)

    # Quick stats for dashboard
    from models.journal import JournalEntry
    from models.mood import MoodEntry
    from models.habits import HabitEntry
    from models.goals import Goal

    today_journal = JournalEntry.query.filter_by(date=today).first()
    today_mood = MoodEntry.query.filter_by(date=today).first()
    today_habits = HabitEntry.query.filter_by(date=today).count()
    active_goals = Goal.query.filter_by(status='active').count()

    quick_stats = {
        'journal_done': bool(today_journal and today_journal.answer),
        'mood_logged': bool(today_mood),
        'habits_count': today_habits,
        'active_goals': active_goals
    }

    return render_template('index.html',
                           daily_quote=daily_quote,
                           quick_stats=quick_stats)


@app.context_processor
def inject_date():
    return {'today': date.today()}


if __name__ == '__main__':
    app.run(debug=True)
