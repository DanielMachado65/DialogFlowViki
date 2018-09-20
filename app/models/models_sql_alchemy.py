from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import orm

from app import db, login_manager


@login_manager.user_loader
def load_user(user_user):
    return Admin(email="admin@gmail.com", password="root")


class Request(db.Model):
    __tablename__ = 'request'
    id_request = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    id_user = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    response = db.relationship("Response", backref=orm.backref("request", uselist=False))

    def __repr__(self):
        return "Request({}, {}, {}, {}, {})".format(
            self.name,
            self.id_user,
            self.text,
            self.timestamp,
            self.response
        )


class Response(db.Model):
    __tablename__ = 'response'
    id_response = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(60), nullable=False)
    intentDetectionConfidence = db.Column(db.Integer, nullable=False)
    fulfillmentText = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('request.id_request'))
    id_request = db.relationship("Request", back_populates="response")

    def __repr__(self):
        return "Response({}, {}, {}, {}, {})".format(
            self.id_response,
            self.action,
            self.intentDetectionConfidence,
            self.fulfillmentText,
            self.parent_id
        )


class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
