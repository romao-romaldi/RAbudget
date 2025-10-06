from http.client import HTTPException

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.db.models import Prefetch

from .models import (BudgetSheet, TypeBudget, Budget, SheetPartener, SheetInvitation, Demande, CommentDemande, choise_role, choise_status)
from .forms import FormBudget
from customuser.models import Profile
from django.contrib.auth.models import User

from .forms import (FormBudgetSheet, FormBudget, FormSection, FormComment, FormDemande)
from .utility import get_monthly_data_by_type, statistiques_par_jours
from gestionbuget import utility
# Create your views here.

def index(request):
    pass

@login_required
def budget_sheet_create(request):
    """
    View to create a new budget sheet.
    """
    if request.method == 'POST':
        form = FormBudgetSheet(request.POST)
        if form.is_valid():
            while transaction.atomic():
                pid = utility.generpid(20)
                budget_sheet = form.save(commit=False)
                budget_sheet.user = request.user.profile
                budget_sheet.pid = pid
                budget_sheet.save()

                SheetPartener.objects.get_or_create(
                    sheet=budget_sheet,
                    user=budget_sheet.user,
                    defaults={'role': 'superadmin', 'pid': utility.generpid(24)}
                )
            # After saving the budget sheet, redirect to a success page or render a template
                if budget_sheet:
                    r = utility.default_create_init(request, budget_sheet , TypeBudget)
                    if request.htmx and r:
                        return render(request, 'gestionbuget/htmx/budgetsheet_created.html',
                                      {'budget_sheet': budget_sheet, 'htmx': True, "is_success": True,
                                       "form": FormBudgetSheet()
                                       }, status=201)
                    return render(request, 'gestionbuget/htmx/budgetsheet_created.html',
                                  {'budget_sheet': budget_sheet}, status=201 )
                else :
                    return render(request, 'gestionbuget/htmx/budgetsheet_created.html',
                                  {'budget_sheet': budget_sheet, "form": FormBudgetSheet()})

    else:
        form = FormBudgetSheet()

    return render(request, 'gestionbuget/htmx/budget_sheet_create.html', {'form': form})

def budget_sheet_delete(request, pid):
    try :
        budget_sheet = request.user.profile.user_budget_sheets.get(pid=pid)
        budget_sheet.status = False
        budget_sheet.save()
    except:
        return render(request, "gestionbuget/htmx/sheet/row_sheet.html",
                      {
                          "budget": "",
                          "status": False
                      })

    return render(request, "gestionbuget/htmx/sheet/row_sheet.html",
                  {
                      "budget": budget_sheet,
                      "status": True
                  })

@login_required
def budget_sheet_list(request):
    """
    View to list all budget sheets.
    """

    # Feuilles créées par l'utilisateur
    mes_feuilles = request.user.profile.user_budget_sheets.filter(status=True)
    print("Mes feuilles:", mes_feuilles)

    # Feuilles où l'utilisateur est partenaire
    feuilles_partagees_ids = SheetPartener.objects.filter(
        user=request.user.profile
    ).values_list('sheet_id', flat=True).distinct()
    feuilles_partagees = BudgetSheet.objects.filter(
        id__in=feuilles_partagees_ids,
        status=True
    )
    print("Feuilles partagées:", feuilles_partagees)

    context = {
        'mes_feuilles': mes_feuilles,
        'feuilles_partagees': feuilles_partagees,
        "form": FormBudgetSheet()
    }
    return render(request, 'gestionbuget/budget_sheet_list.html', context)

