# Generated by Django 4.1.2 on 2022-12-09 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('explore', '0012_alter_corpus_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corpus',
            name='metadata',
            field=models.TextField(null=True),
        ),
    ]
