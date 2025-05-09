# web_apis/evigdia_services/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Service, ServiceAttachment
import os

class ServiceAttachmentInline(admin.TabularInline):
    model = ServiceAttachment
    extra = 0
    readonly_fields = ('uploaded_at', 'filename', 'extension', 'filesize')
    fields = ('file', 'uploaded_at', 'filename', 'extension', 'filesize')

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

class StatusFilter(admin.SimpleListFilter):
    title = _('status')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return Service.STATUS_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

class FileExtensionFilter(admin.SimpleListFilter):
    title = _('file extension')
    parameter_name = 'extension'

    def lookups(self, request, model_admin):
        extensions = set()
        for attachment in ServiceAttachment.objects.all():
            ext = attachment.extension()
            if ext:
                extensions.add(ext.lower())
        return [(ext, _(ext.upper())) for ext in sorted(list(extensions))]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(file__iregex=r'\.' + self.value() + '$')
        return queryset

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'display_subtitle',
        'status',
        'created_by',
        'date_posted',
        'created_at',
        'updated_at',
        'service_image_preview',
        'attachment_count'
    )
    list_filter = (StatusFilter, 'created_at', 'updated_at', 'created_by')
    search_fields = ('title', 'subtitle', 'description', 'sub_description')
    readonly_fields = (
        'created_at',
        'updated_at',
        'created_by',
        'service_image',  # Make the image field readonly
        'sub_service_image', # Make the sub-image field readonly
        'service_image_preview',
        'sub_service_image_preview'
    )
    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'title',
                'subtitle',
                'description',
                'sub_description',
                'status'
            )
        }),
        (_('Images'), {
            'fields': (
                'service_image',
                'service_image_preview',
                'sub_service_image',
                'sub_service_image_preview'
            )
        }),
        (_('Metadata'), {
            'fields': (
                'date_posted',
                'created_at',
                'updated_at',
                'created_by'
            )
        }),
    )
    inlines = [ServiceAttachmentInline]
    date_hierarchy = 'date_posted'
    list_per_page = 20
    actions = ['mark_as_published', 'mark_as_draft', 'mark_as_archived']

    def display_subtitle(self, obj):
        return obj.subtitle if obj.subtitle else '—'
    display_subtitle.short_description = _('Subtitle')

    def service_image_preview(self, obj):
        if obj.service_image and hasattr(obj.service_image, 'url'):
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.service_image.url
            )
        return '—'
    service_image_preview.short_description = _('Main Image Preview')

    def sub_service_image_preview(self, obj):
        if obj.sub_service_image and hasattr(obj.sub_service_image, 'url'):
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 100px;" />',
                obj.sub_service_image.url
            )
        return '—'
    sub_service_image_preview.short_description = _('Sub Image Preview')

    def attachment_count(self, obj):
        return obj.attachments.count()
    attachment_count.short_description = _('Attachments')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Only set created_by if creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser and obj:
            readonly_fields.append('created_by')
        return readonly_fields

    def mark_as_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} services were marked as published.')
    mark_as_published.short_description = _('Mark selected services as Published')

    def mark_as_draft(self, request, queryset):
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} services were marked as draft.')
    mark_as_draft.short_description = _('Mark selected services as Draft')

    def mark_as_archived(self, request, queryset):
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} services were marked as archived.')
    mark_as_archived.short_description = _('Mark selected services as Archived')


@admin.register(ServiceAttachment)
class ServiceAttachmentAdmin(admin.ModelAdmin):
    list_display = ('filename', 'service', 'extension', 'filesize', 'uploaded_at')
    list_filter = ('uploaded_at', FileExtensionFilter)
    search_fields = ('filename', 'service__title')
    readonly_fields = ('uploaded_at', 'filename', 'extension', 'filesize')
    date_hierarchy = 'uploaded_at'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(service__created_by=request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.has_perm('evigdia_services.add_service')

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.service.created_by == request.user
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.service.created_by == request.user
        return super().has_delete_permission(request, obj)