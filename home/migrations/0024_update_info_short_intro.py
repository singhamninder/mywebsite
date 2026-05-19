from django.db import migrations

ABOUT_TEXT = (
    "I'm a geospatial data scientist and remote sensing engineer who enjoys turning "
    "Earth observation data into decisions people can actually use. Over the last several "
    "years I've worked across research and industry — from graduate fieldwork in soil "
    "hydrology and salinity mapping, through post-doctoral remote sensing at UC Riverside "
    "and the USDA Salinity Lab, to production ML systems at Climate LLC (Bayer Crop "
    "Science) — building machine learning pipelines for crop and land-cover analysis, "
    "soil and environmental monitoring, and large-scale spatiotemporal feature engineering. "
    "My PhD in Environmental Sciences (Soil & Water, UC Riverside) keeps me grounded in "
    "the real-world context behind the data, and I bring that perspective into every "
    "project — from geospatial foundation-model prototyping on GCP and Google Earth Engine "
    "to scalable production deployment."
)


def set_short_intro(apps, schema_editor):
    Info = apps.get_model("home", "Info")
    Info.objects.update(short_intro=ABOUT_TEXT)


def reverse_short_intro(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0023_info_profile_image_project_featured_fields"),
    ]

    operations = [
        migrations.RunPython(set_short_intro, reverse_short_intro),
    ]
