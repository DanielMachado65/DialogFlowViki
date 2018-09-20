from datetime import datetime


class RequestUser:
    """ Sample Request """

    def __init__(self, session, name, user_id, text, timestamp=datetime.utcnow):
        self.session = session
        self.name = name
        self.id = user_id
        self.text = text
        self.timestamp = timestamp

    @property
    def user(self):
        return '{} {}'.format(self.id, self.name)

    def __repr__(self):
        return "Request('{}', '{}', '{}', '{}')".format(
            self.session,
            self.name,
            self.id,
            self.text,
            self.timestamp
        )
