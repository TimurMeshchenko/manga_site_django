# Generated by Django 5.0 on 2023-12-29 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remanga', '0016_comment_likes_title_comments_ratings_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ratings',
        ),
        migrations.CreateModel(
            name='Title_rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('title_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='remanga.title')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
    ]
