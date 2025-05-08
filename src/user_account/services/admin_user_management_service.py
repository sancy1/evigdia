
import logging
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from ..exceptions.custom_exceptions import UserNotFoundError, UpdateOperationError 

logger = logging.getLogger(__name__)
User = get_user_model()

class AdminUserManagementService:
    @staticmethod
    def update_user_role(user_id, role):
        try:
            user = User.objects.get(id=user_id)
            if role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            elif role == 'staff':
                user.is_staff = True
                user.is_superuser = False
            elif role == 'user':
                user.is_staff = False
                user.is_superuser = False
            else:
                raise ValueError(f"Invalid role: {role}")
            user.save()
            return user
        except User.DoesNotExist:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        except IntegrityError as e:
            logger.error(f"Error updating role for user {user_id}: {str(e)}")
            raise UpdateOperationError(f"Could not update role for user {user_id} due to database error.")
        except Exception as e:
            logger.error(f"Unexpected error updating role for user {user_id}: {str(e)}")
            raise UpdateOperationError("Failed to update user role.")

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserNotFoundError(f"User with ID {user_id} not found.") # Raised as exception
        except Exception as e:
            logger.error(f"Error fetching user with ID {user_id}: {str(e)}")
            raise

    @staticmethod
    def get_all_users():
        try:
            return User.objects.all()
        except Exception as e:
            logger.error(f"Error fetching all users: {str(e)}")
            raise