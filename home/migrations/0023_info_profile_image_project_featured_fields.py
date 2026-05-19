from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0022_reference"),
    ]

    operations = [
        migrations.AddField(
            model_name="info",
            name="profile_image",
            field=models.ImageField(blank=True, default="default.jpg", null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="code_url",
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="demo_url",
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name="project",
            name="featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="project",
            name="impact_summary",
            field=models.CharField(blank=True, max_length=280, null=True),
        ),
    ]
