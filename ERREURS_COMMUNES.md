# 🚨 Erreurs Communes et Solutions

## ✅ Erreurs Normales (à ignorer)

### 1. **Chrome DevTools**
```
Not Found: /.well-known/appspecific/com.chrome.devtools.json
[05/Oct/2025 14:26:42] "GET /.well-known/appspecific/com.chrome.devtools.json HTTP/1.1" 404 3610
```
**🟢 NORMAL** - Chrome cherche ses outils de développement. Pas d'impact sur l'application.

### 2. **CKEditor Warning**
```
?: (ckeditor.W001) django-ckeditor bundles CKEditor 4.22.1 which isn't supported anymore...
```
**🟡 WARNING** - Version obsolète de CKEditor. Fonctionne mais à mettre à jour plus tard.

## ❌ Erreurs à Corriger

### 1. **Template Syntax Error**
```
TemplateSyntaxError: Could not parse the remainder: '(demande.user_validete.user' from '(demande.user_validete.user'
```
**🔴 ERREUR** - Parenthèses mal fermées dans les templates Django.

**Solution :** Vérifier la syntaxe des conditions `{% if %}` dans les templates.

### 2. **No Demande matches the given query**
```
DoesNotExist: No Demande matches the given query
```
**🔴 ERREUR** - Demande introuvable avec l'ID fourni.

**Solutions :**
- Vérifier que l'ID de la demande est correct
- Ajouter des logs de debug pour tracer les IDs
- Vérifier les permissions d'accès

### 3. **CSRF Token Missing**
```
Forbidden (CSRF token missing or incorrect)
```
**🔴 ERREUR** - Token CSRF manquant dans les formulaires.

**Solution :** Ajouter `{% csrf_token %}` dans tous les formulaires.

## 🔧 Debug Tips

### 1. **Logs Django**
```python
print(f"Debug: variable = {variable}")
```

### 2. **Console JavaScript**
```javascript
console.log('Debug:', variable);
```

### 3. **Template Debug**
```django
{{ variable|pprint }}  <!-- Affiche la structure -->
{% debug %}            <!-- Affiche le contexte -->
```

## 🎯 Commandes Utiles

### Vérifier la syntaxe
```bash
python manage.py check
```

### Tester les templates
```bash
python manage.py shell
```

### Logs en temps réel
```bash
tail -f logs/django.log
```

## 📋 Checklist de Debug

- [ ] Vérifier la syntaxe des templates (`{% if %}` fermés)
- [ ] Confirmer que les IDs existent en base
- [ ] Vérifier les permissions utilisateur
- [ ] Ajouter des logs de debug
- [ ] Tester avec des données réelles
- [ ] Vérifier les tokens CSRF
