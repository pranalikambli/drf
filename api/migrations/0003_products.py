# Generated by Django 3.0.8 on 2020-07-20 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'products',
            },
        ),
    ]
