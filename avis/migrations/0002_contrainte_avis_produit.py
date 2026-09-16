# Generated manually after rating security improvements.

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avis', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='avis',
            constraint=models.UniqueConstraint(fields=('produit', 'utilisateur'), name='avis_produit_unique_par_utilisateur'),
        ),
    ]
