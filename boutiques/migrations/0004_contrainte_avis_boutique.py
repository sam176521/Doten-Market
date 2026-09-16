# Generated manually after rating security improvements.

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutiques', '0003_delete_avis'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='avisboutique',
            name='note',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddConstraint(
            model_name='avisboutique',
            constraint=models.UniqueConstraint(fields=('boutique', 'utilisateur'), name='avis_boutique_unique_par_utilisateur'),
        ),
    ]
