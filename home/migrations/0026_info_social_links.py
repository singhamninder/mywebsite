from django.db import migrations, models


def seed_social_links(apps, schema_editor):
    Info = apps.get_model("home", "Info")
    for info in Info.objects.all():
        updated = False
        if not info.github:
            info.github = "https://github.com/singhamninder"
            updated = True
        if not info.email:
            info.email = "amnindersingh13@gmail.com"
            updated = True
        if updated:
            info.save(update_fields=["github", "email"])


def unseed_social_links(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0025_remove_project_project_link_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="info",
            name="google_scholar",
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="info",
            name="github",
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="info",
            name="email",
            field=models.EmailField(blank=True, max_length=300, null=True),
        ),
        migrations.RunPython(seed_social_links, unseed_social_links),
        migrations.RemoveField(
            model_name="info",
            name="twitter",
        ),
    ]
