


# blog/models/signals_models.py


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

from .engagement_models import Comment, Like, PostReaction, Favorite, CommentReaction
from .analytics_models import PostView, AdminActivityLog
from .sharing_models import ShareTracking
from .notification_models import Notification, AdminNotification



@receiver(post_save, sender=Comment)
def handle_comment_notification(sender, instance, created, **kwargs):
    if created:
        AdminActivityLog.objects.create(
            activity_type=AdminActivityLog.ActivityType.COMMENT,
            user=instance.user,
            post=instance.post,
            metadata={
                'comment_id': str(instance.id),
                'content_preview': instance.content[:50]
            }
        )
        
        if instance.user != instance.post.author:
            Notification.objects.create(
                user=instance.post.author,
                notification_type=Notification.NotificationType.COMMENT,
                message=f"New comment on your post '{instance.post.title}'",
                target_url=instance.post.get_absolute_url(),
                related_post=instance.post
            )
        
        AdminNotification.create_for_comment(instance)

@receiver(post_save, sender=Like)
def handle_like_notification(sender, instance, created, **kwargs):
    if created:
        AdminActivityLog.objects.create(
            activity_type=AdminActivityLog.ActivityType.LIKE,
            user=instance.user,
            post=instance.post
        )
        
        if instance.user != instance.post.author:
            Notification.objects.create(
                user=instance.post.author,
                notification_type=Notification.NotificationType.LIKE,
                message=f"{instance.user.username} liked your post '{instance.post.title}'",
                target_url=instance.post.get_absolute_url(),
                related_post=instance.post
            )

@receiver(post_save, sender=PostReaction)
def handle_reaction_notification(sender, instance, created, **kwargs):
    if created:
        AdminNotification.create_for_reaction(instance)

@receiver(post_save, sender=Favorite)
def handle_favorite_notification(sender, instance, created, **kwargs):
    if created:
        AdminActivityLog.objects.create(
            activity_type=AdminActivityLog.ActivityType.FAVORITE,
            user=instance.user,
            post=instance.post
        )
        
        if instance.user != instance.post.author:
            Notification.objects.create(
                user=instance.post.author,
                notification_type=Notification.NotificationType.FAVORITE,
                message=f"{instance.user.username} favorited your post '{instance.post.title}'",
                target_url=instance.post.get_absolute_url(),
                related_post=instance.post
            )
        
        AdminNotification.create_for_favorite(instance)

@receiver(post_save, sender=PostView)
def handle_view_notification(sender, instance, created, **kwargs):
    if created:
        AdminActivityLog.objects.create(
            activity_type=AdminActivityLog.ActivityType.POST_VIEW,
            user=instance.user,
            post=instance.post,
            ip_address=instance.ip_address,
            metadata={
                'user_agent': instance.user_agent,
                'referrer': instance.referrer
            }
        )
        
        instance.post.view_count = models.F('view_count') + 1
        instance.post.save(update_fields=['view_count'])
        
        AdminNotification.create_for_post_view(instance)

@receiver(post_save, sender=ShareTracking)
def handle_share_tracking(sender, instance, created, **kwargs):
    if created:
        instance.post.save()
        
        AdminActivityLog.objects.create(
            activity_type=AdminActivityLog.ActivityType.SHARE,
            user=instance.user,
            post=instance.post,
            ip_address=instance.ip_address,
            metadata={
                'platform': instance.platform.name if instance.platform else 'direct',
                'method': instance.share_method
            }
        )
        
        AdminNotification.objects.create(
            notification_type=AdminNotification.NotificationType.SHARE,
            title=f"New share of '{instance.post.title}'",
            message=f"Shared via {instance.platform.name if instance.platform else 'direct link'}",
            related_object_id=instance.post.id,
            related_content_type='blogpost',
            metadata={
                'post_id': str(instance.post.id),
                'post_title': instance.post.title,
                'platform': instance.platform.name if instance.platform else None,
                'method': instance.share_method
            }
        )