# Generated by Django 5.0.7 on 2024-07-14 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='procan',
            field=models.PositiveIntegerField(db_column='ProCan', default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='proimg',
            field=models.ImageField(blank=True, db_column='ProIma', null=True, upload_to='static/images/'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='prodes',
            field=models.CharField(blank=True, db_column='ProDes', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='pronom',
            field=models.CharField(db_column='ProNom', max_length=100, unique=True),
        ),
    ]
