# Generated by Django 2.0.2 on 2018-02-26 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('k2k', '0005_auto_20180223_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='colors',
            field=models.ManyToManyField(to='k2k.Color'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sizes',
            field=models.ManyToManyField(to='k2k.Size'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='k2k.Order'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image_path',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]
