import chromadb
chromadb_client = chromadb.Client()
#naming the collection to store the data in
collection_name = "test_collection"
#this will create a new collection if it doesn't exist, or retrieve the existing one if it does
collection = chromadb_client.get_or_create_collection(name=collection_name)

#define text documents
documents = [
    {"id": "1", "text": "Hello, World!"},
    {"id": "2", "text": "How are you doing today?"},
    {"id": "3", "text": "Goodbye! See you later."}
]

#add the documents to the collection. 
#we are using upsert here, which means that if a document with the same id already exists, it will be updated with the new text. Hence we not use .add method here, which would throw an error if a document with the same id already exists.   
for doc in documents:
    collection.upsert(ids=doc["id"], documents=doc["text"])

#define a query text
query= "Hello, world!"

results = collection.query(query_texts=[query], n_results=2) 

print(results)