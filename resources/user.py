import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import JWT, jwt_required, current_identity
from models.user import UserModel


class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username",type = str,required=True, help="the field cannot be left blank")
        parser.add_argument("password", type = str,required= True, help ="the field cannot be left blank" )
        args = parser.parse_args()
        if args["username"].isspace() == True or args["password"].isspace()== True:
            return {"message":'username or password cannot be left blank'}
        elif UserModel.findByUsername(args["username"]) == None:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute('insert into users (username, password) values(?, ?)',(args['username'],args['password']))
            conn.commit()
            cur.close()
            return {"message":'user has been added'}
        return {'message':'username already exists'}
