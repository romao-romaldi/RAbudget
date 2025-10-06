from django.db import models

# Create your models here.

Type_champs = (
    ("charField", "Champ de type texte"),
    ("textField", "Champ de type texte long"),
    ("integerField", "Champ de type entier"),
    ("dateField", "Champ de type date"),
    ("booleanField", "Champ de type booléen"),
    ("emailField", "Champ de type email"),
    ("fileField", "Champ de type fichier"),
    ("imageField", "Champ de type image"),
    ("urlField", "Champ de type URL"),
    ("floatField", "Champ de type nombre à virgule flottante"),
    ("decimalField", "Champ de type nombre décimal"),
    ("timeField", "Champ de type heure"),
    ("dateTimeField", "Champ de type date et heure"),
    ("foreignKey", "Champ de type clé étrangère"),
    ("manyToManyField", "Champ de type plusieurs à plusieurs"),
    ("oneToOneField", "Champ de type un à un"),
)

### partie gestion de l'activité
class Champs(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    type_champs = models.CharField(choices=Type_champs, max_length=50, default=Type_champs[0][0])
    required = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TypeActivity(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    champs = models.ManyToManyField(Champs, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
