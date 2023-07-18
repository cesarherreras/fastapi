from pymongo import MongoClient

#Por defecto se conecta a localhost, no es necesario especificar la URL
db_client = MongoClient().local

#Mongo Atlas
#mongodb+srv://<user>:<password>
#db_client = MongoClient(mongo_url).database_name
