from index import db, ma
from werkzeug.security import check_password_hash

class UserModel(db.Model):
    #creating the table for users
    __tablename = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(), nullable = False)


    #Creating the user records
    def createRecord(self):
        db.session.add(self)
        db.session.commit()
        return self

    
    # fetch all users\
    @classmethod
    def fetch_users(cls):
        users = cls.query.all()
        return users


    # fetch by id
    @classmethod
    def fetch_by_id(cls, id):
        user = cls.query.filter_by(id=id).first()
        return user

    # check if email exists
    @classmethod
    def check_email_exist(cls,email):
        user = cls.query.filter_by(email=email).first()
        return user

    # cjceck if password is valid
    @classmethod
    def check_password(cls,email,password):
        user = cls.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):

            return True
        else:
            return False



# schemas which allow us to regulate or melimit the data we want to expose to the consumer
class UserSchema(ma.Schema):
    class Meta:
        #fields to expose
        fields = ('id', 'username', 'email')