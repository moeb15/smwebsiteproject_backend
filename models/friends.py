from extensions import db
from models.users import User


class Friends(db.Model):
    __tablename__ = 'friends'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    recipient = db.Column(db.Integer, nullable=False, unique=True)
    is_added = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    @classmethod
    def get_friend_request(cls, user_id, recipient):
        if cls.query.filter_by(user_id=user_id, recipient=recipient).first() == None:
            return cls.query.filter_by(user_id=recipient, recipient=user_id).first()
        return cls.query.filter_by(user_id=user_id, recipient=recipient).first()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()