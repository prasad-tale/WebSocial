# Generated by Django 3.0.6 on 2020-06-25 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0004_likepost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user_Posts'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='user_ProfilePics'),
        ),
    ]
