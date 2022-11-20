# Generated by Django 4.1.3 on 2022-11-20 17:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='t_game',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('game_designer', models.CharField(max_length=255)),
                ('game_description', models.TextField(blank=True, max_length=2000, null=True)),
                ('release_year', models.PositiveIntegerField(default=2010)),
                ('min_game_time', models.PositiveIntegerField()),
                ('max_game_time', models.PositiveIntegerField()),
                ('avg_time', models.PositiveIntegerField(default=90)),
                ('min_player', models.PositiveIntegerField(default=2, validators=[django.core.validators.MinValueValidator(1)])),
                ('max_player', models.PositiveIntegerField(default=4, validators=[django.core.validators.MaxValueValidator(15)])),
                ('suggested_players', models.PositiveIntegerField()),
                ('minimal_age', models.PositiveIntegerField(default=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('suggested_age', models.PositiveIntegerField()),
                ('publisher', models.CharField(default='No Data', max_length=255)),
                ('image_url', models.CharField(default='No Avaible Image', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='t_genre',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('genre_name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='t_user',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Username', models.CharField(max_length=30, unique=True)),
                ('Mail', models.CharField(max_length=100, unique=True)),
                ('Password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='t_user_game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BoardGamesAPI.t_game')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='t_user_activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Activity_Type', models.CharField(max_length=30, unique=True)),
                ('Activity_Timestamp', models.DateTimeField()),
                ('User_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='t_review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_number', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BoardGamesAPI.t_game')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='t_game_genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BoardGamesAPI.t_game')),
                ('genre_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BoardGamesAPI.t_genre')),
            ],
        ),
        migrations.CreateModel(
            name='t_friend_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Last_Seen', models.DateField(auto_now=True)),
                ('user1_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user2_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user2_id', to='BoardGamesAPI.t_user')),
            ],
        ),
        migrations.AddConstraint(
            model_name='t_friend_list',
            constraint=models.UniqueConstraint(fields=('user1_id', 'user2_Id'), name='cant be your own friend'),
        ),
    ]
