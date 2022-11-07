# Generated by Django 4.1 on 2022-11-07 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('town', models.CharField(blank=True, max_length=100, null=True)),
                ('county', models.CharField(blank=True, max_length=100, null=True)),
                ('post_code', models.CharField(blank=True, max_length=8, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('longitude', models.CharField(blank=True, max_length=50, null=True)),
                ('latitude', models.CharField(blank=True, max_length=50, null=True)),
                ('captcha_score', models.FloatField(default=0.0)),
                ('has_profile', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
