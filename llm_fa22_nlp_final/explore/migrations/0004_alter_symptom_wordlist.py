# Generated by Django 4.1.2 on 2022-12-04 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0003_alter_corpus_id_alter_medication_id_alter_symptom_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='symptom',
            name='wordlist',
            field=models.TextField(null=True),
        ),
    ]
