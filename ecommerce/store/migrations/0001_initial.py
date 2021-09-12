# Generated by Django 3.1.5 on 2021-04-22 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('url', models.TextField()),
                ('description', models.TextField()),
                ('list_price', models.FloatField()),
                ('sale_price', models.FloatField()),
                ('brand', models.TextField()),
                ('stock_number', models.IntegerField()),
            ],
        ),
    ]
