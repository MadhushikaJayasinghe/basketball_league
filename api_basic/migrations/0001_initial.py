# Generated by Django 3.1.4 on 2021-05-06 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('role', models.CharField(choices=[('COACH', 'Coach'), ('PLAYER', 'Player'), ('ADMIN', 'Admin')], default='PLAYER', max_length=6)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('height', models.FloatField(default=0)),
                ('average_score', models.FloatField(default=0)),
                ('no_of_games', models.IntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game', models.CharField(choices=[('SG', 'Selection Game'), ('QF', 'Quarter Final'), ('SF', 'Semi Final'), ('FI', 'Final')], default='SG', max_length=6)),
                ('game_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_done', models.BooleanField(default=False)),
                ('team_score', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'game',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('team_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'team',
            },
        ),
        migrations.CreateModel(
            name='UserTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('team_id', models.ForeignKey(db_column='team_id', on_delete=django.db.models.deletion.CASCADE, to='api_basic.team')),
            ],
            options={
                'db_table': 'user_team',
            },
        ),
        migrations.CreateModel(
            name='UserStat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_logged_in', models.BooleanField(default=False)),
                ('login_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('logout_time', models.DateTimeField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('user_score', models.IntegerField(default=0)),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_basic.game')),
            ],
            options={
                'db_table': 'user_game',
            },
        ),
        migrations.AddField(
            model_name='game',
            name='team_id',
            field=models.ManyToManyField(to='api_basic.Team'),
        ),
    ]
