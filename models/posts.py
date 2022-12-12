from extensions import db
from models.users import User
from sqlalchemy import desc


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    post_content = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.func.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def get_all_posts(cls,user_id,page,per_page):
        return cls.query.filter_by(user_id=user_id).order_by(desc(cls.created_at)).paginate(page=page,per_page=per_page)

    @classmethod
    def get_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()