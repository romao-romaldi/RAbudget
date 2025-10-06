from django.db import models
from gestionbuget.models import BudgetSheet
from customuser.models import Profile
from ckeditor.fields import RichTextField


# Choix de statut pour les rapports
STATUS_CHOICES = (
    ('draft', 'Brouillon'),
    ('submitted', 'Soumis'),
    ('validated', 'Validé'),
    ('rejected', 'Rejeté'),
)


class Hierarchie(models.Model):
    """
    Définit la hiérarchie entre les utilisateurs pour l'envoi des rapports.
    Un utilisateur peut avoir un supérieur hiérarchique.
    """
    user = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='hierarchie',
        verbose_name='Utilisateur'
    )
    superieur = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordonnes',
        verbose_name='Supérieur hiérarchique'
    )
    budget_sheet = models.ForeignKey(
        BudgetSheet,
        on_delete=models.CASCADE,
        related_name='hierarchies',
        verbose_name='Feuille de budget'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hiérarchie'
        verbose_name_plural = 'Hiérarchies'
        unique_together = ['user', 'budget_sheet']
        ordering = ['budget_sheet', 'user']

    def __str__(self):
        if self.superieur:
            return f"{self.user} → {self.superieur} ({self.budget_sheet.title})"
        return f"{self.user} (pas de supérieur) ({self.budget_sheet.title})"


class Resume(models.Model):
    """
    Rapport journalier créé par un utilisateur et lié à une feuille de budget.
    Le rapport est envoyé au supérieur hiérarchique de l'utilisateur.
    """
    pid = models.CharField(
        max_length=100,
        unique=True,
        help_text="Identifiant unique du rapport"
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Titre'
    )
    content = RichTextField(
        verbose_name='Contenu du rapport',
        help_text='Décrivez les activités et réalisations de la journée',
        config_name='default'
    )
    date_resume = models.DateField(
        verbose_name='Date du rapport',
        help_text='Date de la journée rapportée'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Statut'
    )
    
    # Relations
    budget_sheet = models.ForeignKey(
        BudgetSheet,
        on_delete=models.CASCADE,
        related_name='resumes',
        verbose_name='Feuille de budget'
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='resumes_authored',
        verbose_name='Auteur'
    )
    destinataire = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resumes_received',
        verbose_name='Destinataire (supérieur)'
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date de soumission'
    )
    validated_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Date de validation'
    )

    class Meta:
        verbose_name = 'Rapport journalier'
        verbose_name_plural = 'Rapports journaliers'
        ordering = ['-date_resume', '-created_at']
        unique_together = ['author', 'budget_sheet', 'date_resume']

    def __str__(self):
        return f"{self.title} - {self.date_resume} ({self.author})"

    def submit(self):
        """Soumet le rapport au supérieur hiérarchique"""
        from django.utils import timezone
        
        if self.status == 'draft':
            # Trouver le supérieur hiérarchique
            try:
                hierarchie = Hierarchie.objects.get(
                    user=self.author,
                    budget_sheet=self.budget_sheet
                )
                self.destinataire = hierarchie.superieur
            except Hierarchie.DoesNotExist:
                self.destinataire = None
            
            self.status = 'submitted'
            self.submitted_at = timezone.now()
            self.save()

    def validate(self):
        """Valide le rapport"""
        from django.utils import timezone
        
        if self.status == 'submitted':
            self.status = 'validated'
            self.validated_at = timezone.now()
            self.save()

    def reject(self):
        """Rejette le rapport"""
        if self.status == 'submitted':
            self.status = 'rejected'
            self.save()


class CommentResume(models.Model):
    """
    Commentaires sur un rapport (feedback du supérieur)
    """
    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Rapport'
    )
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='resume_comments',
        verbose_name='Auteur du commentaire'
    )
    content = models.TextField(verbose_name='Commentaire')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'
        ordering = ['created_at']

    def __str__(self):
        return f"Commentaire de {self.author} sur {self.resume.title}"
