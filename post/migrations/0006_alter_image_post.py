# Generated by Django 4.2.6 on 2023-12-26 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_alter_image_photos_alter_post_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post'),
        ),
    ]
