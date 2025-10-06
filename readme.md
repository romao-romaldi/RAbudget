# ZCabinet - Gestion Budgétaire pour Petites Entreprises et Particuliers

## 📋 Description

**ZCabinet** est une application web de gestion budgétaire conçue pour aider les petites entreprises et les particuliers à gérer efficacement leurs finances. L'application permet de suivre les dépenses, les revenus, l'épargne et offre des fonctionnalités collaboratives pour les équipes.

## 🎯 Objectifs

- **Pour les particuliers** : Gérer son budget personnel, suivre ses dépenses et revenus, planifier son épargne
- **Pour les petites entreprises** : 
  - Gestion collaborative des budgets avec système de rôles
  - Workflow de validation des demandes de dépenses
  - Résumés quotidiens avec éditeur riche
  - Statistiques et visualisations des finances
  - Interface intuitive et facile à utiliser

## ✨ Fonctionnalités Principales

### 📊 Gestion Budgétaire (`gestionbuget`)

#### Feuilles de Budget
- **Création de budgets multiples** : Gérez plusieurs budgets séparés (personnel, professionnel, projets)
- **Support multi-devises** : FCFA, USD, EUR, GBP, JPY, CNY, INR, AUD, CAD, CHF
- **Types de budget personnalisables** :
  - Revenus
  - Dépenses
  - Salaires
  - Comptes d'épargne
  - Catégories personnalisées

#### Système de Demandes de Dépenses
- **Création de demandes** avec :
  - Titre et description
  - Montant prévu
  - Montant réel (après validation)
  - Justificatifs (upload de fichiers)
- **Workflow de validation** :
  - Statuts : En attente → Accepté/Rejeté
  - Assignation d'un validateur
  - Système de commentaires
  - Historique des modifications

#### Collaboration d'Équipe
- **Partage de feuilles de budget** avec différents rôles :
  - **SuperAdmin** : Contrôle total (création, modification, suppression, validation)
  - **Gérant** : Gestion et validation des demandes
  - **Gestionnaire** : Saisie et suivi des budgets
  - **Consultation** : Lecture seule des données

#### Statistiques et Visualisations
- **Graphiques mensuels** : Évolution des budgets par type
- **Statistiques journalières** : Suivi détaillé par jour
- **Filtrage par période** : Analyse sur mesure
- **Comparaison prévu vs réel** : Écarts budgétaires

### ✅ Gestion des Tâches (`todo`)

- **Création et suivi de tâches** avec :
  - Statuts : En attente, En cours, Terminé, Archivé
  - Niveaux de priorité
  - Dates d'exécution planifiées
- **Collaboration** :
  - Assignation de responsables multiples
  - Système de validation des tâches
  - Commentaires et discussions
- **Historique** : Suivi complet des tâches terminées

### 📝 Rapports Journaliers (`resume`)

- **Création de rapports quotidiens** :
  - Rapport des activités et réalisations de la journée
  - Lié obligatoirement à une feuille de budget
  - Visible uniquement dans la feuille concernée
- **Système hiérarchique** :
  - Définition de la hiérarchie par feuille de budget
  - Envoi automatique au supérieur hiérarchique
  - Workflow de validation (Brouillon → Soumis → Validé/Rejeté)
- **Collaboration** :
  - Commentaires et feedback du supérieur
  - Historique des validations
  - Notifications de statut

### 👤 Gestion des Utilisateurs (`customuser`)

- **Profils utilisateurs étendus** :
  - Informations personnelles (nom, prénom)
  - Coordonnées (téléphone, adresse, ville, pays)
  - Biographie
- **Identifiants uniques** (UUID) pour chaque profil

## 🛠️ Stack Technique

### Backend
- **Django 4.0.4** - Framework web Python robuste et sécurisé
- **SQLite** - Base de données (développement)
- **Python 3.11** - Langage de programmation

### Frontend
- **TailwindCSS 3** - Framework CSS utility-first pour un design moderne
- **Alpine.js** - Framework JavaScript léger (15kb) pour l'interactivité
- **HTMX** - Interactions AJAX modernes sans JavaScript complexe

### Packages Django
- `django-tailwind` - Intégration TailwindCSS dans Django
- `django-htmx` - Support HTMX pour requêtes partielles
- `django_browser_reload` - Rechargement automatique en développement

### Pourquoi cette stack ?

✅ **Légère et performante** : Pas de framework JS lourd (React/Vue)
✅ **Développement rapide** : TailwindCSS + Alpine.js = productivité maximale
✅ **Expérience utilisateur moderne** : Interactions fluides avec HTMX
✅ **Maintenabilité** : Code simple et facile à comprendre

## 📁 Structure du Projet

