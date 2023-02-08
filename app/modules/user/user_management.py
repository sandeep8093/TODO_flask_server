import string
import random
import jwt
from app.model.db import ConnectDB

connection = ConnectDB()
mongodb_connection = connection.connect_db()

class UserService:

    def __init__(self, email='', password=''):
        self.email = email
        self.password = password
        

    def register(self,data):
        users = mongodb_connection.todolist["users"]
        if data["email"]!=None and data["password"]!=None :
            already_registered=users.find_one({"email":data['email']})
            if already_registered:
                return {'already registered with this mail '}
            else:  
                data['jwt_token']=' '  
                users.insert_one(data)
                return {'Status': 'Successfully Registered','data':data}
        else:
            return {"Please fill the required fields for user"}
       

    def login(self, data):
        users = mongodb_connection.todolist["users"]
        email = data["email"]
        password =data["password"]
        my_secret='hello world'
        
        registered_user=users.find_one({"email":email})
        if registered_user==None:
            return {"email is not registered"}
        else:
            if password!=registered_user['password']:
                return {"wrong password"}
            else:
                payload={
                    "password":registered_user['password'],
                    "email":registered_user['email'],
                }
                
                token = jwt.encode(
                    payload,
                    my_secret, algorithm="HS256"
                )
                newvalues = { "$set": { "jwt_token":token } }
                users.update_one(registered_user, newvalues)
                return {"status": "success", "data": payload ,"token":token}
    
    def get_user(self,data):
        users = mongodb_connection.todolist["users"]
        if data!=None:
            req_user=users.find_one({"email":data})
            return req_user
        else:
            return {"Please give the correct id for user"}  

    def logout(current_user):
        users = mongodb_connection.todolist["users"]
        newvalues = { "$set": { "jwt_token":'' } }
        users.update_one(current_user, newvalues)
        return {"status":"Successfully logged out","user":current_user}
