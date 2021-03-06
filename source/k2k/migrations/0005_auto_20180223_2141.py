# Generated by Django 2.0.2 on 2018-02-23 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('k2k', '0004_auto_20180218_1917'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='sub_category',
            new_name='SubCategory',
        ),
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
    ]