```
zcabinet/
├── customuser/          # Gestion des utilisateurs et profils
│   ├── models.py        # Modèle Profile étendu
│   ├── admin.py
│   └── migrations/
├── gestionbuget/        # Module principal de gestion budgétaire
│   ├── models.py        # BudgetSheet, TypeBudget, Budget, Demande
│   ├── views.py         # Vues et logique métier
│   ├── forms.py         # Formulaires Django
│   ├── urls.py          # Routes du module
│   ├── utility.py       # Fonctions utilitaires (génération PID, stats)
│   ├── templates/       # Templates HTML
│   │   ├── gestionbuget/
│   │   └── htmx/        # Composants HTMX partiels
│   └── templatetags/    # Tags de template personnalisés

├── todo/                # Gestion des tâches
│   ├── models.py        # Todo, TodoComment, TodoValidation
│   ├── views.py
│   └── templates/
├── resume/              # Rapports journaliers
│   ├── models.py        # Resume, Hierarchie, CommentResume
│   ├── views.py         # Vues de gestion des rapports
│   ├── forms.py         # Formulaires
│   ├── urls.py          # Routes du module
│   ├── utility.py       # Génération PID
│   └── templates/       # Templates HTML
│       └── resume/
├── theme/               # Configuration TailwindCSS
│   ├── static/
│   └── templates/
├── templates/           # Templates globaux
│   └── base.html        # Template de base avec Alpine.js
├── static/              # Fichiers statiques (CSS, JS, images)
├── media/               # Fichiers uploadés par les utilisateurs
├── zcabinet/            # Configuration Django
│   ├── settings.py      # Configuration principale
│   ├── urls.py          # Routes principales
│   ├── wsgi.py
│   └── asgi.py
├── manage.py            # Script de gestion Django
├── requirements.txt     # Dépendances Python
├── readme.md            # Ce fichier
└── db.sqlite3           # Base de données SQLite
```

## 🚀 Installation

### Prérequis
- Python 3.11 ou supérieur
- Node.js 16+ (pour TailwindCSS)
- pip (gestionnaire de paquets Python)

### Étapes d'installation

#### 1. Cloner le projet
```bash
git clone <repository-url>
cd zcabinet
```

#### 2. Créer un environnement virtuel
```bash
python -m venv env

# Linux/Mac
source env/bin/activate

# Windows
env\Scripts\activate
```

#### 3. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

#### 4. Installer TailwindCSS
```bash
python manage.py tailwind install
```

#### 5. Appliquer les migrations
```bash
python manage.py migrate
```

#### 6. Créer un superutilisateur
```bash
python manage.py createsuperuser
```
Suivez les instructions pour créer votre compte administrateur.

#### 7. Lancer le serveur de développement

**Terminal 1** - Serveur Django :
```bash
python manage.py runserver
```

**Terminal 2** - Compilation TailwindCSS :
```bash
python manage.py tailwind start
```

#### 8. Accéder à l'application

Ouvrez votre navigateur et accédez à :
- **Application** : http://127.0.0.1:8000/
- **Admin Django** : http://127.0.0.1:8000/admin/
- **Gestion Budget** : http://127.0.0.1:8000/gestions-budget/
- **Rapports** : http://127.0.0.1:8000/resumes/{pid_sheet}/
- **Todos** : http://127.0.0.1:8000/todo/

## 📖 Guide d'Utilisation

### Créer une feuille de budget

1. Connectez-vous à l'application
2. Accédez à **Gestion Budget** (`/gestions-budget/`)
3. Cliquez sur **"Créer une feuille de budget"**
4. Remplissez :
   - **Titre** : Ex. "Budget Entreprise 2025"
   - **Description** : Objectifs et détails
   - **Devise** : Choisissez votre devise
5. Validez : La feuille est créée avec des types de budget par défaut

### Ajouter des types de budget

1. Ouvrez une feuille de budget
2. Créez des catégories personnalisées :
   - **Revenus** : Ventes, prestations, etc.
   - **Dépenses** : Loyer, fournitures, marketing, etc.
   - **Salaires** : Rémunérations du personnel
   - **Épargne** : Objectifs d'économie

### Inviter des collaborateurs

1. Dans une feuille de budget, section **"Partenaires"**
2. Cliquez sur **"Inviter un partenaire"**
3. Sélectionnez l'utilisateur
4. Choisissez le rôle :
   - **SuperAdmin** : Accès complet
   - **Gérant** : Validation des demandes
   - **Gestionnaire** : Saisie des données
   - **Consultation** : Lecture seule
5. Validez l'invitation

### Créer une demande de dépense

