from flask import Blueprint, render_template, request, jsonify
from models.database import db
from models.journal import JournalEntry
from models.habits import Habit, HabitEntry
from models.mood import MoodEntry
from models.goals import Goal
from datetime import date, datetime, timedelta
from sqlalchemy import func
import json

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')


@analytics_bp.route('/')
def dashboard():
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Basic stats
    stats = {
        'journal_entries': JournalEntry.query.count(),
        'active_goals': Goal.query.filter_by(status='active').count(),
        'completed_goals': Goal.query.filter_by(status='completed').count(),
        'mood_entries': MoodEntry.query.count()
    }

    # Mood trends (last 30 days)
    mood_entries = MoodEntry.query.filter(MoodEntry.date >= month_ago).order_by(MoodEntry.date).all()
    mood_trend = []
    for entry in mood_entries:
        mood_trend.append({
            'date': entry.date.strftime('%Y-%m-%d'),
            'mood': entry.mood_score,
            'anxiety': entry.anxiety_level or 0,
            'energy': entry.energy_level or 0
        })

    # Habit completion rates
    habits = Habit.query.filter_by(is_active=True).all()
    habit_stats = []
    for habit in habits:
        entries = HabitEntry.query.filter(
            HabitEntry.habit_id == habit.id,
            HabitEntry.date >= month_ago
        ).all()

        total_days = 30
        completed_days = len([e for e in entries if e.completed])
        completion_rate = (completed_days / total_days) * 100 if total_days > 0 else 0

        habit_stats.append({
            'name': habit.name,
            'completion_rate': completion_rate,
            'icon': habit.icon
        })

    # Weekly mood average
    weekly_moods = MoodEntry.query.filter(MoodEntry.date >= week_ago).all()
    avg_mood = sum([m.mood_score for m in weekly_moods]) / len(weekly_moods) if weekly_moods else 0

    return render_template('analytics/dashboard.html',
                           stats=stats,
                           mood_trend=mood_trend,
                           habit_stats=habit_stats,
                           avg_mood=round(avg_mood, 1))


@analytics_bp.route('/insights')
def insights():
    today = date.today()
    month_ago = today - timedelta(days=30)

    insights = []

    # Mood insights
    mood_entries = MoodEntry.query.filter(MoodEntry.date >= month_ago).all()
    if mood_entries:
        avg_mood = sum([m.mood_score for m in mood_entries]) / len(mood_entries)
        if avg_mood >= 4:
            insights.append({
                'type': 'positive',
                'title': 'Одлично расположение! 😊',
                'message': f'Твоето просечно расположение изнесува {avg_mood:.1f}/5. Продолжувaj со добрите навики!'
            })
        elif avg_mood <= 2.5:
            insights.append({
                'type': 'concern',
                'title': 'Ниско расположение 😟',
                'message': 'Забележуваме дека твоето расположение е ниско последниве денови. Размисли да разговараш со некого од доверба.'
            })

    # Habit insights
    habits = Habit.query.filter_by(is_active=True).all()
    for habit in habits:
        entries = HabitEntry.query.filter(
            HabitEntry.habit_id == habit.id,
            HabitEntry.date >= month_ago
        ).all()

        if entries:
            completion_rate = (len([e for e in entries if e.completed]) / 30) * 100
            if completion_rate >= 80:
                insights.append({
                    'type': 'achievement',
                    'title': f'Одлична навика! {habit.icon}',
                    'message': f'Имаш {completion_rate:.0f}% успех со "{habit.name}". Продолжувај вака!'
                })

    # Goal insights
    goals = Goal.query.filter_by(status='active').all()
    overdue_goals = [g for g in goals if g.target_date and g.target_date < today]
    if overdue_goals:
        insights.append({
            'type': 'reminder',
            'title': 'Рок за цели ⏰',
            'message': f'Имаш {len(overdue_goals)} цели кои го надминаа рокот. Ревидирај ги твоите цели.'
        })

    return render_template('analytics/insights.html', insights=insights)