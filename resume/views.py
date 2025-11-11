from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

from .models import Resume, CommentResume, Hierarchie
from .forms import ResumeForm, CommentResumeForm, HierarchieForm
from gestionbuget.models import BudgetSheet
from . import utility


@login_required
def resume_list(request, pid_sheet):
    """
    Liste des résumés pour une feuille de budget
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid_sheet)
    
    # Vérifier que l'utilisateur a accès à cette feuille
    if budget_sheet.user != request.user.profile:
        # Vérifier si l'utilisateur est partenaire
        is_partner = budget_sheet.type_sheet_partenaire.filter(user=request.user.profile).exists()
        if not is_partner:
            messages.error(request, "Vous n'avez pas accès à cette feuille de budget.")
            return redirect('gestionbudget:budget_sheet_list')
    
    # Résumés créés par l'utilisateur
    my_resumes = budget_sheet.resumes.filter(author=request.user.profile)
    
    # Résumés reçus (en tant que supérieur)
    received_resumes = budget_sheet.resumes.filter(destinataire=request.user.profile)
    
    # Hiérarchies pour le slide-over
    hierarchies = Hierarchie.objects.filter(budget_sheet=budget_sheet)
    
    # Récupérer tous les utilisateurs liés à cette feuille de budget avec leurs rôles
    users_with_roles = []
    
    # Propriétaire
    users_with_roles.append({
        'user': budget_sheet.user,
        'role': 'Propriétaire',
        'is_owner': True
    })

    is_owner = True if budget_sheet.user == request.user.profile else False
    
    # Partenaires
    partenaires = budget_sheet.type_sheet_partenaire.all()
    for partenaire in partenaires:
        users_with_roles.append({
            'user': partenaire.user,
            'role': 'Partenaire',
            'is_owner': False
        })

    print("ok je verife", users_with_roles)
    context = {
        'budget_sheet': budget_sheet,
        'my_resumes': my_resumes,
        'received_resumes': received_resumes,
        'hierarchies': hierarchies,
        'users_with_roles': users_with_roles,
        'today': timezone.now().date(),
        "is_owner": is_owner
    }
    
    return render(request, 'resume/resume_list.html', context)


@login_required
def resume_create(request, pid_sheet):
    """
    Créer un nouveau résumé
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid_sheet)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.author = request.user.profile
            resume.budget_sheet = budget_sheet
            
            # Générer un PID unique
            pid = utility.generpid(25)
            while Resume.objects.filter(pid=pid).exists():
                pid = utility.generpid(25)
            resume.pid = pid
            
            # Trouver le supérieur hiérarchique
            try:
                hierarchie = Hierarchie.objects.get(
                    user=request.user.profile,
                    budget_sheet=budget_sheet
                )
                resume.destinataire = hierarchie.superieur
            except Hierarchie.DoesNotExist:
                resume.destinataire = None
            
            resume.save()
            messages.success(request, 'Rapport créé avec succès.')
            
            return redirect('resume:resume_list', pid_sheet=pid_sheet)
    else:
        # Pré-remplir avec la date du jour
        form = ResumeForm(initial={'date_resume': timezone.now().date()})
    
    context = {
        'form': form,
        'budget_sheet': budget_sheet,
    }
    
    return render(request, 'resume/resume_create.html', context)


@login_required
def resume_detail(request, pid_sheet, pid_resume):
    """
    Détails d'un résumé
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid_sheet)
    resume = get_object_or_404(Resume, pid=pid_resume, budget_sheet=budget_sheet)
    
    # Vérifier les permissions
    can_view = (
        resume.author == request.user.profile or
        resume.destinataire == request.user.profile or
        budget_sheet.user == request.user.profile
    )
    
    if not can_view:
        messages.error(request, "Vous n'avez pas accès à ce résumé.")
        return redirect('resume:resume_list', pid_sheet=pid_sheet)
    
    # Formulaire de commentaire
    comment_form = CommentResumeForm()
    
    context = {
        'budget_sheet': budget_sheet,
        'resume': resume,
        'comment_form': comment_form,
        'can_validate': resume.destinataire == request.user.profile,
        'is_author': resume.author == request.user.profile,
    }
    
    return render(request, 'resume/resume_detail.html', context)


@login_required
def resume_edit(request, pid_sheet, pid_resume):
    """
    Modifier un résumé (seulement si statut = draft)
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid_sheet)
    resume = get_object_or_404(Resume, pid=pid_resume, budget_sheet=budget_sheet)
    
    # Vérifier que l'utilisateur est l'auteur
    if resume.author != request.user.profile:
        messages.error(request, "Vous ne pouvez pas modifier ce résumé.")
        return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)
    
    # Vérifier que le résumé est en brouillon
    if resume.status != 'draft':
        messages.error(request, "Vous ne pouvez modifier qu'un résumé en brouillon.")
        return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)
    
    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rapport modifié avec succès.')
            return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)
    else:
        form = ResumeForm(instance=resume)
    
    context = {
        'form': form,
        'budget_sheet': budget_sheet,
        'resume': resume,
    }
    
    return render(request, 'resume/resume_edit.html', context)


