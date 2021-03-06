# Generated by Django 3.0.2 on 2021-03-16 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone', models.IntegerField(max_length=255)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('company', models.CharField(max_length=255)),
                ('password', models.TextField()),
            ],
        ),
    ]
