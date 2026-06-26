# Generated manually to make Record IDs editable in the admin.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("siteweb", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="record",
            name="id",
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
