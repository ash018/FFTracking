# Generated by Django 2.0.5 on 2018-12-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentMSRLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Userid', models.CharField(db_column='Userid', max_length=50)),
                ('Level1Name', models.CharField(db_column='Level1Name', max_length=50)),
                ('UpazilaCode', models.CharField(db_column='UpazilaCode', max_length=50)),
                ('UpazilaName', models.CharField(db_column='UpazilaName', max_length=50)),
                ('Time', models.DateTimeField()),
                ('Latitude', models.FloatField(db_column='Latitude')),
                ('Longitude', models.FloatField(db_column='Longitude')),
            ],
            options={
                'db_table': 'vwmmCurrentMSRLocation',
                'managed': False,
            },
        ),
    ]