@login_required
def budget_sheet_detail(request, pid):
    """
    View to display details of a specific budget sheet.
    """
    month = datetime.now().month
    year = datetime.now().year
    month_filter = request.GET.get('month_filter', None)
    print("je suis dans budget_sheet_detail", month_filter)
    Month_current = datetime.now()
    print("mois courant : ",Month_current)
    filter = ""

    print("je suis request ",len(request.GET))

    if month_filter:
        month = int(month_filter.split("-")[1])
        year = int(month_filter.split("-")[0])
        print(month_filter, "type", type(month_filter))
        Month_current = datetime.strptime(f"{year}-{month}-1", "%Y-%m-%d")
        filter = month_filter

    try:
        print("je suis pid", pid)
        budget_sheet = get_object_or_404(BudgetSheet, pid=pid, status=True)

        # Vérifier les permissions (propriétaire ou partenaire)
        is_owner = budget_sheet.user == request.user.profile
        is_partner = SheetPartener.objects.filter(sheet=budget_sheet, user=request.user.profile).exists()

        if not (is_owner or is_partner):
            return redirect('gestionbudget:budget_sheet_list')

        type_budgets = budget_sheet.type_budgets_sheet.all().prefetch_related(
            Prefetch('budgets',
                    queryset=Budget.objects.filter(date_created__month=month, date_created__year=year)
                     .order_by('-date_created'),
                    )
        )

        # buggets = type_budgets.budgets.all().filter(date_created__month=datetime.now().month)
    except:
        print("je suis dans erreurs")
        return render(request, 'gestionbuget/budget_sheet_not_found.html', {'pid': pid})

    date = datetime.strptime("2023-07-01", "%Y-%m-%d")



    context = {
        'budget_sheet': budget_sheet,
        "Month_current": Month_current,
        "form": FormBudget(),
        "type_budgets": type_budgets,
        "filter" : filter,
        "partenaires": SheetPartener.objects.filter(sheet=budget_sheet),
        'is_owner': is_owner,
        'is_partner': is_partner
    }

    return render(request, 'gestionbuget/budget_sheet_details.html', context)

@login_required
def chart_budget(request, pid):
    """
    View to display a chart of budgets for a specific budget sheet.
    """


    try:
        budget_sheet = get_object_or_404(BudgetSheet, pid=pid, status=True)

        # Vérifier les permissions (propriétaire ou partenaire)
        is_owner = budget_sheet.user == request.user.profile
        is_partner = SheetPartener.objects.filter(sheet=budget_sheet, user=request.user.profile).exists()

        if not (is_owner or is_partner):
            return JsonResponse({'error': 'Accès non autorisé'}, safe=False, status=403)

        data = get_monthly_data_by_type(Budget.objects.filter(type_budget__budget_sheet__pid=pid))

    except:
        return JsonResponse({}, safe=False, status=404)
    return JsonResponse(data, safe=False, status=200)

@login_required
def chart_budget_month(request, pid):
    """
    View to display a chart of budgets for a specific budget sheet.
    """
    month_filter = request.GET.get('month_filter', None)
    try:
        budget_sheet = get_object_or_404(BudgetSheet, pid=pid, status=True)

        # Vérifier les permissions (propriétaire ou partenaire)
        is_owner = budget_sheet.user == request.user.profile
        is_partner = SheetPartener.objects.filter(sheet=budget_sheet, user=request.user.profile).exists()

        if not (is_owner or is_partner):
            return JsonResponse({'error': 'Accès non autorisé'}, safe=False, status=403)

        print(budget_sheet.pid, )
        buget = Budget.objects.filter(type_budget__budget_sheet__pid=budget_sheet.pid)
        if month_filter:
            data = statistiques_par_jours(buget,
                            datetime.strptime(f"{month_filter}-01", "%Y-%m-%d"))
        else:
            data =statistiques_par_jours(buget)
    except Exception as e:
        print("je suis erreur ", month_filter, str(e))
        return JsonResponse({}, safe=False, status=404)
    return JsonResponse(data, safe=False, status=200)

