# Generated by Django 5.0.6 on 2024-07-07 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AbstractItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("done", models.BooleanField(default=False)),
                ("expiring_date", models.DateField()),
                ("expire_work_day", models.BooleanField(default=False)),
                ("is_next_work_day", models.BooleanField(default=True)),
                (
                    "periodicity",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("monthly", "Monthly"),
                            ("yearly", "Yearly"),
                            ("weekly", "Weekly"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="AbstractFixedItem",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("orcamento.abstractitem",),
        ),
    ]
