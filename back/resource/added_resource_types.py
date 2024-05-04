from django.db import migrations

def create_default_resource_types(apps, schema_editor):
    ResourceType = apps.get_model('resource', 'ResourceType')
    default_types = ['Type1', 'Type2', 'Type3']  # Define your default types here
    for type_name in default_types:
        ResourceType.objects.get_or_create(name=type_name)

class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0004_resourcetype_youtubevideo_type'),  # Adjust with your actual previous migration file
    ]

    operations = [
        migrations.RunPython(create_default_resource_types),
    ]
