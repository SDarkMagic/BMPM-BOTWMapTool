class Actor:
    def __init__(self, actorData: dict) -> None:
        self.params = actorData['!Parameters'] if actorData['!Parameters'] != None else {}
        self.name = actorData['UnitConfigName']
        self.hash_id = actorData['HashId']
        self.links = actorData['LinksToObj'] if actorData['LinksToObj'] != None else []
        self.raw = actorData

    def replace_parameter(self, parameter_name, new_value):
        self.params.update({parameter_name: new_value})
        return

    def update(self):
        self.raw.update({'!Parameters': self.params})
        self.raw['UnitConfigName'] = self.name
        if len(self.links) > 0:
            self.raw['LinksToObj'] = self.links
        return