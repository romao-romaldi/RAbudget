from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


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
