# Generated manually to restore Django-managed Record IDs.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("siteweb", "0002_alter_record_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="record",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
    ]
