# Generated by Django 4.2.23 on 2025-07-24 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('club', '0001_initial'),
        ('child', '0002_alter_child_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='child.child')),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='club.club')),
            ],
            options={
                'unique_together': {('child', 'club')},
            },
        ),
    ]
