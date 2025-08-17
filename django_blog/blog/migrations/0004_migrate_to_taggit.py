# Generated migration for switching to django-taggit

from django.db import migrations
from django.db.models import Q


def migrate_tags_to_taggit(apps, schema_editor):
    """Migrate existing tags to django-taggit format"""
    Post = apps.get_model('blog', 'Post')
    Tag = apps.get_model('blog', 'Tag')
    TaggitTag = apps.get_model('taggit', 'Tag')
    TaggedItem = apps.get_model('taggit', 'TaggedItem')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    # Get the content type for Post model
    post_content_type = ContentType.objects.get_for_model(Post)
    
    # Migrate existing tags
    for post in Post.objects.all():
        for tag in post.tags.all():
            # Create or get taggit tag
            taggit_tag, created = TaggitTag.objects.get_or_create(name=tag.name)
            
            # Create tagged item relationship
            TaggedItem.objects.get_or_create(
                tag=taggit_tag,
                content_type=post_content_type,
                object_id=post.id
            )


def reverse_migrate_tags(apps, schema_editor):
    """Reverse migration - not implemented as it would be complex"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_tag_post_tags'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(migrate_tags_to_taggit, reverse_migrate_tags),
    ]
