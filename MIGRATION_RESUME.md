# Migration de l'application Resume

## Commandes à exécuter

Après avoir créé l'application `resume`, vous devez créer et appliquer les migrations :

```bash
# 1. Créer les migrations
python manage.py makemigrations resume

# 2. Appliquer les migrations
python manage.py migrate resume

# 3. (Optionnel) Créer un superutilisateur si ce n'est pas déjà fait
python manage.py createsuperuser
```

## Vérification

Pour vérifier que tout fonctionne :

```bash
# Vérifier les migrations
python manage.py showmigrations resume

# Lancer le serveur
python manage.py runserver
```

## Accès

Une fois le serveur lancé, accédez à :
- **Admin** : http://127.0.0.1:8000/admin/
- **Résumés** : http://127.0.0.1:8000/resumes/{pid_sheet}/

## Structure créée

L'application `resume` comprend :

### Modèles
- **Resume** : Résumés journaliers
- **Hierarchie** : Relations hiérarchiques entre utilisateurs
- **CommentResume** : Commentaires sur les résumés

### Fonctionnalités
- Création de résumés liés à une feuille de budget
- Système hiérarchique avec envoi automatique au supérieur
- Workflow de validation (Brouillon → Soumis → Validé/Rejeté)
- Commentaires et feedback
- Historique des modifications

### URLs disponibles
- `/resumes/<pid_sheet>/` - Liste des résumés
- `/resumes/<pid_sheet>/create/` - Créer un résumé
- `/resumes/<pid_sheet>/<pid_resume>/` - Détails d'un résumé
- `/resumes/<pid_sheet>/<pid_resume>/edit/` - Modifier un résumé
- `/resumes/<pid_sheet>/<pid_resume>/submit/` - Soumettre un résumé
- `/resumes/<pid_sheet>/<pid_resume>/validate/` - Valider un résumé
- `/resumes/<pid_sheet>/<pid_resume>/reject/` - Rejeter un résumé
- `/resumes/<pid_sheet>/hierarchie/manage/` - Gérer la hiérarchie

## Prochaines étapes

1. Exécuter les migrations
2. Définir la hiérarchie dans une feuille de budget
3. Créer des résumés journaliers
4. Tester le workflow de validation

## Notes importantes

- Un résumé est **obligatoirement lié** à une feuille de budget
- Un résumé n'est visible que dans la feuille où il a été créé
- La hiérarchie est définie **par feuille de budget** (un utilisateur peut avoir différents supérieurs selon les feuilles)
- Les résumés en brouillon peuvent être modifiés, mais pas après soumission
