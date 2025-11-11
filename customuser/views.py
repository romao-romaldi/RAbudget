from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Imports pour la gestion des logos
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Logo
from .forms import LogoForm


def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			# Rediriger vers la liste des feuilles de budget après connexion
			return redirect('gestionbudget:budget_sheet_list')
		else:
			messages.error(request, 'Identifiants invalides')
	return render(request, 'customuser/login.html')

def logout_view(request):
	logout(request)
	return redirect('customuser:login')


@login_required
def logo_list(request):
    """Vue pour afficher la liste des logos"""
    logos = Logo.objects.all()
    return render(request, 'customuser/logo_list.html', {'logos': logos})


@login_required
def logo_create(request):
    """Vue pour créer un nouveau logo"""
    if request.method == 'POST':
        form = LogoForm(request.POST, request.FILES)
        if form.is_valid():
            logo = form.save()
            messages.success(request, f'Logo "{logo.nom}" créé avec succès.')
            return redirect('customuser:logo_list')
    else:
        form = LogoForm()
    return render(request, 'customuser/logo_form.html', {'form': form, 'action': 'Créer'})


@login_required
def logo_edit(request, pk):
    """Vue pour modifier un logo existant"""
    logo = get_object_or_404(Logo, pk=pk)
    if request.method == 'POST':
        form = LogoForm(request.POST, request.FILES, instance=logo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Logo "{logo.nom}" modifié avec succès.')
            return redirect('customuser:logo_list')
    else:
        form = LogoForm(instance=logo)
    return render(request, 'customuser/logo_form.html', {'form': form, 'action': 'Modifier', 'logo': logo})


@login_required
def logo_activate(request, pk):
    """Vue pour activer un logo"""
    logo = get_object_or_404(Logo, pk=pk)
    logo.est_actif = True
    logo.save()
    messages.success(request, f'Logo "{logo.nom}" activé avec succès.')
    return redirect('customuser:logo_list')


@login_required
def logo_delete(request, pk):
    """Vue pour supprimer un logo"""
    logo = get_object_or_404(Logo, pk=pk)
    if request.method == 'POST':
        nom_logo = logo.nom
        logo.delete()
        messages.success(request, f'Logo "{nom_logo}" supprimé avec succès.')
        return redirect('customuser:logo_list')
    return render(request, 'customuser/logo_confirm_delete.html', {'logo': logo})
