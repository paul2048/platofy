# Generated by Django 3.0.3 on 2020-02-17 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0020_question_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='times_used',
            field=models.PositiveIntegerField(default=1),
        ),
    ]