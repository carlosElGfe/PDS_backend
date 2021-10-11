from pymongo import MongoClient

def jugar(jugada):
    if jugada == "dudo":
        #logica del dudo
        pass
    elif jugada == "calzo":
        pass
    else:
        #logica prediccion   
        pass     
    return 0

def conection(collection_name):    
    client = MongoClient("mongodb+srv://new_user1:new_user123@cluster0.3rxb9.mongodb.net/cacho?retryWrites=true&w=majority")
    db = client[collection_name]
    print(db.collection_names())
    return db