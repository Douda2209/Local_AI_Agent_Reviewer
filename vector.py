# we implement the logic that embedding the documents and storing them in a vector database

# vector search is a database, locally hosted using ChromaDB
# allows to quickly retrieve/lookup informations based on similarity search and the model can use it
# in our case we take the csv file with pizza restaurant reviews, embed them and store them in the vector db

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

#load the csv file with pandas
reviews = pd.read_csv("realistic_restaurant_reviews.csv")

#initialize the embeddings model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# store the embedded reviews in ChromaDB
db_location = "./reviews_embed_db"

#check if the database folder already exists
add_new_embedd_db = not os.path.exists(db_location)

if add_new_embedd_db:
    #create a list of Document objects from the reviews
    docs = []
    ids = []

    # parse the rows and add them to the docs list
    for i,row in reviews.iterrows():
        document = Document(page_content=row["Title"]+""+row["Review"], #combine the title with the review text
                            metadata = {"rating":row["Rating"], "date": row["Date"]},
                            id=str(i)) #set the id as the row index
    
        ids.append(str(i))
        docs.append(document)
    
# create the Chroma vector database and add the documents

vector_store = Chroma(collection_name="pizza_reviews",
                      persist_directory=db_location,
                      embedding_function=embeddings)

if add_new_embedd_db:
    vector_store.add_documents(docs, ids=ids)
    
# make the vector store be usable by the model: allows to lookup documents

retriever = vector_store.as_retriever(search_kwargs={"k":5}) #get top 5 similar reviews
         


