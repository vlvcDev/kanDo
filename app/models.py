from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db
from flask_login import UserMixin


# Association table for many-to-many relationship between users and boards
board_users = db.Table('board_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('board_id', db.Integer, db.ForeignKey('kanban_board.id'), primary_key=True),
    db.Column('role', db.String(20), nullable=False)  # e.g., 'owner', 'collaborator', 'viewer'
)

# Association table for many-to-many relationship between users and tickets (assigned users)
ticket_assignees = db.Table('ticket_assignees',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True)
)

# Association table for linking predecessor and successor tickets
ticket_links = db.Table('ticket_links',
    db.Column('predecessor_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True),
    db.Column('successor_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationships
    boards = db.relationship('KanbanBoard', secondary=board_users, back_populates='users')
    tickets_created = db.relationship('Ticket', backref='creator', lazy=True, foreign_keys='Ticket.created_by')
    tickets_completed = db.relationship('Ticket', backref='completer', lazy=True, foreign_keys='Ticket.completed_by')
    notifications = db.relationship('Notification', backref='user', lazy=True)
    activities = db.relationship('ActivityLog', backref='user', lazy=True)

class KanbanBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)  # For soft deletion

    # Relationships
    users = db.relationship('User', secondary=board_users, back_populates='boards')
    sections = db.relationship('Section', backref='board', lazy=True, cascade="all, delete-orphan")
    activities = db.relationship('ActivityLog', backref='board', lazy=True, cascade="all, delete-orphan")

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('kanban_board.id'), nullable=False)

    # Relationships
    tickets = db.relationship('Ticket', backref='section', lazy=True, cascade="all, delete-orphan")

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    github_issue_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)  # For soft deletion

    # Foreign keys
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    completed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Relationships
    assignees = db.relationship('User', secondary=ticket_assignees, backref='assigned_tickets', lazy=True)
    predecessors = db.relationship('Ticket', secondary=ticket_links,
                                   primaryjoin=id==ticket_links.c.successor_id,
                                   secondaryjoin=id==ticket_links.c.predecessor_id,
                                   backref='successors')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.Integer, db.ForeignKey('kanban_board.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