1. Sélectionnez un type de budget
2. Cliquez sur **"Nouvelle demande"**
3. Remplissez :
   - **Titre** : Ex. "Achat ordinateurs"
   - **Description** : Justification détaillée
   - **Montant prévu** : Budget estimé
   - **Justificatif** : Upload de devis/facture
   - **Validateur** : Choisissez qui doit approuver
4. Soumettez la demande

### Valider une demande

1. Le validateur reçoit la demande (statut : **En attente**)
2. Il peut :
   - **Consulter** les détails et justificatifs
   - **Commenter** pour demander des précisions
   - **Accepter** : La demande est approuvée
   - **Rejeter** : La demande est refusée avec motif
3. Si acceptée, saisir le **montant réel** dépensé

### Consulter les statistiques

1. Dans une feuille de budget, onglet **"Statistiques"**
2. Visualisez :
   - **Graphiques mensuels** par type de budget
   - **Évolution journalière** des dépenses/revenus
   - **Comparaison prévu vs réel**
3. Filtrez par période avec le sélecteur de date

### Gérer les tâches (Todo)

1. Accédez à **Todos** (`/todo/`)
2. Créez une tâche :
   - Titre et description
   - Priorité (haute, moyenne, basse)
   - Date d'exécution
   - Responsables
3. Suivez l'avancement avec les statuts
4. Ajoutez des commentaires
5. Validez les tâches terminées

### Créer et gérer des rapports journaliers

#### Définir la hiérarchie

1. Ouvrez une feuille de budget
2. Accédez à **Rapports** puis **Gérer la hiérarchie**
3. Définissez les relations hiérarchiques :
   - Sélectionnez un utilisateur
   - Choisissez son supérieur hiérarchique
   - Validez

#### Créer un rapport

1. Dans une feuille de budget, accédez à **Rapports**
2. Cliquez sur **Nouveau rapport**
3. Remplissez :
   - **Titre** : Ex. "Rapport du 04/10/2025"
   - **Date** : Date de la journée
   - **Contenu** : Activités et réalisations détaillées
4. Le rapport est créé en mode **Brouillon**

#### Soumettre un rapport

1. Ouvrez votre rapport en brouillon
2. Vérifiez le contenu
3. Cliquez sur **Soumettre au supérieur**
4. Le rapport est envoyé automatiquement à votre supérieur hiérarchique

#### Valider un rapport (en tant que supérieur)

1. Accédez à **Rapports reçus**
2. Ouvrez le rapport à valider
3. Lisez le contenu
4. Options :
   - **Valider** : Approuver le rapport
   - **Rejeter** : Refuser avec commentaire
   - **Commenter** : Demander des précisions

## 🔧 Configuration

### Paramètres importants (`zcabinet/settings.py`)

```python
# Langue de l'interface
LANGUAGE_CODE = 'fr-fr'

# Fuseau horaire
TIME_ZONE = 'UTC'

# Mode debug (DÉSACTIVER EN PRODUCTION)
DEBUG = True

# Hôtes autorisés (CONFIGURER EN PRODUCTION)
ALLOWED_HOSTS = ["*", "127.0.0.1", "localhost"]

# Applications installées
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    
    # Custom apps
    "customuser",
    "todo",
    "gestionbuget",
    "resume",
    
    # External apps
    'tailwind',
    'theme',
    "django_htmx",
    'django_browser_reload'
]
```

### Devises supportées

- **FCFA** - Franc CFA
- **USD** - Dollar américain
- **EUR** - Euro
- **GBP** - Livre sterling
- **JPY** - Yen japonais
- **CNY** - Yuan chinois
- **INR** - Roupie indienne
- **AUD** - Dollar australien
- **CAD** - Dollar canadien
- **CHF** - Franc suisse

## 🔐 Sécurité

### ⚠️ Avant la mise en production

**CRITIQUE** - Ces modifications sont **OBLIGATOIRES** :

1. **Changer la SECRET_KEY**
```python
# settings.py
import secrets
SECRET_KEY = secrets.token_urlsafe(50)
```

2. **Désactiver le mode DEBUG**
```python
DEBUG = False
```

3. **Configurer ALLOWED_HOSTS**
```python
ALLOWED_HOSTS = ['votre-domaine.com', 'www.votre-domaine.com']
```