@login_required
def created_budget(request, pid):
    # try:
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid, status=True)

    # Vérifier les permissions (propriétaire ou partenaire)
    is_owner = budget_sheet.user == request.user.profile
    is_partner = SheetPartener.objects.filter(sheet=budget_sheet, user=request.user.profile).exists()

    if not (is_owner or is_partner):
        return redirect('gestionbudget:budget_sheet_list')

    month = datetime.now().month
    year = datetime.now().year
    if request.method == "POST":
        type_budget = request.POST.get("type_budget", None)
        type_budget = budget_sheet.type_budgets_sheet.get(id=type_budget)
        pid = utility.generpid(21)

        while len(Budget.objects.filter(pid=pid)) > 0:
            pid = utility.generpid(21)
        form = FormBudget(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.type_budget = type_budget
            f.user = request.user.profile
            f.pid = pid
            f.save()

            if request.htmx:
                return render(request, 'gestionbuget/htmx/create_budgets.html',
                              {"type_budget":type_budget, "budget":f,
                               'htmx': True, "is_success": True, "form": FormBudget(),
                               "budget_sheet":budget_sheet
                               }, status=201)
            return render(request, 'gestionbuget/htmx/create_budgets.html',
                              {"type_budget":type_budget, "budget":f, "budget_sheet":budget_sheet}, status=201)
        return render(request, 'gestionbuget/htmx/create_budgets.html',
                      {"type_budget": type_budget, "form":form, "budget_sheet":budget_sheet})

    return render(request, 'gestionbuget/htmx/create_budgets.html',
                  {"form":FormBudget(), "type_budget":budget_sheet.type_budgets_sheet.last(),
                   "form_section": FormSection()})

@login_required
def create_section(request, pid):
    context = {
        "form": FormSection()
    }
    return render(request, "", )


@login_required
def create_demande(request, pid_sheet):
    form = FormDemande()
    context = {
        "form": form
    }
    print("je suis request ", len(request.GET))
    # try :
    if request.method == "POST":
        user_valideur = request.POST.get("user_validateur", None)
        # type_budget = request.POST.get("type_budget", None)
        pid = request.POST.get("type_budget", None)
        form = FormDemande(request.POST, request.FILES)
        if not pid :
            context = {
                "form": form
            }
            return render(request, "gestionbuget/htmx/demande/created_demande.html", context)

        type_budget_ = request.user.profile.user_type_budgets.get(id=pid, budget_sheet__pid=pid_sheet)
        context["budget_sheet"] = type_budget_.budget_sheet

        pid = utility.generpid(35)
        while len(Demande.objects.filter(pid=pid)) > 0:
            pid = utility.generpid(35)

        # type_budget_ = ""
        # if type_budget:
        #     type_budget_= TypeBudget.objects.filter(budget_sheet=budget_sheet, id=type_budget)

        user_validat = ""
        if user_valideur:
            user_validat = SheetPartener.objects.filter(pid=user_valideur, sheet=type_budget_.budget_sheet).first()

        if form.is_valid() and user_validat and type_budget_:
            print("je suis la pour voir que je suis dedans", user_valideur)
            f = form.save(commit=False)
            f.user = request.user.profile
            f.user_validete = user_validat
            f.type_budget = type_budget_
            f.budget_sheet = type_budget_.budget_sheet
            f.pid = pid
            f.save()




            if request.htmx:
                return render(request,"gestionbuget/htmx/demande/created_demande.html", context,
                              status=201)
            return render(request, "gestionbuget/htmx/demande/created_demande.html", context,
                          status=201)
    # except :
    #     return render(request, 'gestionbuget/budget_sheet_not_found.html', {
    #         'pid_sheet': pid_sheet, "form": form
    #     },status=406)

    return render(request, "gestionbuget/htmx/demande/created_demande.html", context)


@login_required
def manage_users(request, pid):
    """
    Gérer les utilisateurs d'une feuille de budget
    """
    
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid)
    
    # Vérifier que l'utilisateur est propriétaire
    if budget_sheet.user != request.user.profile:
        return redirect('gestionbudget:budget_sheet_detail', pid=pid)
    
    # Récupérer tous les utilisateurs disponibles
    all_users = Profile.objects.exclude(id=budget_sheet.user.id)
    
    # Récupérer les partenaires actuels
    partenaires = SheetPartener.objects.filter(sheet=budget_sheet)
    partenaire_ids = [p.user.id for p in partenaires]
    
    # Utilisateurs disponibles (non encore partenaires)
    available_users = all_users.exclude(id__in=partenaire_ids)
    
    success_message = None
    error_message = None
    show_create_form = False
    
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        
        if action == 'add' and user_id:
            user = get_object_or_404(Profile, id=user_id)
            SheetPartener.objects.create(sheet=budget_sheet, user=user)
            success_message = f'{user} a été ajouté comme partenaire.'
            return redirect('gestionbudget:manage_users', pid=pid)
        
        elif action == 'remove' and user_id:
            partenaire = get_object_or_404(SheetPartener, sheet=budget_sheet, user_id=user_id)
            partenaire.delete()
            success_message = 'Partenaire retiré avec succès.'
            return redirect('gestionbudget:manage_users', pid=pid)
        
        elif action == 'create_user':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            role = request.POST.get('role')
            
            # Validation
            if not username or not email or not password:
                error_message = 'Tous les champs obligatoires doivent être remplis.'
                show_create_form = True
            elif User.objects.filter(username=username).exists():
                error_message = 'Ce nom d\'utilisateur existe déjà.'
                show_create_form = True
            elif User.objects.filter(email=email).exists():
                error_message = 'Cet email est déjà utilisé.'
                show_create_form = True
            else:
                # Créer l'utilisateur Django
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Créer le profil
                if first_name and last_name:
                    profile = user.profile
                    profile.first_name = first_name
                    profile.last_name = last_name
                    profile.save()
                
                if role:
                    pid = utility.generpid(21)
                    while len(SheetPartener.objects.filter(pid=pid)) > 0:
                        pid = utility.generpid(21)
                    SheetPartener.objects.create(sheet=budget_sheet, user=user, role=role, status="accept", pid=pid)

                success_message = f'Utilisateur {username} créé avec succès.'
                return redirect('gestionbudget:manage_users', pid=pid)
    
    context = {
        'budget_sheet': budget_sheet,
        'partenaires': partenaires,
        
        'success_message': success_message,
        'error_message': error_message,
        'show_create_form': show_create_form,
        'role': choise_role,
        'pending_invitations': SheetInvitation.objects.filter(sheet=budget_sheet, status='pending'),
    }
    
    return render(request, 'gestionbuget/manage_users.html', context)


