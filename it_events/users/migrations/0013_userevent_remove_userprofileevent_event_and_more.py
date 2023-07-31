# Generated by Django 4.1 on 2023-07-07 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_alter_event_author'),
        ('users', '0012_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_users', to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Список событий организатора',
                'verbose_name_plural': 'Список событий организатора',
                'ordering': ('-id',),
            },
        ),
        # migrations.RemoveField(
        #     model_name='userprofileevent',
        #     name='event',
        # ),
        # migrations.RemoveField(
        #     model_name='userprofileevent',
        #     name='user_profile',
        # ),
        # migrations.DeleteModel(
        #     name='UserProfile',
        # ),
        # migrations.DeleteModel(
        #     name='UserProfileEvent',
        # ),
        migrations.AddConstraint(
            model_name='userevent',
            constraint=models.UniqueConstraint(fields=('user', 'event'), name='unique_user_event'),
        ),
    ]