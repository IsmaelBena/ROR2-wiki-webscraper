from pymongo import MongoClient
client = MongoClient('')
db = client.admin
serverStatusResult=db.command("serverStatus")
print(serverStatusResult)
