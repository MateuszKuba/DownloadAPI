# Generated by Django 2.2 on 2019-04-07 15:39

import WebPagesDownload.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='WebText',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.FileField(upload_to=WebPagesDownload.models.text_path)),
                ('download', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webtext', to='WebPagesDownload.Download')),
            ],
        ),
        migrations.CreateModel(
            name='WebImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', models.ImageField(upload_to=WebPagesDownload.models.image_path)),
                ('download', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webimage', to='WebPagesDownload.Download')),
            ],
        ),
    ]
