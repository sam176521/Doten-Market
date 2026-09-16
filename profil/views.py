from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profil
from .forms import ProfilForm

@login_required
def mon_profil(request):

    profil, _ = Profil.objects.get_or_create(utilisateur=request.user)

    if request.method == 'POST':

        form = ProfilForm(
            request.POST,
            request.FILES,
            instance=profil
        )

        if form.is_valid():
            form.save()
            return redirect('profil_vendeur', pk=request.user.id)

    else:
        form = ProfilForm(instance=profil)

    return render(request, 'profil/mon_profil.html', {
        'form': form
    })
