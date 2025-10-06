


class MapperTypeActivity:
    """
        cette class à pour role de mapper touts les champs d'un type d'activité
        elle permet de retourner un dictionnaire avec comme clé le nom du champ

        init:
            type_activity: instance de TypeActivity -> Model
            champs : le nom du champs à mapper du type foreignKey ou manyToManyField -> string

    """

    def __init__(self, type_activity, data_check:dict,champs="champs"):
        self.type_activity = type_activity
        self.champs = champs
        self.data_check = data_check
        self.liste_champs = {}

    def mapper_(self):
        """
            retourne un dictionnaire avec comme clé le nom du champ
        """
        if self.champs:
            champs = self.type_activity.champs.all()

            dict_champs = {}
            for champ in champs:
                self.liste_champs[champ.name] = {"name": champ.name,
                                                 "type_champs": champ.type_champs,"required": champ.required}

    def verification_champs_(self, item:tuple):
        """
            cette méthode permet de vérifier si les champs envoyés dans data
            correspondent aux champs du type d'activité
            data: dictionnaire avec comme clé le nom du champ
            retourne True si les champs correspondent, False sinon

            data :
                - clé : nom du champ
                - valeur : valeur du champ
        """
        if item[0] in self.liste_champs.keys():
            champ_info = self.liste_champs.get(item[0], None)
            if champ_info:
                required =self.ckeked_require_champs_(champ_info["required"], item[1])

                return required
            else:
                return {"status": False, "message": "Le champ n'existe pas dans le type d'activité."}

        return {"status": False, "message": "Le champ n'existe pas dans le type d'activité."}

    def checked_required_champs_(self, champs, item):
        if champs and item:
            return {"status": True, "message": "Le champ est requis et la valeur est fournie."}
        elif not champs:
            return {"status": True, "message": "Le champ n'est pas requis."}

        return {"status": False, "message": "Le champ est requis mais la valeur est manquante."}

    def checked_type_champs_(self, champs, item):
        pass


    def checked_champs(self):
        for data in self.data_check.items():
            item = self.verification_champs_(data)









