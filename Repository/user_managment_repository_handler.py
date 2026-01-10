import json
import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from propelauth_py.errors import CreateUserException, BadRequestException
from packages.auth_provider import Auth_provider
from Models.User import createUserRequest, createUserResponse, updateUserRequest, updateUserResponse, deleteUserResponse, Complete_user
from Repository.user_managment_repository import user_managment_repository

# Configure logging
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "USERS.json")

class user_managment_repository_handler(user_managment_repository):
    """Handler for user management operations with PropelAuth integration."""

    auth_provider: Auth_provider
    
    ## can't  check authorization , Because permission mapping is not  available in free version 
    ## alternative can Put check for is_admin(org_id)  or is_owner(org_id)  but not best way to do this ...
    def create_user(self, request: createUserRequest) -> createUserResponse:
        try:
            # Get PropelAuth client
            propel_client = self.auth_provider.get_client()
            
            # Create user in PropelAuth
            logger.info(f"Creating user in PropelAuth: {request.user.email}")
            propel_user = propel_client.create_user(
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
                password=request.user.password,
                # PropelAuth configuration
                email_confirmed=False,
                send_email_to_confirm_email_address=True,
                ask_user_to_update_password_on_login=False,
            )
            
            # Add user to organization
            logger.info(f"Adding user {propel_user.user_id} to org {request.user.orgId}")
            propel_client.add_user_to_org(
                user_id=propel_user.user_id,
                org_id=request.user.orgId,
                role=request.user.role,
            )
            
            # Create complete user object with PropelAuth user_id
            complete_user = Complete_user(
                **request.user.model_dump(),
                id=propel_user.user_id,  # Fixed: was propel_client.user_id
                created_at=datetime.now()
            )
            
            # Save to JSON file (mock database)
            self._save_user_to_file(complete_user)
            
            logger.info(f"User created successfully: {complete_user.id}")
            return createUserResponse(
                message="User created successfully",
                status=201,
                user_id=complete_user.id
            )
            
        except CreateUserException as e:
            # Handle PropelAuth user creation validation errors
            error_details = str(e)
            logger.error(f"PropelAuth validation error: {error_details}")
            raise HTTPException(
                status_code=400,
                detail=f"User creation failed: {error_details}"
            )
            
        except BadRequestException as e:
            # Handle PropelAuth organization/role errors
            error_details = str(e)
            logger.error(f"PropelAuth bad request error: {error_details}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid request: {error_details}"
            )
            
        except Exception as e:
            logger.error(f"Failed to create user: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    def update_user(self, user_id: str, request: updateUserRequest) -> updateUserResponse:
        try:
            propel_client = self.auth_provider.get_client()
            
            # Prepare update data for PropelAuth metadata
            update_kwargs = {}
            if request.first_name: update_kwargs["first_name"] = request.first_name
            if request.last_name: update_kwargs["last_name"] = request.last_name
            if request.email: update_kwargs["email"] = request.email

            # Handle Role Update
            if request.role:
                if not request.orgId:
                    raise HTTPException(status_code=400, detail="orgId is required to change user role")
                
                logger.info(f"Changing role for user {user_id} in org {request.orgId} to {request.role}")
                propel_client.change_user_role_in_org(
                    user_id=user_id,
                    org_id=request.orgId,
                    role=request.role
                )
                update_kwargs["role"] = request.role
                update_kwargs["orgId"] = request.orgId

            if not update_kwargs:
                return updateUserResponse(message="No fields to update", status=200)

            # Update Metadata in PropelAuth (if any metadata fields changed)
            metadata_fields = {k: v for k, v in update_kwargs.items() if k in ["first_name", "last_name", "email"]}
            if metadata_fields:
                logger.info(f"Updating user metadata in PropelAuth: {user_id}")
                propel_client.update_user_metadata(user_id=user_id, **metadata_fields)
            
            # Update in JSON file
            self._update_user_in_file(user_id, update_kwargs)
            
            return updateUserResponse(message="User updated successfully", status=200)
            
        except Exception as e:
            logger.error(f"Failed to update user {user_id}: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

    def delete_user(self, user_id: str) -> deleteUserResponse:
        try:
            propel_client = self.auth_provider.get_client()
            
            # Delete from PropelAuth
            logger.info(f"Deleting user from PropelAuth: {user_id}")
            propel_client.delete_user(user_id=user_id)
            
            # Delete from JSON file
            self._delete_user_from_file(user_id)
            
            return deleteUserResponse(message="User deleted successfully", status=200)
            
        except Exception as e:
            logger.error(f"Failed to delete user {user_id}: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
    
    def _save_user_to_file(self, user: Complete_user) -> None:
        try:
            data = self._read_file()
            user_data = user.model_dump(mode='json')
            data["users"].append(user_data)
            self._write_file(data)
            logger.debug(f"User saved to {USERS_FILE}")
        except Exception as e:
            logger.error(f"Failed to save user to file: {str(e)}", exc_info=True)
            raise

    def _update_user_in_file(self, user_id: str, update_data: dict) -> None:
        try:
            data = self._read_file()
            for user in data.get("users", []):
                if user["id"] == user_id:
                    user.update(update_data)
                    break
            self._write_file(data)
        except Exception as e:
            logger.error(f"Failed to update user in file: {str(e)}")
            raise

    def _delete_user_from_file(self, user_id: str) -> None:
        try:
            data = self._read_file()
            data["users"] = [u for u in data.get("users", []) if u["id"] != user_id]
            self._write_file(data)
        except Exception as e:
            logger.error(f"Failed to delete user from file: {str(e)}")
            raise

    def _read_file(self) -> dict:
        if not os.path.exists(USERS_FILE):
            return {"users": []}
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else {"users": []}

    def _write_file(self, data: dict) -> None:
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

