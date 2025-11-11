from django.shortcuts import render


def contact_personne(request):
    return render(request, 'lawyer/contacts/contact_personne_list.html')

def details_contact_personne(request):
    return render(request, 'lawyer/contacts/details_contact_personne.html')