
# price_api/views.py
import logging
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import SubscriptionPrice
from .serializers import SubscriptionPriceSerializer
from django.conf import settings  # Import settings
from decimal import Decimal
from django.db import IntegrityError

from .swagger_docs import (
    get_price_schema,
    update_price_schema,
    create_price_schema,
    get_plan_schema,
    get_all_plans_schema,
    deactivate_plan_schema,
    reactivate_plan_schema
)

logger = logging.getLogger(__name__)

@get_price_schema()
@api_view(['POST'])  # Expecting API key in the body
@authentication_classes([])
@permission_classes([])

def get_price(request):
    """
    Get current price for a subscription plan.
    Required GET parameter: plan_type (monthly/yearly)
    Required POST parameter (in body): api_key
    """
    plan_type = request.query_params.get('plan_type')
    api_key = request.data.get('api_key')

    if not plan_type:
        return Response(
            {"error": "plan_type parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not api_key:
        return Response(
            {"error": "api_key parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if api_key != settings.PRICE_API_KEY:
        logger.warning(f"Invalid API key: {api_key}")
        return Response(
            {"error": "Invalid API key"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        price = SubscriptionPrice.objects.get(
            plan_type=plan_type,
            is_active=True
        )
        serializer = SubscriptionPriceSerializer(price)
        return Response(serializer.data)
    except SubscriptionPrice.DoesNotExist:
        logger.warning(f"Price not found for plan_type: {plan_type}")
        return Response(
            {"error": "Price not found for this plan type"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error fetching price for plan_type '{plan_type}': {str(e)}")
        return Response(
            {"error": "Internal server error while fetching price"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



# Update Plan ------------------------------------------------------------------------------
@update_price_schema()
@api_view(['PUT'])
@authentication_classes([])
@permission_classes([])
def update_price(request):
    """Handles the PUT request to update price."""
    plan_type = request.data.get('plan_type')
    api_key = request.data.get('api_key')
    price_usd = request.data.get('price_usd')
    description = request.data.get('description', None)  # Optional description

    if not plan_type:
        return Response(
            {"error": "plan_type parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not api_key:
        return Response(
            {"error": "api_key parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not price_usd:
        return Response(
            {"error": "price_usd parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        price_usd = Decimal(str(price_usd))  # Convert to decimal
        if price_usd < 0:
            return Response(
                {"error": "price_usd cannot be negative."},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception:
        return Response(
            {"error": "Invalid price_usd value. Must be a valid number."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if api_key != settings.PRICE_API_KEY:
        logger.warning(f"Invalid API key: {api_key}")
        return Response(
            {"error": "Invalid API key"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        subscription_plan = SubscriptionPrice.objects.get(plan_type=plan_type, is_active=True)
    except SubscriptionPrice.DoesNotExist:
        logger.warning(f"Price not found for plan_type: {plan_type} during update attempt.")
        return Response(
            {"error": "Price not found for this plan type"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        logger.error(f"Error fetching price for update (plan_type: {plan_type}): {str(e)}")
        return Response(
            {"error": "Internal server error while fetching price for update"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    subscription_plan.price_usd = price_usd
    if description is not None:
        subscription_plan.description = description

    try:
        subscription_plan.save()
        logger.info(f"Price for plan {plan_type} updated to {price_usd}, description: {description}")
        return Response(
            {"message": f"Price for plan {plan_type} updated successfully."},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.error(f"Error saving updated price for plan {plan_type}: {str(e)}")
        return Response(
            {"error": "Internal server error while saving updated price"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



# Create Plan ------------------------------------------------------------------------------
@create_price_schema()
@api_view(['POST'])  # Expecting API key in the body
@authentication_classes([])
@permission_classes([])
def create_price(request):
    """Handles the POST request to create a new price."""
    plan_type = request.data.get('plan_type')
    api_key = request.data.get('api_key')
    price_usd = request.data.get('price_usd')
    description = request.data.get('description', None)  # Optional description

    if not plan_type:
        return Response(
            {"error": "plan_type parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not api_key:
        return Response(
            {"error": "api_key parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )
    if not price_usd:
        return Response(
            {"error": "price_usd parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if api_key != settings.PRICE_API_KEY:
        logger.warning(f"Invalid API key: {api_key} during create attempt.")
        return Response(
            {"error": "Invalid API key"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        price_usd = Decimal(str(price_usd))  # Convert to decimal
        if price_usd < 0:
            return Response(
                {"error": "price_usd cannot be negative."},
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception:
        return Response(
            {"error": "Invalid price_usd value. Must be a valid number."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Check if a price already exists for this plan type
        if SubscriptionPrice.objects.filter(plan_type=plan_type).exists():
            return Response(
                {"error": f"Price already exists for plan type: {plan_type}. Use the update endpoint to modify."},
                status=status.HTTP_409_CONFLICT  # HTTP 409 Conflict
            )

        serializer = SubscriptionPriceSerializer(data={'plan_type': plan_type, 'price_usd': price_usd, 'description': description})
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Price created for plan {plan_type} with price {price_usd}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Validation error during price creation for plan {plan_type}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except IntegrityError:
        logger.error(f"Integrity error while creating price for plan {plan_type}. This might be due to a unique constraint violation.")
        return Response(
            {"error": f"Could not create price for plan type: {plan_type}. A price for this plan type might already exist."},
            status=status.HTTP_409_CONFLICT
        )
    except Exception as e:
        logger.error(f"Error creating price for plan {plan_type}: {str(e)}")
        return Response(
            {"error": "Internal server error while creating price"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



# Fetch Single Plan ------------------------------------------------------------------------------
@get_plan_schema()
@api_view(['POST'])  # Expecting API key in the body
@authentication_classes([])
@permission_classes([])
def get_plan(request, plan_type):
    """
    Get details for a specific subscription plan.
    Required URL parameter: plan_type (monthly/yearly)
    Required POST parameter (in body): api_key
    """
    api_key = request.data.get('api_key')

    if not api_key:
        return Response(
            {"error": "api_key parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if api_key != settings.PRICE_API_KEY:
        logger.warning(f"Invalid API key: {api_key}")
        return Response(
            {"error": "Invalid API key"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        plan = SubscriptionPrice.objects.get(plan_type=plan_type, is_active=True)
        serializer = SubscriptionPriceSerializer(plan)
        return Response(serializer.data)
    except SubscriptionPrice.DoesNotExist:
        logger.warning(f"Plan details not found for plan_type: {plan_type}")
        return Response(
            {"error": "Plan details not found for this plan type"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error fetching plan details for {plan_type}: {str(e)}")
        return Response(
            {"error": "Internal server error while fetching plan details"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



# Fetch All Plan ------------------------------------------------------------------------------
@get_all_plans_schema()
@api_view(['POST'])  # Expecting API key in the body
@authentication_classes([])
@permission_classes([])
def get_all_plans(request):
    """
    Get details for all active subscription plans.
    Required POST parameter (in body): api_key
    """
    api_key = request.data.get('api_key')

    if not api_key:
        return Response(
            {"error": "api_key parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if api_key != settings.PRICE_API_KEY:
        logger.warning(f"Invalid API key: {api_key}")
        return Response(
            {"error": "Invalid API key"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        plans = SubscriptionPrice.objects.filter(is_active=True)
        serializer = SubscriptionPriceSerializer(plans, many=True)
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching all active plans: {str(e)}")
        return Response(
            {"error": "Internal server error while fetching all plans"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        

# Deactivate Plan ------------------------------------------------------------------------------
@deactivate_plan_schema()
@api_view(['DELETE'])
@authentication_classes([])
@permission_classes([])
def deactivate_plan(request, plan_type):
    """
    Deactivate a subscription plan by marking it as inactive.
    Required URL parameter: plan_type (monthly/yearly)
    Required DELETE parameter (in body): api_key
    """
    api_key = request.data.get('api_key')

    if not api_key:
        return Response(
            {"error": "api_key parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if api_key != settings.PRICE_API_KEY:
        logger.warning(f"Invalid API key: {api_key}")
        return Response(
            {"error": "Invalid API key"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        plan = SubscriptionPrice.objects.get(plan_type=plan_type)
        
        if not plan.is_active:
            return Response(
                {"error": f"Plan {plan_type} is already inactive"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        plan.is_active = False
        plan.save()
        
        logger.info(f"Plan {plan_type} deactivated")
        return Response(
            {"message": f"Plan {plan_type} has been deactivated"},
            status=status.HTTP_200_OK
        )
            
    except SubscriptionPrice.DoesNotExist:
        logger.warning(f"Plan not found for deactivation (plan_type: {plan_type})")
        return Response(
            {"error": "Plan not found for this plan type"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error deactivating plan {plan_type}: {str(e)}")
        return Response(
            {"error": "Internal server error while deactivating plan"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
        

# Re-Activate Plan ------------------------------------------------------------------------------
@reactivate_plan_schema()
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def reactivate_plan(request, plan_type):
    """
    Reactivate a deactivated subscription plan.
    Required URL parameter: plan_type (monthly/yearly)
    Required POST parameter (in body): api_key
    """
    api_key = request.data.get('api_key')

    if not api_key:
        return Response(
            {"error": "api_key parameter is required in the request body"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if api_key != settings.PRICE_API_KEY:
        logger.warning(f"Invalid API key: {api_key}")
        return Response(
            {"error": "Invalid API key"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        plan = SubscriptionPrice.objects.get(plan_type=plan_type)
        
        if plan.is_active:
            return Response(
                {"error": f"Plan {plan_type} is already active"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        plan.is_active = True
        plan.save()
        
        logger.info(f"Plan {plan_type} reactivated")
        return Response(
            {"message": f"Plan {plan_type} has been reactivated"},
            status=status.HTTP_200_OK
        )
            
    except SubscriptionPrice.DoesNotExist:
        logger.warning(f"Plan not found for reactivation (plan_type: {plan_type})")
        return Response(
            {"error": "Plan not found for this plan type"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f"Error reactivating plan {plan_type}: {str(e)}")
        return Response(
            {"error": "Internal server error while reactivating plan"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )