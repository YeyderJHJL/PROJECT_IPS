# Generated by Django 5.0.7 on 2024-07-14 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadopersonal',
            name='estpercod',
            field=models.AutoField(db_column='EstPerCod', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='estadopersonal',
            name='estpernom',
            field=models.CharField(db_column='EstPerNom', max_length=50),
        ),
    ]
