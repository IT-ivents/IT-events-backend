# Generated by Django 4.1 on 2023-06-28 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_alter_event_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image_small',
            field=models.ImageField(blank=True, help_text='Загрузите фотографию', upload_to='events/image', verbose_name='Фотография мероприятия'),
        ),
    ]