# Generated by Django 4.0.5 on 2022-06-08 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('artist', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('description', models.TextField(max_length=250)),
            ],
        ),
    ]
