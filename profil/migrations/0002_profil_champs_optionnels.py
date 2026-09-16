# Generated manually after profile auto-creation improvements.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='adresse',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='profil',
            name='telephone',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='profil',
            name='ville',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profil',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
