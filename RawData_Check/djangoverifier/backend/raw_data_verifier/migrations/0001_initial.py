# Generated by Django 4.2.2 on 2023-06-22 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DFUFileInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, null=True)),
                ('file_hash', models.CharField(max_length=255, null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('eq_number', models.IntegerField(null=True)),
                ('serial_id', models.CharField(max_length=255, null=True)),
                ('data_transfer_time_range', models.CharField(max_length=255, null=True)),
                ('data_transfer_date', models.CharField(max_length=255, null=True)),
                ('patient_count', models.IntegerField(null=True)),
                ('image_coll_count_in_drive', models.IntegerField(null=True)),
                ('image_coll_count_in_verification_excel', models.IntegerField(null=True)),
                ('is_match', models.BooleanField(null=True)),
                ('spectral_view_size_on_drive', models.CharField(max_length=255, null=True)),
                ('DFU_size_on_drive', models.CharField(max_length=255, null=True)),
                ('guidListID', models.IntegerField(null=True)),
                ('images_count', models.IntegerField(null=True)),
                ('Raw_MSI', models.IntegerField(default=0, null=True)),
                ('Pseudocolor_generation_intermediate_output', models.IntegerField(default=0, null=True)),
                ('Pseudocolor', models.IntegerField(default=0, null=True)),
                ('Reference', models.IntegerField(default=0, null=True)),
                ('CJA', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GuidList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collectionName', models.CharField(max_length=255, null=True)),
                ('ImageCollFolderNames', models.TextField(null=True)),
                ('ImgCollGUIDs', models.TextField(null=True)),
            ],
        ),
    ]