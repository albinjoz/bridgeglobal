# Generated by Django 3.0.3 on 2021-06-03 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wallet',
            old_name='deposited_by',
            new_name='owned_by',
        ),
        migrations.RemoveField(
            model_name='wallet',
            name='deposited_at',
        ),
        migrations.AlterField(
            model_name='wallet',
            name='status',
            field=models.CharField(blank=None, choices=[(0, 'Enabled'), (1, 'Disabled')], max_length=10, null=True),
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposited_at', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=3, max_digits=25)),
                ('reference_id', models.CharField(blank=None, max_length=300, null=True)),
                ('deposited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('wallet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.Wallet')),
            ],
        ),
    ]
