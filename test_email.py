#!/usr/bin/env python
"""
Script de test pour la configuration email
Usage: python test_email.py destinataire@example.com
"""

import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zcabinet.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_config(recipient_email):
    """Test la configuration email en envoyant un email de test"""
    
    print("🔧 Configuration Email:")
    print(f"   Backend: {settings.EMAIL_BACKEND}")
    print(f"   Host: {settings.EMAIL_HOST}")
    print(f"   Port: {settings.EMAIL_PORT}")
    print(f"   TLS: {settings.EMAIL_USE_TLS}")
    print(f"   User: {settings.EMAIL_HOST_USER}")
    print(f"   From: {settings.DEFAULT_FROM_EMAIL}")
    print()
    
    try:
        print(f"📧 Envoi d'un email de test à {recipient_email}...")
        
        send_mail(
            subject='Test Email - Budget Manager',
            message='''
Bonjour,

Ceci est un email de test pour vérifier la configuration SMTP de Budget Manager.

Si vous recevez cet email, la configuration fonctionne correctement !

Cordialement,
L'équipe Budget Manager
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        
        print("✅ Email envoyé avec succès !")
        
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            print("ℹ️  Mode console activé - l'email s'affiche ci-dessus au lieu d'être envoyé")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi: {e}")
        print("\n🔍 Vérifications à faire:")
        print("   1. Vérifiez vos identifiants SMTP dans le fichier .env")
        print("   2. Assurez-vous que EMAIL_HOST_USER et EMAIL_HOST_PASSWORD sont corrects")
        print("   3. Pour Gmail, utilisez un mot de passe d'application")
        print("   4. Vérifiez que le serveur SMTP autorise les connexions")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_email.py destinataire@example.com")
        sys.exit(1)
    
    recipient = sys.argv[1]
    test_email_config(recipient)