@login_required
def create_user_htmx(request, pid):
    """
    Créer un utilisateur via HTMX et l'ajouter comme partenaire
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid)
    
    # Vérifier que l'utilisateur est propriétaire
    if budget_sheet.user != request.user.profile:
        return render(request, 'gestionbuget/htmx/user_error.html', {
            'error': "Vous n'avez pas les permissions pour créer des utilisateurs."
        }, status=403)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        role = request.POST.get('role', 'consultation')  # Rôle par défaut
        
        # Validation
        if not username or not email or not password:
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Tous les champs obligatoires doivent être remplis.'
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Ce nom d\'utilisateur existe déjà.'
            }, status=400)
        
        if User.objects.filter(email=email).exists():
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Cet email est déjà utilisé.'
            }, status=400)
        
        # Créer l'utilisateur Django
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Créer le profil
        profile, created = Profile.objects.get_or_create(user=user)
        
        # Créer le partenaire avec le rôle
        from .utility import generpid
        partner_pid = generpid(24)
        while SheetPartener.objects.filter(pid=partner_pid).exists():
            partner_pid = generpid(24)
            
        partner = SheetPartener.objects.create(
            sheet=budget_sheet,
            user=profile,
            role=role,
            pid=partner_pid
        )
        
        # Récupérer tous les partenaires pour la mise à jour
        partenaires = SheetPartener.objects.filter(sheet=budget_sheet)
        
        # Créer la réponse avec header HTMX pour fermer le slide-over
        response = render(request, 'gestionbuget/htmx/partners_table.html', {
            'partner': partner,
            'partenaires': partenaires,
            'budget_sheet': budget_sheet,
            'success': f'Utilisateur {username} créé et ajouté avec le rôle {dict(choise_role).get(role, role)}.'
        })
        
        # Ajouter un header HTMX pour déclencher un événement
        response['HX-Trigger'] = 'closeCreateSlide'
        return response
    
    return render(request, 'gestionbuget/htmx/user_error.html', {
        'error': 'Méthode non autorisée.'
    }, status=405)


@login_required
def remove_partner_htmx(request, pid):
    """
    Supprimer un partenaire via HTMX
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid)
    
    # Vérifier que l'utilisateur est propriétaire
    if budget_sheet.user != request.user.profile:
        return render(request, 'gestionbuget/htmx/user_error.html', {
            'error': "Vous n'avez pas les permissions pour supprimer des partenaires."
        }, status=403)
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        
        if user_id:
            try:
                partenaire = SheetPartener.objects.get(sheet=budget_sheet, user_id=user_id)
                username = partenaire.user.user.username
                partenaire.delete()
                
                # Récupérer tous les partenaires pour la mise à jour
                partenaires = SheetPartener.objects.filter(sheet=budget_sheet)
                
                return render(request, 'gestionbuget/htmx/partners_table.html', {
                    'partenaires': partenaires,
                })
            except SheetPartener.DoesNotExist:
                return render(request, 'gestionbuget/htmx/user_error.html', {
                    'error': 'Partenaire non trouvé.'
                }, status=404)
    
    return render(request, 'gestionbuget/htmx/user_error.html', {
        'error': 'Méthode non autorisée.'
    }, status=405)

