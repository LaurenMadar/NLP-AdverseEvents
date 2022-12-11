# Generated by Django 4.1.2 on 2022-12-04 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Corpus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=200)),
                ('safe', models.BooleanField()),
                ('date imported', models.DateTimeField()),
                ('addedby', models.CharField(max_length=200)),
                ('corpus', models.TextField()),
            ],
        ),
    ]
