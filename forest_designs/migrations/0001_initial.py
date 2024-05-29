# Generated by Django 5.0.4 on 2024-05-29 17:20

import datetime
import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plant_species', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlantImageKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'plant image type',
                'verbose_name_plural': 'plant image types',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlantLogKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'plant log type',
                'verbose_name_plural': 'plant log types',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ZoneKind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'zone type',
                'verbose_name_plural': 'zone types',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, unique=True, verbose_name='location')),
                ('notes', models.TextField(blank=True, verbose_name='notes')),
                ('genus', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='plant_species.genus')),
                ('species', models.ForeignKey(blank=True, help_text='When specified, genus is automatically set.', null=True, on_delete=django.db.models.deletion.PROTECT, to='plant_species.species')),
                ('variety', models.ForeignKey(blank=True, help_text='When specified, species and genus are automatically set.', null=True, on_delete=django.db.models.deletion.PROTECT, to='plant_species.speciesvariety')),
            ],
            options={
                'verbose_name': 'plant',
                'verbose_name_plural': 'plants',
            },
        ),
        migrations.CreateModel(
            name='PlantImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(db_index=True, default=datetime.datetime.now, verbose_name='date')),
                ('image', models.ImageField(upload_to='plant_images', verbose_name='image')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='forest_designs.plant')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forest_designs.plantimagekind')),
            ],
            options={
                'verbose_name': 'plant image',
                'verbose_name_plural': 'plant images',
                'ordering': ('plant', '-date'),
            },
        ),
        migrations.CreateModel(
            name='PlantLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now, help_text='Timestamp of the log entry.', verbose_name='date')),
                ('notes', models.TextField(verbose_name='notes')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='forest_designs.plant')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forest_designs.plantlogkind')),
            ],
            options={
                'verbose_name': 'plant log',
                'verbose_name_plural': 'plant logs',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('area', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, verbose_name='area')),
                ('kind', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='forest_designs.zonekind')),
            ],
            options={
                'verbose_name': 'zone',
                'verbose_name_plural': 'zones',
                'ordering': ['name'],
            },
        ),
        migrations.AddConstraint(
            model_name='plant',
            constraint=models.CheckConstraint(check=models.Q(('species__isnull', False), ('genus__isnull', False), ('variety__isnull', False), _connector='OR'), name='forest_designs_plant_genus_species_variety_notnull'),
        ),
    ]
