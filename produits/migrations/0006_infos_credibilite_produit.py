# Generated manually after product credibility improvements.

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0005_delete_panier'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='details_credibilite',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='produit',
            name='etat',
            field=models.CharField(choices=[('neuf', 'Neuf'), ('comme_neuf', 'Comme neuf'), ('occasion', 'Occasion'), ('reconditionne', 'Reconditionne')], default='neuf', max_length=20),
        ),
        migrations.AddField(
            model_name='produit',
            name='garantie',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='produit',
            name='marque',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='produit',
            name='origine',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='produit',
            name='qualite',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='produit',
            name='prix',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='produit',
            name='stock',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
