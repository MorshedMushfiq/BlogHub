# Generated by Django 5.1.1 on 2024-11-12 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0003_post_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='Media/Profile_Pic'),
        ),
    ]
