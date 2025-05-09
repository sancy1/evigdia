from django.contrib import admin
from .models import AppManager, GlobalAppControl


@admin.register(AppManager)
class AppManagerAdmin(admin.ModelAdmin):
    list_display = ('app_type', 'is_active', 'requires_update', 'website_url', 'created_at', 'updated_at')
    list_filter = ('is_active', 'requires_update')
    search_fields = ('app_type',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GlobalAppControl)
class GlobalAppControlAdmin(admin.ModelAdmin):
    list_display = ('is_global_shutdown', 'is_global_update', 'website_url', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_add_permission(self, request):
        # Only allow one global control instance
        return not GlobalAppControl.objects.exists()
    
    
    


# @admin.register(GlobalAppControl)
# class GlobalAppControlAdmin(admin.ModelAdmin):
#     list_display = (
#         'id',  # Add this as the first field
#         'is_global_shutdown',
#         'global_shutdown_message',
#         'is_global_update',
#         'global_update_message',
#         'website_url'
#     )
#     list_editable = (
#         'is_global_shutdown',
#         'global_shutdown_message',
#         'is_global_update',
#         'global_update_message',
#         'website_url'
#     )
#     list_display_links = ('id',)  # Only ID links to change form
    
#     def has_add_permission(self, request):
#         return not GlobalAppControl.objects.exists()