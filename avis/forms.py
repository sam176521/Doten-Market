from django import forms
from .models import Avis

class AvisForm(forms.ModelForm):

    class Meta:
        model = Avis

        fields = [
            'note',
            'commentaire'
        ]
