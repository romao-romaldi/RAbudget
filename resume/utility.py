import random
import string


def generpid(length=20):
    """
    Génère un identifiant unique aléatoire
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
