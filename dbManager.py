import pymongo

class dbManager():

    def __init__(self, data,credURL):
        self.data = data
        self.client = pymongo.MongoClient(credURL)
        print(self.client.list_database_names())
        self.allItemsDB = self.client['Items']
        print(self.allItemsDB.list_collection_names())
        print('Database manager created')
    
    def capNewCollection(self):
        itemCollection = self.allItemsDB['item']
        itemCollection.insert_many(self.data)
        print('Data added')

    def updateData(self):
        for entry in self.data:
            self.itemCollection.update_one( {"name" : entry['name']}, {"$set": entry}, upsert=True)
        print('All Data updated')