@login_required
def resume_submit(request, pid_sheet, pid_resume):
    """
    Soumettre un résumé au supérieur
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid_sheet)
    resume = get_object_or_404(Resume, pid=pid_resume, budget_sheet=budget_sheet)
    
    # Vérifier que l'utilisateur est l'auteur
    if resume.author != request.user.profile:
        messages.error(request, "Vous ne pouvez pas soumettre ce résumé.")
        return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)
    
    if resume.status == 'draft':
        resume.submit()
        if resume.destinataire:
            messages.success(request, f'Résumé soumis à {resume.destinataire}.')
        else:
            messages.warning(request, 'Résumé soumis mais aucun supérieur hiérarchique défini.')
    else:
        messages.error(request, 'Ce résumé a déjà été soumis.')
    
    return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)


@login_required
def resume_validate(request, pid_sheet, pid_resume):
    """
    Valider un résumé (par le supérieur)
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid_sheet)
    resume = get_object_or_404(Resume, pid=pid_resume, budget_sheet=budget_sheet)
    
    # Vérifier que l'utilisateur est le destinataire
    if resume.destinataire != request.user.profile:
        messages.error(request, "Vous ne pouvez pas valider ce résumé.")
        return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)
    
    if resume.status == 'submitted':
        resume.validate()
        messages.success(request, 'Résumé validé avec succès.')
    else:
        messages.error(request, 'Ce résumé ne peut pas être validé.')
    
    return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)


@login_required
def resume_reject(request, pid_sheet, pid_resume):
    """
    Rejeter un résumé (par le supérieur)
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid_sheet)
    resume = get_object_or_404(Resume, pid=pid_resume, budget_sheet=budget_sheet)
    
    # Vérifier que l'utilisateur est le destinataire
    if resume.destinataire != request.user.profile:
        messages.error(request, "Vous ne pouvez pas rejeter ce résumé.")
        return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)
    
    if resume.status == 'submitted':
        resume.reject()
        messages.warning(request, 'Résumé rejeté.')
    else:
        messages.error(request, 'Ce résumé ne peut pas être rejeté.')
    
    return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)


@login_required
def comment_create(request, pid_sheet, pid_resume):
    """
    Ajouter un commentaire sur un résumé
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid_sheet)
    resume = get_object_or_404(Resume, pid=pid_resume, budget_sheet=budget_sheet)
    
    if request.method == 'POST':
        form = CommentResumeForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.resume = resume
            comment.author = request.user.profile
            comment.save()
            messages.success(request, 'Commentaire ajouté.')
            
            if request.htmx:
                return render(request, 'resume/htmx/comment_created.html', {
                    'comment': comment,
                    'resume': resume
                })
    
    return redirect('resume:resume_detail', pid_sheet=pid_sheet, pid_resume=pid_resume)


@login_required
def hierarchie_manage(request, pid_sheet):
    """
    Gérer la hiérarchie pour une feuille de budget
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid_sheet)
    
    # Vérifier que l'utilisateur est propriétaire ou superadmin
    if budget_sheet.user != request.user.profile:
        messages.error(request, "Vous n'avez pas les permissions pour gérer la hiérarchie.")
        return redirect('resume:resume_list', pid_sheet=pid_sheet)
    
    hierarchies = Hierarchie.objects.filter(budget_sheet=budget_sheet)
    
    # Récupérer tous les utilisateurs liés à cette feuille de budget avec leurs rôles
    users_with_roles = []
    
    # Propriétaire
    users_with_roles.append({
        'user': budget_sheet.user,
        'role': 'Propriétaire',
        'is_owner': True
    })
    
    # Partenaires
    partenaires = budget_sheet.type_sheet_partenaire.all()
    for partenaire in partenaires:
        users_with_roles.append({
            'user': partenaire.user,
            'role': 'Partenaire',
            'is_owner': False
        })
    
    if request.method == 'POST':
        form = HierarchieForm(request.POST, budget_sheet=budget_sheet)
        if form.is_valid():
            hierarchie = form.save(commit=False)
            hierarchie.budget_sheet = budget_sheet
            hierarchie.save()
            messages.success(request, 'Hiérarchie définie avec succès.')
            return redirect('resume:hierarchie_manage', pid_sheet=pid_sheet)
    else:
        form = HierarchieForm(budget_sheet=budget_sheet)
    
    context = {
        'budget_sheet': budget_sheet,
        'hierarchies': hierarchies,
        'users_with_roles': users_with_roles,
        'form': form,
    }
    
    return render(request, 'resume/hierarchie_manage.html', context)
