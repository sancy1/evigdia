
# views/swagger.py
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .serializers import SubscriptionPriceSerializer




# API FOR CONSUMPTION ------------------------------------------------------------------------------
def get_price_schema():
    """
    Swagger documentation decorator for get_price view
    """
    return swagger_auto_schema(
        method='post',  # Explicitly specify the method
        operation_description="""Get current price for a subscription plan.
        Required GET parameter: plan_type (monthly/yearly)
        Required POST parameter (in body): api_key""",
        manual_parameters=[
            openapi.Parameter(
                name='plan_type',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description='Subscription plan type (monthly/yearly)',
                enum=['monthly', 'yearly']
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['api_key'],
            properties={
                'api_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='API key for authentication'
                )
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Price retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        'plan_type': openapi.Schema(type=openapi.TYPE_STRING, example='monthly'),
                        'price': openapi.Schema(type=openapi.TYPE_NUMBER, example=9.99),
                        'currency': openapi.Schema(type=openapi.TYPE_STRING, example='USD'),
                        'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, example='2023-01-01T00:00:00Z'),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, example='2023-01-01T00:00:00Z'),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='plan_type parameter is required'
                        ),
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid API key'
                        ),
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Price not found for this plan type'
                        ),
                    }
                )
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal Server Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Internal server error while fetching price'
                        ),
                    }
                )
            )
        },
        tags=['Plan Type & Prices'],
        examples={
            'application/json': {
                'Valid Request': {
                    'api_key': 'your_api_key_here'
                },
                'Missing API Key': {
                    'other_field': 'value'
                }
            }
        }
    )




# Update Plan ------------------------------------------------------------------------------
def update_price_schema():
    """
    Swagger documentation decorator for update_price view
    """
    return swagger_auto_schema(
        method='put',
        operation_description="""Update price for a subscription plan.
        Required parameters in body: plan_type, api_key, price_usd
        Optional parameter: description""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['plan_type', 'api_key', 'price_usd'],
            properties={
                'plan_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Subscription plan type (monthly/yearly)',
                    enum=['monthly', 'yearly']
                ),
                'api_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='API key for authentication'
                ),
                'price_usd': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='New price in USD (must be positive)',
                    example=9.99
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Optional description of the plan',
                    nullable=True
                )
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Price updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Price for plan monthly updated successfully.'
                        ),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            examples={
                                'Missing parameter': 'plan_type parameter is required in the request body',
                                'Invalid price': 'price_usd cannot be negative',
                                'Invalid number': 'Invalid price_usd value. Must be a valid number.'
                            }
                        ),
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid API key'
                        ),
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Price not found for this plan type'
                        ),
                    }
                )
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal Server Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            examples={
                                'Fetch error': 'Internal server error while fetching price for update',
                                'Save error': 'Internal server error while saving updated price'
                            }
                        ),
                    }
                )
            )
        },
        tags=['Plan Type & Prices'],
        examples={
            'application/json': {
                'Valid Request': {
                    'plan_type': 'monthly',
                    'api_key': 'your_api_key_here',
                    'price_usd': 12.99,
                    'description': 'New monthly subscription price'
                },
                'Missing Required Field': {
                    'api_key': 'your_api_key_here',
                    'price_usd': 12.99
                },
                'Invalid Price': {
                    'plan_type': 'monthly',
                    'api_key': 'your_api_key_here',
                    'price_usd': -5.00
                }
            }
        }
    )




# Create Plan ------------------------------------------------------------------------------
# views/swagger.py
def create_price_schema():
    """
    Swagger documentation decorator for create_price view
    """
    return swagger_auto_schema(
        method='post',
        operation_description="""Create a new subscription plan price.
        Required parameters in body: plan_type, api_key, price_usd
        Optional parameter: description""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['plan_type', 'api_key', 'price_usd'],
            properties={
                'plan_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['monthly', 'yearly'],
                    description='Type of subscription plan'
                ),
                'api_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Authentication API key'
                ),
                'price_usd': openapi.Schema(
                    type=openapi.TYPE_NUMBER,
                    description='Price in USD (must be positive)',
                    example=9.99
                ),
                'description': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Optional description of the plan',
                    nullable=True
                )
            }
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Price created successfully",
                schema=SubscriptionPriceSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            examples={
                                'Missing parameter': 'plan_type parameter is required in the request body',
                                'Invalid price': 'price_usd cannot be negative',
                                'Invalid number': 'Invalid price_usd value. Must be a valid number.'
                            }
                        ),
                        'plan_type': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        ),
                        'price_usd': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING)
                        )
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid API key'
                        ),
                    }
                )
            ),
            status.HTTP_409_CONFLICT: openapi.Response(
                description="Conflict",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Price already exists for plan type: monthly. Use the update endpoint to modify.'
                        ),
                    }
                )
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal Server Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Internal server error while creating price'
                        ),
                    }
                )
            )
        },
        tags=['Plan Type & Prices'],
        examples={
            'application/json': {
                'Valid Request': {
                    'plan_type': 'monthly',
                    'api_key': 'your_api_key_here',
                    'price_usd': 12.99,
                    'description': 'New monthly subscription price'
                },
                'Missing Required Field': {
                    'api_key': 'your_api_key_here',
                    'price_usd': 12.99
                },
                'Existing Plan': {
                    'plan_type': 'monthly',
                    'api_key': 'your_api_key_here',
                    'price_usd': 12.99,
                    'description': 'This will fail if monthly exists'
                }
            }
        }
    )
    
    
    

