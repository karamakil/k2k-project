# Generated by Django 2.0.2 on 2018-03-06 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('k2k', '0007_auto_20180226_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='colors',
            field=models.ManyToManyField(default=None, null=True, to='k2k.Color'),
        ),
        migrations.AlterField(
            model_name='item',
            name='country',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='k2k.Country'),
        ),
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(default=None, null=True),
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
