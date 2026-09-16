from django import forms
from .models import Boutique


class BoutiqueForm(forms.ModelForm):

    class Meta:

        model = Boutique

        fields = [
            'nom',
            'description',
            'logo'
        ]

from django import forms
from .models import AvisBoutique


class AvisBoutiqueForm(forms.ModelForm):

    class Meta:

        model = AvisBoutique

        fields = [
            'note',
            'commentaire'
        ]
