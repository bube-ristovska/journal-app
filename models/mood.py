from models.database import db, BaseModel


class MoodEntry(BaseModel):
    __tablename__ = 'mood_entries'

    date = db.Column(db.Date, nullable=False, unique=True)
    mood_score = db.Column(db.Integer, nullable=False)  # 1-5
    mood_emoji = db.Column(db.String(10))
    mood_name = db.Column(db.String(50))
    anxiety_level = db.Column(db.Integer)  # 1-10
    energy_level = db.Column(db.Integer)  # 1-10
    sleep_quality = db.Column(db.Integer)  # 1-10
    notes = db.Column(db.Text)
    triggers = db.Column(db.Text)  # JSON string
    coping_strategies = db.Column(db.Text)  # JSON string


class MoodPattern(BaseModel):
    __tablename__ = 'mood_patterns'

    week_start = db.Column(db.Date, nullable=False)
    average_mood = db.Column(db.Float)
    mood_variance = db.Column(db.Float)
    anxiety_average = db.Column(db.Float)
    energy_average = db.Column(db.Float)
    insights = db.Column(db.Text)