@login_required
def send_invitation_htmx(request, pid):
    print(f"Vue send_invitation_htmx appelée avec pid: {pid}")
    """
    Envoyer une invitation à un utilisateur existant
    """
    from django.utils import timezone
    from datetime import timedelta
    import secrets
    from django.core.mail import send_mail
    from django.conf import settings
    
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid)
    
    # Vérifier que l'utilisateur est propriétaire
    if budget_sheet.user != request.user.profile:
        return render(request, 'gestionbuget/htmx/user_error.html', {
            'error': "Vous n'avez pas les permissions pour envoyer des invitations."
        }, status=403)
    
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username')
        role = request.POST.get('role', 'consultation')
        
        if not email_or_username:
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Email ou nom d\'utilisateur requis.'
            }, status=400)
        
        # Vérifier si l'utilisateur existe
        user_exists = False
        if '@' in email_or_username:
            user_exists = User.objects.filter(email=email_or_username).exists()
        else:
            user_exists = User.objects.filter(username=email_or_username).exists()
        
        if not user_exists:
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Utilisateur non trouvé dans le système.'
            }, status=404)
        
        # Vérifier si une invitation existe déjà
        existing_invitation = SheetInvitation.objects.filter(
            sheet=budget_sheet,
            email_or_username=email_or_username,
            status='pending'
        ).first()
        
        if existing_invitation:
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Une invitation est déjà en attente pour cet utilisateur.'
            }, status=400)
        
        # Créer l'invitation
        from .utility import generpid
        invitation_pid = generpid(24)
        while SheetInvitation.objects.filter(pid=invitation_pid).exists():
            invitation_pid = generpid(24)
        
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(days=settings.INVITATION_EXPIRE_DAYS)
        
        invitation = SheetInvitation.objects.create(
            pid=invitation_pid,
            sheet=budget_sheet,
            invited_by=request.user.profile,
            email_or_username=email_or_username,
            role=role,
            token=token,
            expires_at=expires_at
        )
        
        # Envoyer l'email d'invitation
        invitation_url = request.build_absolute_uri(f'/gestions-budget/accept_invitation/{token}/')
        
        try:
            send_mail(
                subject=f'Invitation à rejoindre "{budget_sheet.title}"',
                message=f'''
                    Bonjour,

                    {request.user.profile} vous invite à rejoindre la feuille de budget "{budget_sheet.title}" en tant que {role}.

                    Pour accepter cette invitation, cliquez sur le lien suivant :
                    {invitation_url}

                    Cette invitation expire le {expires_at.strftime("%d/%m/%Y à %H:%M")}.

                    Cordialement,
                    L'équipe Budget Manager
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email_or_username if '@' in email_or_username else User.objects.get(username=email_or_username).email],
                fail_silently=False,
            )
        except Exception as e:
            invitation.delete()
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': f'Erreur lors de l\'envoi de l\'email: {str(e)}'
            }, status=500)
        
        # Récupérer les invitations en attente
        pending_invitations = SheetInvitation.objects.filter(sheet=budget_sheet, status='pending')
        
        # Créer la réponse avec header HTMX pour fermer le slide-over
        response = render(request, 'gestionbuget/htmx/invitations_section.html', {
            'invitation': invitation,
            'pending_invitations': pending_invitations,
            'budget_sheet': budget_sheet,
            'success': f'Invitation envoyée à {email_or_username}.'
        })
        
        # Ajouter un header HTMX pour déclencher un événement
        response['HX-Trigger'] = 'closeInviteSlide'
        return response
    
    return render(request, 'gestionbuget/htmx/user_error.html', {
        'error': 'Méthode non autorisée.'
    }, status=405)

@login_required
def accept_invitation(request, token):
    """
    Accepter ou refuser une invitation
    """
    from django.utils import timezone
    
    invitation = get_object_or_404(SheetInvitation, token=token)
    
    # Vérifier si l'invitation a expiré
    if invitation.expires_at < timezone.now():
        invitation.status = 'expired'
        invitation.save()
        return render(request, 'gestionbuget/invitation_expired.html', {'invitation': invitation})
    
    # Vérifier si l'utilisateur connecté correspond à l'invitation
    user_matches = False
    if '@' in invitation.email_or_username:
        user_matches = request.user.email == invitation.email_or_username
    else:
        user_matches = request.user.username == invitation.email_or_username
    
    if not user_matches:
        return render(request, 'gestionbuget/invitation_error.html', {
            'error': 'Cette invitation ne vous est pas destinée.'
        })
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'accept':
            # Créer le partenaire
            from .utility import generpid
            partner_pid = generpid(24)
            while SheetPartener.objects.filter(pid=partner_pid).exists():
                partner_pid = generpid(24)
            
            SheetPartener.objects.create(
                sheet=invitation.sheet,
                user=request.user.profile,
                role=invitation.role,
                pid=partner_pid
            )
            
            invitation.status = 'accepted'
            invitation.save()
            
            return redirect('gestionbudget:budget_sheet_detail', pid=invitation.sheet.pid)
        
        elif action == 'reject':
            invitation.status = 'rejected'
            invitation.save()
            
            return render(request, 'gestionbuget/invitation_rejected.html', {'invitation': invitation})
    
    return render(request, 'gestionbuget/accept_invitation.html', {'invitation': invitation})

@login_required
def demandes_list(request, pid):
    """
    Liste des demandes pour une feuille de budget
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid)
    
    # Vérifier les permissions
    is_owner = budget_sheet.user == request.user.profile
    is_partner = SheetPartener.objects.filter(sheet=budget_sheet, user=request.user.profile).exists()
    
    if not (is_owner or is_partner):
        return redirect('gestionbudget:budget_sheet_list')
    
    # Récupérer les demandes
    demandes = Demande.objects.filter(budget_sheet=budget_sheet).order_by('-created_at')
    
    # Récupérer les types de budget pour le formulaire
    type_budgets = TypeBudget.objects.filter(budget_sheet=budget_sheet)
    
    # Récupérer les validateurs possibles
    possible_validators = get_possible_validators(budget_sheet, request.user.profile)
    
    context = {
        'budget_sheet': budget_sheet,
        'demandes': demandes,
        'type_budgets': type_budgets,
        'possible_validators': possible_validators,
        'is_owner': is_owner,
        'is_partner': is_partner,
        'choise_status': choise_status,
    }
    
    return render(request, 'gestionbuget/demandes_list.html', context)


@login_required
def create_demande_htmx(request, pid):
    """
    Créer une demande via HTMX
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid)
    
    # Vérifier les permissions
    is_partner = SheetPartener.objects.filter(sheet=budget_sheet, user=request.user.profile).exists()
    is_owner = budget_sheet.user == request.user.profile
    
    if not (is_owner or is_partner):
        return render(request, 'gestionbuget/htmx/user_error.html', {
            'error': "Vous n'avez pas les permissions pour créer des demandes."
        }, status=403)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        amount_spent = request.POST.get('amount_spent')
        type_budget_id = request.POST.get('type_budget')
        validator_id = request.POST.get('validator')
        file = request.FILES.get('file')
        
        # Validation
        if not title or not amount_spent or not type_budget_id or not validator_id:
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Tous les champs obligatoires doivent être remplis.'
            }, status=400)
        
        try:
            amount_spent = float(amount_spent)
            type_budget = TypeBudget.objects.get(id=type_budget_id, budget_sheet=budget_sheet)
            
            # Valider le validateur sélectionné
            if validator_id == 'owner':
                # Créer un SheetPartener pour le propriétaire s'il n'existe pas
                validator, created = SheetPartener.objects.get_or_create(
                    sheet=budget_sheet,
                    user=budget_sheet.user,
                    defaults={'role': 'superadmin', 'pid': utility.generpid(24)}
                )
            else:
                validator = SheetPartener.objects.get(id=validator_id, sheet=budget_sheet)
                
        except (ValueError, TypeBudget.DoesNotExist, SheetPartener.DoesNotExist):
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Données invalides.'
            }, status=400)
        
        # Créer la demande
        demande_pid = utility.generpid(24)
        while Demande.objects.filter(pid=demande_pid).exists():
            demande_pid = utility.generpid(24)
        
        # Le validateur a été sélectionné et validé ci-dessus
        
        demande = Demande.objects.create(
            pid=demande_pid,
            title=title,
            description=description,
            amount_spent=amount_spent,
            type_budget=type_budget,
            budget_sheet=budget_sheet,
            user=request.user.profile,
            user_validete=validator,
            file=file
        )
        
        # Récupérer toutes les demandes pour la mise à jour
        demandes = Demande.objects.filter(budget_sheet=budget_sheet).order_by('-created_at')
        
        return render(request, 'gestionbuget/htmx/demandes_table.html', {
            'demandes': demandes,
            'budget_sheet': budget_sheet,
            'success': f'Demande "{title}" créée avec succès.'
        })
    
    return render(request, 'gestionbuget/htmx/user_error.html', {
        'error': 'Méthode non autorisée.'
    }, status=405)


@login_required
def update_demande_status_htmx(request, pid, demande_pid):
    """
    Mettre à jour le statut d'une demande via HTMX
    """
    print(f"Debug: pid={pid}, demande_pid={demande_pid}")
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid)
    print(f"Debug: budget_sheet trouvé: {budget_sheet.title}")
    
    # Vérifier si la demande existe
    try:
        demande = Demande.objects.get(pid=demande_pid, budget_sheet=budget_sheet)
        print(f"Debug: demande trouvée: {demande.title}")
    except Demande.DoesNotExist:
        print(f"Debug: Aucune demande trouvée avec pid={demande_pid}")
        print(f"Debug: Demandes disponibles: {[d.pid for d in Demande.objects.filter(budget_sheet=budget_sheet)]}")
        return render(request, 'gestionbuget/htmx/user_error.html', {
            'error': f'Demande non trouvée (pid: {demande_pid})'
        }, status=404)
    
    # Vérifier les permissions (seul le validateur peut changer le statut)
    can_validate = (
        demande.user_validete and 
        demande.user_validete.user == request.user.profile
    ) or budget_sheet.user == request.user.profile
    
    if not can_validate:
        return render(request, 'gestionbuget/htmx/user_error.html', {
            'error': "Vous n'avez pas les permissions pour valider cette demande."
        }, status=403)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        comment = request.POST.get('comment', '')
        amount_reel = request.POST.get('amount_reel')
        file_reel = request.FILES.get('file_reel')
        
        if new_status not in ['accept', 'reject']:
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Statut invalide.'
            }, status=400)
        
        # Mettre à jour la demande
        print(f"Debug: Ancien statut: {demande.status}")
        demande.status = new_status
        print(f"Debug: Nouveau statut: {demande.status}")
        
        if amount_reel:
            try:
                demande.amount_reel = float(amount_reel)
                print(f"Debug: Montant réel mis à jour: {demande.amount_reel}")
            except ValueError:
                print(f"Debug: Erreur conversion montant réel: {amount_reel}")
                pass
        if file_reel:
            demande.file_reel = file_reel
            print(f"Debug: Fichier réel ajouté: {file_reel.name}")
        
        demande.save()
        print(f"Debug: Demande sauvegardée avec statut: {demande.status}")
        
        # Ajouter un commentaire si fourni
        if comment:
            CommentDemande.objects.create(
                description=comment,
                status=new_status,
                demande=demande,
                user=request.user.profile
            )
        
        # Récupérer toutes les demandes pour la mise à jour
        demandes = Demande.objects.filter(budget_sheet=budget_sheet).order_by('-created_at')
        
        status_text = "acceptée" if new_status == "accept" else "rejetée"
        
        # Créer la réponse avec header HTMX pour fermer le slide-over
        from django.http import HttpResponse
        response = render(request, 'gestionbuget/htmx/demandes_table.html', {
            'demandes': demandes,
            'budget_sheet': budget_sheet,
            'success': f'Demande "{demande.title}" {status_text}.',
            'request': request
        })
        
        # Ajouter un header HTMX pour déclencher un événement
        response['HX-Trigger'] = 'closeValidateSlide'
        return response
    
    return render(request, 'gestionbuget/htmx/user_error.html', {
        'error': 'Méthode non autorisée.'
    }, status=405)

@login_required
def demande_detail(request, pid, demande_pid):
    """
    Détails d'une demande avec commentaires
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid)
    demande = get_object_or_404(Demande, pid=demande_pid, budget_sheet=budget_sheet)
    
    # Vérifier les permissions
    is_owner = budget_sheet.user == request.user.profile
    is_partner = SheetPartener.objects.filter(sheet=budget_sheet, user=request.user.profile).exists()
    is_demandeur = demande.user == request.user.profile
    
    if not (is_owner or is_partner or is_demandeur):
        return redirect('gestionbudget:budget_sheet_list')
    
    # Récupérer les commentaires
    commentaires = CommentDemande.objects.filter(demande=demande).order_by('created_at')
    
    context = {
        'budget_sheet': budget_sheet,
        'demande': demande,
        'commentaires': commentaires,
        'is_owner': is_owner,
        'is_partner': is_partner,
        'is_demandeur': is_demandeur,
        'can_validate': (
            demande.user_validete and 
            demande.user_validete.user == request.user.profile
        ) or is_owner,
    }
    
    return render(request, 'gestionbuget/demande_detail.html', context)


@login_required
def add_comment_htmx(request, pid, demande_pid):
    """
    Ajouter un commentaire à une demande via HTMX
    """
    budget_sheet = get_object_or_404(BudgetSheet, pid=pid)
    demande = get_object_or_404(Demande, pid=demande_pid, budget_sheet=budget_sheet)
    
    # Vérifier les permissions
    is_owner = budget_sheet.user == request.user.profile
    is_partner = SheetPartener.objects.filter(sheet=budget_sheet, user=request.user.profile).exists()
    is_demandeur = demande.user == request.user.profile
    
    if not (is_owner or is_partner or is_demandeur):
        return render(request, 'gestionbuget/htmx/user_error.html', {
            'error': "Vous n'avez pas les permissions pour commenter."
        }, status=403)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        
        if not comment_text:
            return render(request, 'gestionbuget/htmx/user_error.html', {
                'error': 'Le commentaire ne peut pas être vide.'
            }, status=400)
        
        # Créer le commentaire
        CommentDemande.objects.create(
            description=comment_text,
            status='pending',  # Statut par défaut pour les commentaires
            demande=demande,
            user=request.user.profile
        )
        
        # Récupérer tous les commentaires pour la mise à jour
        commentaires = CommentDemande.objects.filter(demande=demande).order_by('created_at')
        
        return render(request, 'gestionbuget/htmx/comments_section.html', {
            'commentaires': commentaires,
            'demande': demande,
            'success': 'Commentaire ajouté avec succès.'
        })
    
    return render(request, 'gestionbuget/htmx/user_error.html', {
        'error': 'Méthode non autorisée.'
    }, status=405)

def get_possible_validators(budget_sheet, user_profile):
    """
    Retourne les validateurs possibles selon la hiérarchie des rôles
    """
    # Hiérarchie des rôles (du plus bas au plus haut)
    role_hierarchy = {
        'consultation': 0,
        'gestionnaire': 1, 
        'gerant': 2,
        'superadmin': 3
    }
    
    # Obtenir le rôle de l'utilisateur actuel
    user_partner = SheetPartener.objects.filter(
        sheet=budget_sheet, 
        user=user_profile
    ).first()
    
    is_owner = budget_sheet.user == user_profile

    
    if is_owner:
        # Le propriétaire peut demander validation à n'importe qui
        user_role_level = 3  # Niveau maximum
    elif user_partner:
        user_role_level = role_hierarchy.get(user_partner.role, 0)
    else:
        return []
    
    # Obtenir tous les partenaires avec un rôle supérieur
    possible_validators = []
    
    # Ajouter le propriétaire comme option
    if not is_owner:
        possible_validators.append({
            'id': 'owner',
            'name': f"{budget_sheet.user.user.get_full_name() or budget_sheet.user.user.username} (Propriétaire)",
            'role': 'Propriétaire'
        })
    

    # Ajouter les partenaires avec rôle supérieur
    for partner in SheetPartener.objects.filter(sheet=budget_sheet):
        partner_role_level = role_hierarchy.get(partner.role, 0)
        # Inclure si le rôle est supérieur ou égal (pour permettre validation entre pairs)
        if partner_role_level >= user_role_level and partner.user != user_profile:
            role_display = dict(choise_role).get(partner.role, partner.role)
            possible_validators.append({
                'id': partner.id,
                'name': f"{partner.user.user.get_full_name() or partner.user.user.username}",
                'role': role_display
            })
    
    return possible_validators
