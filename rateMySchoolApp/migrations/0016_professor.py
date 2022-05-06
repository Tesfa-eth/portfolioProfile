# Generated by Django 4.0.3 on 2022-05-04 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rateMySchoolApp', '0015_post_profanity_prob'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('country_code', models.IntegerField()),
                ('overall_rating', models.IntegerField()),
                ('currentUniversity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rateMySchoolApp.universities')),
            ],
        ),
    ]
