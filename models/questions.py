from datetime import datetime, timezone
from sqlalchemy import text

from extensions import db

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    choices = db.Column(db.JSON(), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id'), nullable=True, index=True)
    
    created_at = db.Column(
            db.DateTime,
            default=lambda: datetime.now(timezone.utc),
            server_default=text('CURRENT_TIMESTAMP')
        )
    updated_at = db.Column(
            db.DateTime,
            default=lambda: datetime.now(timezone.utc),
            onupdate=text('CURRENT_TIMESTAMP'),
            server_default=text('CURRENT_TIMESTAMP')
        )

    question_tags = db.relationship('QuestionTag', backref=db.backref('questions', lazy=True))

class QuestionTag(db.Model):
    __tablename__ = 'question_tags'

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, primary_key=True)
    tag_name = db.Column(db.String(64), nullable=False, primary_key=True)

class Section(db.Model):
    __tablename__ = 'sections'

    section_id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(100), nullable=False, unique=True)
    unit = db.Column(db.String(100), nullable=True)
    chapter = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)

    questions = db.relationship('Question', backref=db.backref('section', lazy=True))
class UserQuestionHistory(db.Model):
    __tablename__ = 'user_question_histories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'questions.id'), nullable=False)
    solved_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_correct = db.Column(db.Boolean, default=False)
    is_solved = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('user_question_histories', lazy=True))
    question = db.relationship('Question', backref=db.backref('user_question_histories', lazy=True))

class UserFlaggedQuestion(db.Model):
    __tablename__ = 'user_flagged_questions'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False, primary_key=True)
    flag = db.Column(db.String(16), nullable=False)# green, yellow, red

    user = db.relationship('User', backref=db.backref('user_flagged_questions', lazy=True))
    question = db.relationship('Question', backref=db.backref('user_flagged_questions', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'question_id', 'flag', name='unique_user_flagged_question'),
    )