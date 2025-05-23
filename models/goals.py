from models.database import db, BaseModel


class Goal(BaseModel):
    __tablename__ = 'goals'

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    target_date = db.Column(db.Date)
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='active')
    progress = db.Column(db.Integer, default=0)


class GoalMilestone(BaseModel):
    __tablename__ = 'goal_milestones'

    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    completed_date = db.Column(db.Date)

    goal = db.relationship('Goal', backref='milestones')