import json
from bson.objectid import ObjectId
from app.model.db import ConnectDB

#Fetching connection to Mongodb
connection = ConnectDB()
mongodb_connection = connection.connect_db()

class TODOService:
   
    def add_TODO( data,user_id):    
        TODOs = mongodb_connection.todolist["TODOs"]
        data['user_id']=user_id
        data['is_completed']=0
        TODOs.insert_one(data)
        output = {'Status': 'Successfully Inserted','data':data}
        return output

    def check_TODO(TODO_id,user_id):          
        TODO = mongodb_connection.todolist["TODOs"]
        users = mongodb_connection.todolist["users"]
        req_user=users.find_one({"_id":ObjectId(user_id)})
        if req_user:
            res = TODO.update_one(
            {"_id":ObjectId(TODO_id),"user_id":ObjectId(user_id)} ,
            {
                "$set": {"is_completed":1}
            }
            )
            return {"successfully completed"}              
        else:
            return {"user not available"}    

    def get_TODO(self,user_id):                 
        TODOs = mongodb_connection.todolist["TODOs"]
        documents = TODOs.find({"user_id":ObjectId(user_id)})
        return {'TODOs':documents}

    def get_checked_TODO(self,user_id):                 
        TODOs = mongodb_connection.todolist["TODOs"]
        documents = TODOs.find({"user_id":ObjectId(user_id),"is_completed":1})
        return {'Completed TODOs':documents}

    def get_unchecked_TODO(self,user_id):                 
        TODOs = mongodb_connection.todolist["TODOs"]
        documents = TODOs.find({"is_completed":0,"user_id":ObjectId(user_id)})
        return {'Unchecked TODOs':documents}        

    def get_one_TODO(self,id,user_id):                 
        TODOs = mongodb_connection.todolist["TODOs"]
        objInstance = ObjectId(id)
        documents = TODOs.find_one({"_id":objInstance,"user_id":ObjectId(user_id)})
        if documents:
            return {'Requested TODO':documents}   
        else:
            return {'TODO not found'}     

    def update_TODO(TODO_id,data,user_id):          
        TODO = mongodb_connection.todolist["TODOs"]
        users = mongodb_connection.todolist["users"]
        req_user=users.find_one({"_id":ObjectId(user_id)})
        if req_user:
            res = TODO.update_one(
            {"_id":ObjectId(TODO_id),"user_id":ObjectId(user_id)} ,
            {
                "$set": data
            }
            )
            return {"successfully updated"}              
        else:
            return {"user not available"}
      

    def delete_one_TODO(id,user_id):          
        TODOs = mongodb_connection.todolist["TODOs"]
        users = mongodb_connection.todolist["users"]
        req=TODOs.find_one({"_id":ObjectId(id),"user_id":ObjectId(user_id)})
        objInstance = ObjectId(id)
        if req:
            res = TODOs.delete_one({"_id": objInstance,"user_id":ObjectId(user_id)})
            return {"successfully deleted"}
        else:
            return {"user/list not available"}  

    
    def delete_TODO(user_id):          
        TODOs = mongodb_connection.todolist["TODOs"]
        users = mongodb_connection.todolist["users"]
        req_user=users.find_one({"_id":ObjectId(user_id)})
        if req_user:
            res = TODOs.delete_many({"user_id":ObjectId(user_id)})
            return {"successfully deleted",res}
        else:
            return {"user not available"}          
              


