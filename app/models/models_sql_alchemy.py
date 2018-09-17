from datetime import datetime

from sqlalchemy import orm

from app import db


class Request(db.Model):
    __tablename__ = 'request'
    session = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    response = db.relationship("Response", backref=orm.backref("request", uselist=False))

    def __repr__(self):
        return "Request({}, {}, {}, {}, {}, {})".format(
            self.session,
            self.name,
            self.id,
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
    parent_id = db.Column(db.String(30), db.ForeignKey('request.session'))
    id_request = db.relationship("Request", back_populates="response")

    def __repr__(self):
        return "Response({}, {}, {}, {}, {})".format(
            self.id_response,
            self.action,
            self.intentDetectionConfidence,
            self.fulfillmentText,
            self.parent_id
        )
