# Generated by Django 4.2.20 on 2025-04-08 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('accreditation', models.CharField(blank=True, max_length=255)),
                ('treatment_type', models.CharField(default='General', max_length=100)),
                ('cost_estimate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('accepts_insurance', models.BooleanField(default=True)),
                ('is_available', models.BooleanField(default=True)),
                ('facilities', models.ManyToManyField(related_name='hospitals', to='hospital_search.facility')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('rating', models.PositiveIntegerField()),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='hospital_search.hospital')),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('specialty', models.CharField(max_length=100)),
                ('profile', models.TextField()),
                ('rating', models.FloatField(default=0.0)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='hospital_search.hospital')),
            ],
        ),
    ]
