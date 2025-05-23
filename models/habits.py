from models.database import db, BaseModel


class Habit(BaseModel):
    __tablename__ = 'habits'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    target_frequency = db.Column(db.String(20), default='daily')
    icon = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)


class HabitEntry(BaseModel):
    __tablename__ = 'habit_entries'

    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)

    habit = db.relationship('Habit', backref='entries')

    __table_args__ = (db.UniqueConstraint('habit_id', 'date'),)