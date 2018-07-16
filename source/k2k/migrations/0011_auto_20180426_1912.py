# Generated by Django 2.0.2 on 2018-04-26 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('k2k', '0010_auto_20180311_2144'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='k2k.User'),
        ),
        migrations.AlterField(
            model_name='item',
            name='colors',
            field=models.ManyToManyField(default=None, null=True, to='k2k.Color'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sizes',
            field=models.ManyToManyField(default=None, null=True, to='k2k.Size'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='k2k.Order'),
        ),
    ]