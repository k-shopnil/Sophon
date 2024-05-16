# import wikipedia

# wikipedia.set_lang("en")
# # print(wikipedia.search("Elon Musk"))
# print(wikipedia.summary("Mother", sentences=2))
# print(wikipedia.page("Elon Musk").content)

import requests

url ="https://www.wikidata.org/w/api.php"

#query=input("Enter the search query: ")

def wikiengine(query):
    try:
        params ={
        "action":"wbsearchentities",
        "format":"json",
        "language":"en",
        "search":query
        }
        
        data = requests.get(url,params=params)
        # print(data.json())
        #print(data.json()["search"][0]["description"])
        d=data.json()["search"][0]["description"]
        l=data.json()["search"][0]["label"]
        u= data.json()["search"][0]["url"]
        #print(f"Learn more about {l} at http:{u}" )
    except Exception as e:
        d="Sorry, I couldn't find anything like that. Please check for any typo/misspelling."
        l=""
        u=""
    
    return d,l,u

#wikiengine(query)

