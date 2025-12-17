

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('running', 'Running'), ('passed', 'Passed'), ('failed', 'Failed'), ('error', 'Error')], default='running', max_length=20)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('duration', models.FloatField(blank=True, null=True)),
                ('total_tests', models.IntegerField(default=0)),
                ('passed_tests', models.IntegerField(default=0)),
                ('failed_tests', models.IntegerField(default=0)),
                ('error_tests', models.IntegerField(default=0)),
                ('coverage_percentage', models.FloatField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-start_time'],
            },
        ),
        migrations.CreateModel(
            name='TestNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('test_failure', 'Test Failure'), ('build_failure', 'Build Failure'), ('coverage_drop', 'Coverage Drop')], max_length=20)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_sent', models.BooleanField(default=False)),
                ('test_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_dashboard.testrun')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('class_name', models.CharField(max_length=200)),
                ('module_name', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('passed', 'Passed'), ('failed', 'Failed'), ('error', 'Error'), ('skipped', 'Skipped')], max_length=20)),
                ('duration', models.FloatField(default=0.0)),
                ('error_message', models.TextField(blank=True)),
                ('traceback', models.TextField(blank=True)),
                ('test_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_cases', to='test_dashboard.testrun')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
