import pymongo

mClient = None
db = None
guilds = None

#perPage = 

def init():
    global mClient
    global guilds
    global db

    mClient = pymongo.MongoClient("mongodb://localhost:27017/")
    
    db = mClient["bedibot"]

    guilds = db["guilds"]

def insertQuote(guildId: int, quote: str, quotedPerson: str):
    doc = {
        'quote': quote,
        'name': quotedPerson
    }
    coll = db["a" + str(guildId) + ".quotes"]
    try:
        coll.insert_one(doc)
        return True
    except:
        return False

def deleteQuote(guildId, quote, quotedPerson):
    coll = db["a"+guildId + ".quotes"]
    coll.delete_one({"quote": quote, "name": quotedPerson})
    
def findQuotes(guildId, quotedPerson, page):
   quotes = []

   coll = db["a"+guildId+".quotes"]
   count = 0
   for x in coll.find({"name": quotedPerson}):
        quotes.append("'" + x["quote"] + "' -" + x["name"])
        count += 1
        if count >= amount:
           break 

   return quotes





#init()
#insertQuote("758817188710449183","this is a quote4","Aadi")
#nsertQuote("758817188710449183","this is a quote1","Aadi")
#insertQuote("758817188710449183","this is a quote2","Aadi")
#insertQuote("758817188710449183","this is a quote3","Aadi")
#deleteQuote("758817188710449183","this is a quote3","Aadi")

#quotes = findQuotes("758817188710449183","Aadi",4)
#for quote in quotes:
 #   print(quote)