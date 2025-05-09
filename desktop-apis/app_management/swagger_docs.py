
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .serializers import GlobalAppControlSerializer, AppManagerSerializer


# views/swagger.py

def global_app_control_post_schema():
    return swagger_auto_schema(
        operation_description="""Create new global control (only if none exists).
        Requires API key in headers.""",
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Global control created successfully",
                schema=GlobalAppControlSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Global control already exists. Use PUT/PATCH to update.'
                        ),
                        'field_errors': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            )
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
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['Global Control']
    )

def global_app_control_get_schema():
    return swagger_auto_schema(
        operation_description="""Get current global control.
        Will create one if none exists.
        Requires API key in headers.""",
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Global control retrieved",
                schema=GlobalAppControlSerializer
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
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['Global Control']
    )

def global_app_control_put_schema():
    return swagger_auto_schema(
        operation_description="""Full update of global control.
        Will create one if none exists.
        Requires API key in headers.""",
        request_body=GlobalAppControlSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Global control updated",
                schema=GlobalAppControlSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field_errors': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            )
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
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['Global Control']
    )

def global_app_control_patch_schema():
    return swagger_auto_schema(
        operation_description="""Partial update of global control.
        Will create one if none exists.
        Requires API key in headers.""",
        request_body=GlobalAppControlSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Global control partially updated",
                schema=GlobalAppControlSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field_errors': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            )
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
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['Global Control']
    )

def global_app_control_delete_schema():
    return swagger_auto_schema(
        operation_description="""Delete global control.
        A new one will be created on next access.
        Requires API key in headers.""",
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="Global control deleted successfully"
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
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['Global Control']
    )
    
    


# views/swagger.py

def app_manager_post_schema():
    return swagger_auto_schema(
        operation_description="""Create new app manager.
        Requires API key in headers.
        Required parameter: app_type""",
        request_body=AppManagerSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="App manager created successfully",
                schema=AppManagerSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            examples={
                                'Missing app_type': 'app_type is required',
                                'Duplicate app': 'App manager for [type] already exists'
                            }
                        ),
                        'field_errors': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            )
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
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['App Management']
    )




def app_manager_get_schema():
    return swagger_auto_schema(
        operation_description="""Get app manager(s).
        Returns single manager if app_type query parameter is provided, all managers otherwise.
        Requires API key in headers.""",
        manual_parameters=[
            openapi.Parameter(
                name='app_type',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=False,
                description='Filter by specific app type'
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="App manager(s) retrieved",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,  # Added type here for the outer schema
                    oneOf=[
                        openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'app_type': openapi.Schema(type=openapi.TYPE_STRING),
                                    # Add all other fields from your AppManagerSerializer here
                                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                                    # Include any other fields your serializer has
                                }
                            )
                        ),
                        openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'app_type': openapi.Schema(type=openapi.TYPE_STRING),
                                # Same fields as above for single object response
                            }
                        )
                    ]
                )
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,  # Add type here
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='App manager not found'
                        ),
                    }
                )
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Unauthorized",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,  # Add type here
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='Invalid API key'
                        ),
                    }
                )
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['App Management']
    )



def app_manager_put_schema():
    return swagger_auto_schema(
        operation_description="""Full update of app manager.
        Requires API key in headers.
        Required URL parameter: app_type""",
        manual_parameters=[
            openapi.Parameter(
                name='app_type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='App type to update'
            )
        ],
        request_body=AppManagerSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="App manager updated",
                schema=AppManagerSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field_errors': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            )
                        )
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
                            example='App manager not found'
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
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['App Management']
    )



def app_manager_patch_schema():
    return swagger_auto_schema(
        operation_description="""Partial update of app manager.
        Requires API key in headers.
        Required URL parameter: app_type""",
        manual_parameters=[
            openapi.Parameter(
                name='app_type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='App type to update'
            )
        ],
        request_body=AppManagerSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="App manager partially updated",
                schema=AppManagerSerializer
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad Request",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'field_errors': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING)
                            )
                        )
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
                            example='App manager not found'
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
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['App Management']
    )



def app_manager_delete_schema():
    return swagger_auto_schema(
        operation_description="""Delete app manager.
        Requires API key in headers.
        Required URL parameter: app_type""",
        manual_parameters=[
            openapi.Parameter(
                name='app_type',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description='App type to delete'
            )
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description="App manager deleted successfully"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Not Found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example='App manager not found'
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
            )
        },
        security=[{'APIKeyHeader': []}],
        tags=['App Management']
    )
    
    
    
    





def app_status_check_schema():
    return swagger_auto_schema(
        operation_description="""Check status of apps.
        Requires API key in request body.
        Returns global status and individual app statuses.""",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['api_key'],
            properties={
                'api_key': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='API key for authentication'
                ),
                'app_types': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='Specific app types to check (optional)'
                )
            }
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Status check successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'global': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'is_shutdown': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'shutdown_message': openapi.Schema(type=openapi.TYPE_STRING),
                                'requires_update': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                'update_message': openapi.Schema(type=openapi.TYPE_STRING),
                                'website_url': openapi.Schema(type=openapi.TYPE_STRING)
                            }
                        ),
                        'apps': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'requires_update': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'shutdown_message': openapi.Schema(type=openapi.TYPE_STRING),
                                    'update_message': openapi.Schema(type=openapi.TYPE_STRING),
                                    'website_url': openapi.Schema(type=openapi.TYPE_STRING)
                                }
                            )
                        )
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
            )
        },
        tags=['App Status']
    )