4. **Utiliser une base de données robuste**
```python
# PostgreSQL (recommandé)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'zcabinet_db',
        'USER': 'votre_user',
        'PASSWORD': 'votre_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. **Configurer HTTPS**
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

6. **Gérer les fichiers statiques**
```bash
python manage.py collectstatic
```

7. **Utiliser un serveur WSGI** (Gunicorn, uWSGI)
```bash
gunicorn zcabinet.wsgi:application
```

### Bonnes pratiques

- ✅ Utiliser des variables d'environnement pour les secrets
- ✅ Sauvegardes régulières de la base de données
- ✅ Logs d'activité et monitoring
- ✅ Mises à jour régulières des dépendances
- ✅ Tests de sécurité périodiques

## 🐛 Bugs Corrigés

### Version actuelle

✅ **Corrigé** - `gestionbuget/views.py` ligne 189 : Syntaxe `with` → `while` et `Budget.object` → `Budget.objects`
✅ **Corrigé** - `gestionbuget/models.py` ligne 169 : Double assignation `models.name =` supprimée
✅ **Corrigé** - `customuser/models.py` ligne 12 : `uuid.uuid4()` → `uuid.uuid4` (fonction, pas appel)

## 🚧 Roadmap / TODO

### Court terme
- [ ] Ajouter des tests unitaires
- [ ] Implémenter l'éditeur riche (TinyMCE/CKEditor) pour les résumés quotidiens
- [ ] Système de notifications en temps réel
- [ ] Export PDF des budgets et rapports
- [ ] Tableau de bord avec widgets personnalisables

### Moyen terme
- [ ] API REST (Django REST Framework) pour application mobile
- [ ] Application mobile (React Native / Flutter)
- [ ] Intégration avec services bancaires (Open Banking)
- [ ] Rapports automatiques par email
- [ ] Multi-langue (i18n)

### Long terme
- [ ] Intelligence artificielle pour prédictions budgétaires
- [ ] Analyse des tendances et recommandations
- [ ] Intégration comptabilité (export vers logiciels comptables)
- [ ] Mode hors-ligne (PWA)

## 🧪 Tests

### Lancer les tests
```bash
python manage.py test
```

### Tests par application
```bash
python manage.py test gestionbuget
python manage.py test todo
python manage.py test customuser
python manage.py test resume
```

## 📊 Modèles de Données

### Module Gestion Budget

**BudgetSheet** : Feuille de budget principale
- `pid` : Identifiant unique
- `title` : Titre
- `description` : Description
- `currency` : Devise
- `user` : Propriétaire

**TypeBudget** : Catégorie de budget
- `name` : Nom du type
- `is_income` : Est un revenu
- `is_spent` : Est une dépense
- `is_salary` : Est un salaire
- `budget_sheet` : Feuille parente

**Budget** : Entrée budgétaire
- `title` : Titre
- `amount_spent` : Montant prévu
- `amount_reel` : Montant réel
- `type_budget` : Type
- `user` : Créateur

**Demande** : Demande de dépense
- `title` : Titre
- `amount_spent` : Montant demandé
- `amount_reel` : Montant réel
- `status` : pending/accept/reject
- `file` : Justificatif
- `user_validete` : Validateur

**SheetPartener** : Partenaire d'une feuille
- `role` : superadmin/gerant/gestionnaire/consultation
- `sheet` : Feuille partagée
- `user` : Utilisateur partenaire

### Module Rapports Journaliers

**Resume** : Rapport journalier
- `pid` : Identifiant unique
- `title` : Titre du rapport
- `content` : Contenu détaillé
- `date_resume` : Date de la journée
- `status` : draft/submitted/validated/rejected
- `budget_sheet` : Feuille de budget liée
- `author` : Auteur du rapport
- `destinataire` : Supérieur hiérarchique

**Hierarchie** : Relation hiérarchique
- `user` : Utilisateur
- `superieur` : Supérieur hiérarchique
- `budget_sheet` : Feuille de budget concernée

**CommentResume** : Commentaire sur un rapport
- `resume` : Rapport concerné
- `author` : Auteur du commentaire
- `content` : Contenu du commentaire

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. Créez une **branche** pour votre fonctionnalité
   ```bash
   git checkout -b feature/ma-fonctionnalite
   ```
3. **Committez** vos changements
   ```bash
   git commit -m "Ajout de ma fonctionnalité"
   ```
4. **Pushez** vers la branche
   ```bash
   git push origin feature/ma-fonctionnalite
   ```
5. Ouvrez une **Pull Request**

### Guidelines

- Code propre et commenté
- Respecter la structure existante
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation

## 📄 Licence

À définir

## 📧 Support

Pour toute question, suggestion ou problème :

- **Issues GitHub** : Ouvrez une issue
- **Email** : contact@zcabinet.com (à configurer)
- **Documentation** : Consultez ce README

## 🙏 Remerciements

Merci à tous les contributeurs et à la communauté open-source pour les outils utilisés :

- Django Team
- TailwindCSS
- Alpine.js
- HTMX

---

**Développé avec ❤️ pour simplifier la gestion budgétaire des petites entreprises et particuliers**

*ZCabinet - Votre partenaire pour une gestion financière efficace et collaborative*