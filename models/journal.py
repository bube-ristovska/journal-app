from models.database import db, BaseModel
from sqlalchemy import text


class JournalEntry(BaseModel):
    __tablename__ = 'journal_entries'

    date = db.Column(db.Date, nullable=False, unique=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    gratitude_1 = db.Column(db.String(255))
    gratitude_2 = db.Column(db.String(255))
    gratitude_3 = db.Column(db.String(255))
    highlight = db.Column(db.Text)
    challenge = db.Column(db.Text)
    tomorrow_goal = db.Column(db.Text)
    energy_level = db.Column(db.Integer)
    stress_level = db.Column(db.Integer)


class JournalPrompt(BaseModel):
    __tablename__ = 'journal_prompts'

    category = db.Column(db.String(50), nullable=False)
    question = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)