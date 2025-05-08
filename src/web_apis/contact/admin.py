

# web_apis/contact/admin.py

from django.contrib import admin
from django.urls import reverse
from django.utils import timezone  # Import timezone
from .models import Contact, ContactAttachment
from django.db.models import Q
from .serializers import ContactSerializer  # Import your serializer (for consistency)

class ContactAttachmentInline(admin.TabularInline):
    """
    Inline admin for ContactAttachment within Contact admin.
    """
    model = ContactAttachment
    extra = 0  # Number of empty forms to display
    readonly_fields = ['file_link', 'uploaded_at', 'file_size']
    fields = ['file_link', 'uploaded_at', 'file_size']
    # No 'add' permission in the inline, as attachments are created via the Contact form.
    def has_add_permission(self, request, obj=None):
        return False

    def file_link(self, obj):
        if obj.file:
            # Return the URL for the file.  Django Admin will handle the link in its templates.
            return obj.file.url
        return "-"
    file_link.short_description = "File"

    def file_size(self, obj):
        return f"{obj.filesize() / 1024:.1f} KB" if obj.filesize() else "-"
    file_size.short_description = "Size"


class ContactStatusFilter(admin.SimpleListFilter):
    """
    Custom filter for Contact status (New, Processed, Urgent).
    """
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('new', 'New (unprocessed)'),
            ('processed', 'Processed'),
            ('urgent', 'Urgent (High/Critical)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'new':
            return queryset.filter(is_processed=False)
        if self.value() == 'processed':
            return queryset.filter(is_processed=True)
        if self.value() == 'urgent':
            return queryset.filter(Q(urgency_level='high') | Q(urgency_level='critical'))


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin interface for the Contact model.
    """
    # Use fields from ContactSerializer for consistency
    readonly_fields = list(ContactSerializer.Meta.read_only_fields) + ['processed_date', 'processed_by', 'contact_details', 'message_preview']
    # list_display and fieldsets adapted from serializer fields for better admin presentation
    list_display = [
        'truncated_subject',  # Custom method for truncated subject
        'contact_person',     # Custom method for formatted name/email
        'contact_method',     # Custom method for contact method display
        'urgency_level',      # Custom method for urgency level display
        'submission_date',
        'processed_status',   # Custom method for processing status
        'attachment_count'   # Custom method for attachment count
    ]
    list_filter = [
        ContactStatusFilter,         # Custom filter
        'preferred_contact_method',
        'urgency_level',
        'submission_date',
        'is_processed'
    ]
    search_fields = [
        'full_name',
        'email',
        'phone_number',
        'subject',
        'message_content'
    ]
    # Correctly formatted fieldsets (all tuples)
    fieldsets = (
        ('Contact Information', {
            'fields': (
                'contact_details',  # Custom method for combined contact info
                ('full_name', 'email', 'phone_number'),
            ),
        }),
        ('Submission Details', {
            'fields': (
                'subject',
                'message_preview',  # Custom method for message preview
                ('preferred_contact_method', 'urgency_level'),
                'privacy_policy_accepted',
            ),
        }),
        ('Metadata', {
            'fields': (
                ('submission_date', 'is_processed'),
                ('processed_date', 'processed_by'),
                ('ip_address', 'user_agent'),
                ('referrer_url', 'browser_language'),
            ),
            'classes': ('collapse',),
        }),
    )
    inlines = [ContactAttachmentInline]
    actions = ['mark_as_processed', 'mark_as_unprocessed']
    date_hierarchy = 'submission_date'
    list_per_page = 20
    list_select_related = True

    # Custom display methods (modified to remove HTML)
    def contact_details(self, obj):
        return {
            'name': obj.full_name,
            'email': obj.email,
            'phone_number': obj.phone_number,
        }
    contact_details.short_description = "Contact"

    def message_preview(self, obj):
        return obj.message_content[:100] + "..." if len(obj.message_content) > 100 else obj.message_content
    message_preview.short_description = "Message Preview"

    def truncated_subject(self, obj):
        return obj.subject[:50] + '...' if len(obj.subject) > 50 else obj.subject
    truncated_subject.short_description = "Subject"
    truncated_subject.admin_order_field = 'subject'  # Make it sortable

    def contact_person(self, obj):
        return {
            'name': obj.full_name,
            'email': obj.email,
        }
    contact_person.short_description = "Contact Person"

    def contact_method(self, obj):
        methods = {
            'email': 'Email',
            'phone': 'Phone',
            'either': 'Either'
        }
        return methods.get(obj.preferred_contact_method, obj.preferred_contact_method)
    contact_method.short_description = "Contact Method"

    def urgency_badge(self, obj):
        return obj.get_urgency_level_display()

    urgency_badge.short_description = "Urgency"
    urgency_badge.admin_order_field = 'urgency_level'  # Make it sortable

    def processed_status(self, obj):
        return "Processed" if obj.is_processed else "Pending"
    processed_status.short_description = "Status"

    def attachment_count(self, obj):
        return obj.attachments.count()
    attachment_count.short_description = "Attachments"

    # Actions for marking contacts as processed/unprocessed
    def mark_as_processed(self, request, queryset):
        updated = queryset.update(
            is_processed=True,
            processed_date=timezone.now(),
            processed_by=request.user
        )
        self.message_user(request, f"{updated} submissions marked as processed.")
    mark_as_processed.short_description = "Mark selected as processed"

    def mark_as_unprocessed(self, request, queryset):
        updated = queryset.update(
            is_processed=False,
            processed_date=None,
            processed_by=None
        )
        self.message_user(request, f"{updated} submissions marked as unprocessed.")
    mark_as_unprocessed.short_description = "Mark selected as unprocessed"

    # Override save_model to set processed_by and processed_date
    def save_model(self, request, obj, form, change):
        if 'is_processed' in form.changed_data and obj.is_processed:
            obj.processed_by = request.user
            obj.processed_date = timezone.now()
        super().save_model(request, obj, form, change)



@admin.register(ContactAttachment)
class ContactAttachmentAdmin(admin.ModelAdmin):
    """
    Admin interface for the ContactAttachment model.  Reduced functionality,
    as attachments are primarily managed through the Contact admin.
    """
    list_display = ['filename', 'contact_link', 'uploaded_at', 'file_size']
    list_filter = ['uploaded_at']
    search_fields = ['file', 'contact__full_name', 'contact__email']
    readonly_fields = ['file_link', 'uploaded_at', 'file_size', 'contact_link']

    def contact_link(self, obj):
        # Return a simple URL.  Django Admin will handle the link.
        return reverse('admin:web_apis_contact_change', args=[obj.contact.id])
    contact_link.short_description = "Contact"

    def file_link(self, obj):
        if obj.file:
            return obj.file.url
        return "-"
    file_link.short_description = "File"

    def file_size(self, obj):
        return f"{obj.filesize() / 1024:.1f} KB" if obj.filesize() else "-"
    file_size.short_description = "Size"

    def filename(self, obj):
        return obj.filename()
    filename.short_description = "Filename"

    def has_add_permission(self, request):
        # Prevent direct creation of attachments; they should be uploaded via Contact form.
        return False
