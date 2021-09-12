# Generated by Django 3.2 on 2021-04-30 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_rename_product_order_order_detail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_detail',
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='OrderDetail',
        ),
    ]
