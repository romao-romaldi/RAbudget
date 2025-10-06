# Configuration Email pour les Invitations

## Configuration rapide

1. **Copiez le fichier d'exemple** :
   ```bash
   cp .env.example .env
   ```

2. **Modifiez le fichier `.env`** avec vos paramètres email

## Configuration Gmail (Recommandée pour les tests)

### Étapes :

1. **Activez l'authentification à 2 facteurs** sur votre compte Gmail
2. **Générez un mot de passe d'application** :
   - Allez dans les paramètres de votre compte Google
   - Sécurité → Authentification à 2 facteurs → Mots de passe des applications
   - Générez un mot de passe pour "Django App"

3. **Configurez le fichier `.env`** :
   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=votre-email@gmail.com
   EMAIL_HOST_PASSWORD=votre-mot-de-passe-app-genere
   DEFAULT_FROM_EMAIL=votre-email@gmail.com
   ```

## Configuration Outlook/Hotmail

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@outlook.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe
DEFAULT_FROM_EMAIL=votre-email@outlook.com
```

## Configuration Yahoo Mail

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@yahoo.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=votre-email@yahoo.com
```

## Configuration pour serveur SMTP personnalisé

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.votre-domaine.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@votre-domaine.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe
DEFAULT_FROM_EMAIL=noreply@votre-domaine.com
```

## Mode Test (Console)

Pour les tests en développement, utilisez :

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Les emails s'afficheront dans la console du serveur Django au lieu d'être envoyés.

## Variables disponibles

| Variable | Description | Défaut |
|----------|-------------|---------|
| `EMAIL_BACKEND` | Backend d'envoi d'email | `console.EmailBackend` |
| `EMAIL_HOST` | Serveur SMTP | `smtp.gmail.com` |
| `EMAIL_PORT` | Port SMTP | `587` |
| `EMAIL_USE_TLS` | Utiliser TLS | `True` |
| `EMAIL_HOST_USER` | Nom d'utilisateur SMTP | `` |
| `EMAIL_HOST_PASSWORD` | Mot de passe SMTP | `` |
| `DEFAULT_FROM_EMAIL` | Email expéditeur par défaut | `noreply@budgetmanager.com` |
| `INVITATION_EXPIRE_DAYS` | Durée de validité des invitations (jours) | `7` |

## Test de la configuration

Pour tester votre configuration email :

```bash
python manage.py shell
```

```python
from django.core.mail import send_mail

send_mail(
    'Test Email',
    'Ceci est un email de test.',
    'from@example.com',
    ['to@example.com'],
    fail_silently=False,
)
```

## Sécurité

⚠️ **Important** :
- Ne commitez jamais le fichier `.env` dans votre repository
- Utilisez des mots de passe d'application pour Gmail
- Gardez vos identifiants email sécurisés
