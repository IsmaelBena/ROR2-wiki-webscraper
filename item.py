class item():
    def __init__(self, name, rarity, category, imageUrl, unlock=''):
        self.name = name
        self.rarity = rarity
        self.category = category
        self.unlock = unlock
        self.imageUrl = imageUrl

    def getJson(self):
        return {
            'item_id': self.id,
            'name': self.name,
            'rarity': self.rarity,
            'category': self.category,
            'unlock': self.unlock
        }
