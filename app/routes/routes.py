from bson import json_util
from flask import request, Response

from app import app
from app.middleware.auth_middleware import token_required
from app.modules.TODO.TODOservice import TODOService
from app.modules.user.user_management import UserService


@app.route("/", methods=["GET"])
def index():
    return "TODO system"

#Authentication Services

#Here User registers into the app and its data is stored in database ,If the user with same email already exists,it will return error
# body::{
#     "email":"abcd@gmail.com",
#     "password":"123456"
# }
#we add jwt_token as empty in user document
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if data is None or data == {}:
        return Response(response=json_util.dumps({"Error": "Please provide  information"}),
                        status=400, mimetype='application/json')
    response = UserService().register(data)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


#we get email and password as input
#Here we search the user by its email and password,then we use jwt token to encode the info and for authentication
#we add this token feature to jwt_token in user document
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data is None or data == {}:
        return Response(response=json_util.dumps({"Error": "Please provide  information"}),
                        status=400, mimetype='application/json')
    response = UserService().login(data)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


#Here we can get currentuser by its id
@app.route('/get_user', methods=['POST'])
@token_required
def get_user(current_user):
    return Response(response=json_util.dumps(current_user), status=200,
                    mimetype='application/json')


#Here user logs out and the jwt_token option will be blank
@app.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    response=UserService.logout(current_user)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')




#TODO Services
# Create MongoDB Document TODO, through API and METHOD - POST
# body::{
#     "title":"This is title",
#     "description":"This is description"
# }
#Initially the tasks are incomplete and we add userid for referencing
@app.route('/add_TODO', methods=['POST'])  
@token_required
def add_TODO(current_user):
    data = request.json
    print(current_user)
    response = TODOService.add_TODO(data,current_user['_id'])
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


# Marks the particular todo as complete, through API and METHOD - POST
@app.route('/check_TODO/<TODO_id>', methods=['POST']) 
@token_required    
def check_TODO(current_user,TODO_id):
    response = TODOService.check_TODO(TODO_id,current_user['_id'])
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


#Updates the todo list item by its id ,through API and METHOD - POST
@app.route('/update_TODO/<TODO_id>', methods=['POST']) 
@token_required    
def update_TODO(current_user,TODO_id):
    data = request.json
    response = TODOService.update_TODO(TODO_id,data,current_user['_id'])
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


#deletes the entire todo list of a user by its userid ,through API and METHOD - POST
@app.route('/delete_TODO', methods=['POST']) 
@token_required    
def delete_TODO(current_user):
    response = TODOService.delete_TODO(current_user['_id'])
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


#deletes the todo list item by its todo_id ,through API and METHOD - POST
@app.route('/delete_one_TODO/<TODO_id>', methods=['POST']) 
@token_required    
def delete_one_TODO(current_user,TODO_id):
#  data = request.json
    response = TODOService.delete_one_TODO(TODO_id,current_user['_id'])
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')


#gets all the items in todo list ,through API and METHOD - GET
@app.route('/get_TODO', methods=['GET'])
@token_required
def get_TODO(current_user):
    response = TODOService().get_TODO(current_user['_id'])
    print(response)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')     


#gets all the completed items in todo list ,through API and METHOD - GET
@app.route('/get_checked_TODO', methods=['GET'])
@token_required
def get_checked_TODO(current_user):
    response = TODOService().get_checked_TODO(current_user['_id'])
    print(response)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')     


#gets all the incompleted items in todo list ,through API and METHOD - GET
@app.route('/get_unchecked_TODO', methods=['GET'])
@token_required
def get_unchecked_TODO(current_user):
    response = TODOService().get_unchecked_TODO(current_user['_id'])
    print(response)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')     


#gets one of the items in todo list by todo_id,through API and METHOD - GET
@app.route('/get_one_TODO/<TODO_id>', methods=['GET'])
@token_required
def get_one_TODO(current_user,TODO_id):
    response = TODOService().get_one_TODO(TODO_id,current_user['_id'])
    print(response)
    return Response(response=json_util.dumps(response), status=200,
                    mimetype='application/json')                                                                                
                    
