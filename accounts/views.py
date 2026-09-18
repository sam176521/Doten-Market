from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from boutiques.models import Boutique
from profil.models import Profil

from .forms import RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            try:
                validate_password(user.password, user)
            except ValidationError as errors:
                for error in errors:
                    form.add_error('password', error)
                return render(request, 'accounts/register.html', {'form': form})

            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


User = get_user_model()


def profil_vendeur(request, pk):
    vendeur = get_object_or_404(User, id=pk)
    profil, _ = Profil.objects.get_or_create(utilisateur=vendeur)
    boutique = Boutique.objects.filter(proprietaire=vendeur).first()
    produits = boutique.produit_set.select_related('categorie').all() if boutique else []
    nombre_produits = produits.count() if boutique else 0

    return render(request, 'accounts/profil_vendeur.html', {
        'vendeur': vendeur,
        'profil': profil,
        'boutique': boutique,
        'produits': produits,
        'nombre_produits': nombre_produits,
    })




