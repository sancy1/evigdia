
import logging
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from ..models import Profile
# from ...payments.models import Payment, Subscription, ActivationKey, HardwareProfile 
from ..exceptions.custom_exceptions import DeleteOperationError, UserNotFoundError

logger = logging.getLogger(__name__)
User = get_user_model()


class AdminUserDeletionService:
    @staticmethod
    def delete_user_and_related_data(user):
        deleted_objects = [
            {"model": "Profile", "count": Profile.objects.filter(user=user).count()},
            # {"model": "Payment", "count": Payment.objects.filter(user=user).count()},
            # {"model": "Subscription", "count": Subscription.objects.filter(user=user).count()},
            # {"model": "ActivationKey", "count": ActivationKey.objects.filter(user=user).count()},
            # {"model": "HardwareProfile", "count": HardwareProfile.objects.filter(user=user).count()},
            # Add any other models you want to track
        ]
        total_deleted = sum(item['count'] for item in deleted_objects) + 1  # +1 for the user account itself
        user_id = user.id
        user_email = user.email
        user_username = user.username

        Profile.objects.filter(user=user).delete()
        # Payment.objects.filter(user=user).delete()
        # Subscription.objects.filter(user=user).delete()
        # ActivationKey.objects.filter(user=user).delete()
        # HardwareProfile.objects.filter(user=user).delete()
        user.delete()

        return {
            "user": {"id": user_id, "email": user_email, "username": user_username, "deleted": True},
            "deleted_objects": deleted_objects,
            "total_deleted": total_deleted,
            "timestamp": timezone.now().isoformat() + "Z",
            "deletion_complete": True
        }


    @staticmethod
    def delete_all_users_except_admin():
        try:
            with transaction.atomic():
                users_to_delete = User.objects.exclude(is_staff=True, is_superuser=True)
                deleted_count = 0
                for user in users_to_delete:
                    AdminUserDeletionService.delete_user_and_related_data(user)
                    deleted_count += 1
                return deleted_count
        except Exception as e:
            logger.error(f"Error deleting all users except admin: {str(e)}")
            raise DeleteOperationError("Failed to delete all users except admin.")


    @staticmethod
    def delete_single_user(user_id):
        try:
            user_to_delete = User.objects.get(id=user_id)
            return AdminUserDeletionService.delete_user_and_related_data(user_to_delete)
        except User.DoesNotExist:
            raise UserNotFoundError(f"User with ID {user_id} not found.")
        except Exception as e:
            logger.error(f"Error deleting user with ID {user_id}: {str(e)}")
            raise DeleteOperationError(f"Failed to delete user with ID {user_id}.")


    @staticmethod
    def delete_unverified_users():
        try:
            with transaction.atomic():
                unverified_users = User.objects.filter(is_verified=False)
                deleted_count = 0
                for user in unverified_users:
                    AdminUserDeletionService.delete_user_and_related_data(user)
                    deleted_count += 1
                return deleted_count
        except Exception as e:
            logger.error(f"Error deleting unverified users: {str(e)}")
            raise DeleteOperationError("Failed to delete all unverified users.")
