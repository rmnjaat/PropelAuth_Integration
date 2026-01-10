import json
import logging
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from propelauth_py.errors import CreateUserException, BadRequestException
from packages.auth_provider import Auth_provider
from Models.User import createUserRequest, createUserResponse, Complete_user
from Repository.user_managment_repository import user_managment_repository

# Configure logging
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "USERS.json")

class user_managment_repository_handler(user_managment_repository):
    """Handler for user management operations with PropelAuth integration."""

    auth_provider: Auth_provider
    
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
    
    def _save_user_to_file(self, user: Complete_user) -> None:

        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                data = json.loads(content) if content else {"users": []}
          
            # Append new user
            user_data = user.model_dump(mode='json')
            data["users"].append(user_data)
            
            # Write back to file with proper formatting
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            logger.debug(f"User saved to {USERS_FILE}")
            
        except Exception as e:
            logger.error(f"Failed to save user to file: {str(e)}", exc_info=True)
            raise

