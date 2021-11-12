from pymongo import MongoClient
client = MongoClient('mongodb+srv://Desktop-IB:<ECb2PseFIlifY3jQ>@ror2-cluster.viquk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = client.admin
serverStatusResult=db.command("serverStatus")
print(serverStatusResult)