# Fetch Single Plan ------------------------------------------------------------------------------
def get_plan_schema():
    """
    Swagger documentation decorator for get_plan view
    """
    return swagger_auto_schema(
        method='post',
        operation_description="""Get details for a specific subscription plan.
        Required URL parameter: plan_type (monthly/yearly)
        Required POST parameter (in body): api_key""",
        manual_parameters=[
            openapi.Parameter(
                name='plan_type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Subscription plan type',
                enum=['monthly', 'yearly']
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['api_key'],
            properties={
                'api_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='API key for authentication'
                )
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Plan details retrieved successfully",
                schema=SubscriptionPriceSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='api_key parameter is required in the request body'
                        ),
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid API key'
                        ),
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Plan details not found for this plan type'
                        ),
                    }
                )
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal Server Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Internal server error while fetching plan details'
                        ),
                    }
                )
            )
        },
        tags=['Plan Type & Prices'],
        examples={
            'application/json': {
                'Valid Request': {
                    'api_key': 'your_api_key_here'
                },
                'Missing API Key': {
                    'wrong_field': 'value'
                }
            }
        }
    )




# Fetch All Plan ------------------------------------------------------------------------------
def get_all_plans_schema():
    """
    Swagger documentation decorator for get_all_plans view
    """
    return swagger_auto_schema(
        method='post',
        operation_description="""Get details for all active subscription plans.
        Required POST parameter (in body): api_key""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['api_key'],
            properties={
                'api_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='API key for authentication'
                )
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Active plans retrieved successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'plan_type': openapi.Schema(type=openapi.TYPE_STRING, example='monthly'),
                            'plan_type_display': openapi.Schema(type=openapi.TYPE_STRING, example='Monthly'),
                            'price_usd': openapi.Schema(type=openapi.TYPE_NUMBER, example=9.99),
                            'description': openapi.Schema(type=openapi.TYPE_STRING, example='Monthly subscription', nullable=True),
                            'last_updated': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, example='2023-01-01T00:00:00Z'),
                            'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True)
                        }
                    )
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='api_key parameter is required in the request body'
                        ),
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid API key'
                        ),
                    }
                )
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal Server Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Internal server error while fetching all plans'
                        ),
                    }
                )
            )
        },
        tags=['Plan Type & Prices'],
        examples={
            'application/json': {
                'Valid Request': {
                    'api_key': 'your_api_key_here'
                },
                'Missing API Key': {
                    'wrong_field': 'value'
                }
            }
        }
    )




# Deactivate Plan ------------------------------------------------------------------------------
def deactivate_plan_schema():
    """
    Swagger documentation decorator for deactivate_plan view
    """
    return swagger_auto_schema(
        method='delete',
        operation_description="""Deactivate a subscription plan by marking it as inactive.
        Required URL parameter: plan_type (monthly/yearly)
        Required DELETE parameter (in body): api_key""",
        manual_parameters=[
            openapi.Parameter(
                name='plan_type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Subscription plan type to deactivate',
                enum=['monthly', 'yearly']
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['api_key'],
            properties={
                'api_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='API key for authentication'
                )
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Plan deactivated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Plan monthly has been deactivated'
                        ),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            examples={
                                'Missing API key': 'api_key parameter is required in the request body',
                                'Already inactive': 'Plan monthly is already inactive'
                            }
                        ),
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid API key'
                        ),
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Plan not found for this plan type'
                        ),
                    }
                )
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal Server Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Internal server error while deactivating plan'
                        ),
                    }
                )
            )
        },
        tags=['Plan Type & Prices'],
        examples={
            'application/json': {
                'Valid Request': {
                    'api_key': 'your_api_key_here'
                },
                'Missing API Key': {
                    'wrong_field': 'value'
                }
            }
        }
    )
    



# Re-Activate Plan ------------------------------------------------------------------------------
def reactivate_plan_schema():
    """
    Swagger documentation decorator for reactivate_plan view
    """
    return swagger_auto_schema(
        method='post',
        operation_description="""Reactivate a deactivated subscription plan.
        Required URL parameter: plan_type (monthly/yearly)
        Required POST parameter (in body): api_key""",
        manual_parameters=[
            openapi.Parameter(
                name='plan_type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='Subscription plan type to reactivate',
                enum=['monthly', 'yearly']
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['api_key'],
            properties={
                'api_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='API key for authentication'
                )
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Plan reactivated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Plan monthly has been reactivated'
                        ),
                    }
                )
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            examples={
                                'Missing API key': 'api_key parameter is required in the request body',
                                'Already active': 'Plan monthly is already active'
                            }
                        ),
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid API key'
                        ),
                    }
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Plan not found for this plan type'
                        ),
                    }
                )
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Internal Server Error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Internal server error while reactivating plan'
                        ),
                    }
                )
            )
        },
        tags=['Plan Type & Prices'],
        examples={
            'application/json': {
                'Valid Request': {
                    'api_key': 'your_api_key_here'
                },
                'Missing API Key': {
                    'wrong_field': 'value'
                }
            }
        }
    )