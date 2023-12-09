# Generated by Django 4.2.1 on 2023-12-02 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remanga', '0005_remove_title_avg_rating_remove_title_count_bookmarks_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='avg_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='title',
            name='count_bookmarks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='title',
            name='count_rating',
            field=models.IntegerField(default=0),
        ),
    ]
