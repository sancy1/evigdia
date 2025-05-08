
# # blog/views/utils.py

# from rest_framework.response import Response
# from rest_framework import status

# class DeactivationHandlerMixin:
#     """
#     Mixin for soft deletion (deactivation) with JSON success messages
#     Usage: Inherit this mixin in your ViewSet
#     """
    
#     # Field name to use for deactivation (default is 'is_active')
#     deactivation_field = 'is_active'
    
#     # Message template - customize in child classes if needed
#     deactivation_message = '{model_name} "{instance_name}" has been deactivated successfully.'
    
#     def perform_destroy(self, instance):
#         """Perform soft delete by setting is_active=False"""
#         setattr(instance, self.deactivation_field, False)
#         instance.save()
    
#     def get_deactivation_message(self, instance):
#         """Generate the success message"""
#         return self.deactivation_message.format(
#             model_name=instance.__class__.__name__,
#             instance_name=str(instance)
#         )  # This was the missing closing parenthesis
    
#     def destroy(self, request, *args, **kwargs):
#         """Override default destroy to return success message"""
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(
#             {'status': self.get_deactivation_message(instance)},
#             status=status.HTTP_200_OK
#         )