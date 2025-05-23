from models.database import db, BaseModel


class CopingStrategy(BaseModel):
    __tablename__ = 'coping_strategies'

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(20))
    duration = db.Column(db.String(50))
    instructions = db.Column(db.Text)
    benefits = db.Column(db.Text)


class CrisisResource(BaseModel):
    __tablename__ = 'crisis_resources'

    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(50))
    website = db.Column(db.String(255))
    description = db.Column(db.Text)
    country = db.Column(db.String(50))
    is_emergency = db.Column(db.Boolean, default=False)


class EducationalContent(BaseModel):
    __tablename__ = 'educational_content'

    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    age_group = db.Column(db.String(20))
    reading_time = db.Column(db.Integer)
    tags = db.Column(db.Text)