from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash
from config.pyconfig import DevelopmentConfiguration


app = Flask(__name__)

#creating an instance of the devlopment configurations in our app
app.config.from_object(DevelopmentConfiguration)


#Instanciating my library imports to my app
db = SQLAlchemy(app)
ma = Marshmallow(app)


#instanciating my Api
api = Api(app, version="1.0", title="Agendas Api", description="Api to manage agendas")


#Namespacing - used to classify your routes endpoints
ns_users = api.namespace("user", description="Perform user operations")
ns_agenda = api.namespace("agenda", description="Perform agenda operations")
ns_login = api.namespace("login", description="Perform login operations")


#Api Models
user = api.model('users', {
    "username": fields.String(required=True, description="The user's username"),
    "email": fields.String(required=True, description="The user's email"),
    "password": fields.String(required=True, desciption="the user's password")
})

agenda = api.model('agenda', {
    "title": fields.String(required=True, description="The title of the agenda"),
    "description": fields.String(required=True, description="The description for the agenda title")
})

login = api.model('login', {
    "email": fields.String(required=True, description="User's email for login"),
    "password": fields.String(required=True, description="User's password for login")
})


#importing the models to be used
from models.agenda import AgendaModel, AgendaSchema
from models.users import UserModel, UserSchema

#instanciating the schema classes we have
user_schema = UserSchema()
users_schema = UserSchema(many = True)

agenda_schema = AgendaSchema()
agendas_schema = AgendaSchema(many = True)


#before any request is handled, we need to have the tables existing in our db
@app.before_first_request
def createTables():
    db.create_all()

@ns_users.route('')
class User(Resource):

    @api.expect(user)
    def post(self):
        #defining the payload
        data = api.payload

        username = data['username']
        email = data['email']
        password = data['password']


        hashedPassword = generate_password_hash(password)
        user = UserModel(username = username, email = email, password = hashedPassword)
        user.createRecord()

        return {"message" : "Record Added Successfully"}, 201

    def get(self):

        users = UserModel.fetch_users()
        return users_schema.dump(users), 200

@ns_users.route('/<int:id>')
class User(Resource):
 
    def get(self,id):

        user = UserModel.fetch_by_id(id)
        return user_schema.dump(user)

@ns_login.route('')
class Login(Resource):

    @api.expect(login)
    def post(self):
        data = api.payload

        email = data['email']
        password = data['password']

        if UserModel.check_email_exist(email):
            
            if UserModel.check_password(email,password):

                return {"message":"Successfully logged in"}
            else:
                return {"message":"Wrong login credentials!"}
        else:
            return {"message":"Email does not exist!"}


# Handling the agendas model endpoints and results:
@ns_agenda.route('')
class Agenda(Resource):
    @api.expect(agenda)
    # adding a new agenda to db
    def post(self):
        #defining the payload
        data = api.payload

        title = data['title']
        description = data['description']
        agenda = AgendaModel(title = title, agenda = description)
        agenda.createRecord()

        return {"message" : "Record added successfully"}, 201

    #fetch all agendas in db
    def get(self):
        
        agenda = AgendaModel.fetchAgendas()
        return agendas_schema.dump(agenda), 200

#fetch an agenda by id
#first, we create a route for sending the id via get http method
@ns_agenda.route('/<int:id>')
class Agenda(Resource):
    
    def get(self, id):

        agenda = AgendaModel.fetch_agendas_by_id(id)
        return agenda_schema.dump(agenda)

            





if __name__ == "__main__":
    app.run(debug=True)