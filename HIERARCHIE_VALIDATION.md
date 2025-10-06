# 🏛️ Hiérarchie de Validation des Demandes

## 📋 Système de Validation Hiérarchique

Le système permet maintenant au **demandeur de choisir son validateur** selon une hiérarchie de rôles bien définie.

## 🎯 Hiérarchie des Rôles

### Niveaux (du plus bas au plus haut) :
1. **👤 Consultation** (niveau 0)
2. **📊 Gestionnaire** (niveau 1) 
3. **🏢 Gérant** (niveau 2)
4. **👑 Super Admin** (niveau 3)
5. **🔑 Propriétaire** (niveau maximum)

## ✅ Règles de Validation

### 🟢 **Consultation** peut demander validation à :
- ✅ **Gestionnaire** (niveau supérieur)
- ✅ **Gérant** (niveau supérieur)
- ✅ **Super Admin** (niveau supérieur)
- ✅ **Propriétaire** (toujours disponible)

### 🟡 **Gestionnaire** peut demander validation à :
- ✅ **Gérant** (niveau supérieur)
- ✅ **Super Admin** (niveau supérieur)
- ✅ **Propriétaire** (toujours disponible)
- ❌ ~~Consultation~~ (niveau inférieur)

### 🟠 **Gérant** peut demander validation à :
- ✅ **Super Admin** (niveau supérieur)
- ✅ **Propriétaire** (toujours disponible)
- ❌ ~~Gestionnaire~~ (niveau inférieur)
- ❌ ~~Consultation~~ (niveau inférieur)

### 🔴 **Super Admin** peut demander validation à :
- ✅ **Propriétaire** (seul niveau supérieur)
- ❌ ~~Gérant~~ (niveau inférieur)
- ❌ ~~Gestionnaire~~ (niveau inférieur)
- ❌ ~~Consultation~~ (niveau inférieur)

### 👑 **Propriétaire** peut demander validation à :
- ✅ **Tous les rôles** (peut choisir n'importe qui)

## 🔧 Fonctionnement Technique

### 1. **Sélection du Validateur**
```html
<select name="validator" required>
    <option value="">Sélectionner un validateur</option>
    {% for validator in possible_validators %}
    <option value="{{ validator.id }}">
        {{ validator.name }} - {{ validator.role }}
    </option>
    {% endfor %}
</select>
```

### 2. **Logique de Filtrage**
```python
def get_possible_validators(budget_sheet, user_profile):
    # Hiérarchie des rôles
    role_hierarchy = {
        'consultation': 0,
        'gestionnaire': 1, 
        'gerant': 2,
        'superadmin': 3
    }
    
    # Filtrer selon le niveau hiérarchique
    # Inclure uniquement les rôles supérieurs ou égaux
```

### 3. **Validation Backend**
```python
# Vérifier que le validateur sélectionné est autorisé
if validator_id == 'owner':
    # Propriétaire toujours autorisé
    validator = get_or_create_owner_partner()
else:
    # Vérifier que le partenaire existe et a les permissions
    validator = SheetPartener.objects.get(id=validator_id)
```

## 📊 Exemples Pratiques

### Cas 1: Utilisateur "Consultation"
**Peut choisir parmi :**
- Marie Dupont - Gestionnaire
- Jean Martin - Gérant  
- Admin Système - Super Admin
- Pierre Durand (Propriétaire)

### Cas 2: Utilisateur "Gestionnaire"
**Peut choisir parmi :**
- Jean Martin - Gérant
- Admin Système - Super Admin  
- Pierre Durand (Propriétaire)

### Cas 3: Utilisateur "Gérant"
**Peut choisir parmi :**
- Admin Système - Super Admin
- Pierre Durand (Propriétaire)

## 🎨 Interface Utilisateur

### Formulaire de Demande :
1. **Titre** *(obligatoire)*
2. **Type de budget** *(obligatoire)*
3. **Montant** *(obligatoire)*
4. **🆕 Validateur** *(obligatoire)* ← **NOUVEAU**
5. **Description** *(optionnel)*
6. **Fichier** *(optionnel)*

### Affichage du Sélecteur :
```
┌─────────────────────────────────────┐
│ Validateur *                        │
│ ┌─────────────────────────────────┐ │
│ │ Sélectionner un validateur    ▼ │ │
│ └─────────────────────────────────┘ │
│ Choisissez la personne qui validera │
│ votre demande                       │
└─────────────────────────────────────┘
```

## 🔄 Workflow Complet

1. **Création de demande** → Sélection du validateur selon hiérarchie
2. **Soumission** → Validation backend des permissions
3. **Notification** → Le validateur choisi reçoit la demande
4. **Validation** → Accept/Reject par le validateur sélectionné

## ✨ Avantages

- ✅ **Flexibilité** : Le demandeur choisit son validateur
- ✅ **Hiérarchie respectée** : Seuls les rôles supérieurs disponibles
- ✅ **Transparence** : Validation claire et traçable
- ✅ **Sécurité** : Contrôles backend stricts
- ✅ **UX améliorée** : Interface intuitive avec rôles affichés
