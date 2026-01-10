

import json
import uuid
from Models.User import createUserRequest,createUserResponse ,Complete_user
from datetime import datetime

from Repository.user_managment_repository import user_managment_repository

class user_managment_repository_handler(user_managment_repository):
    
    def create_user(self, request:createUserRequest)->createUserResponse:
        ## I am not commection to DB
        ## jUst mocking the Dataase by a json file..
        User = Complete_user(**request.user.model_dump(),id = str(uuid.uuid4()),created_at = datetime.now())

        try:
            with open("Repository/USERS.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"users": []}

        user_data = User.model_dump(mode='json')
        data["users"].append(user_data)

        with open("Repository/USERS.json", "w") as f:
            json.dump(data, f)

        return createUserResponse(
            message="User created successfully",
            status=201,
            user_id=User.id
        )

        
