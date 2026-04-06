import chromadb
from chromadb.utils import embedding_functions

# Define the embedding function using the specific model
tamil_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

client = chromadb.PersistentClient(path="holywalls/chroma_db")

# Create collection with the specific embedding function
collection = client.get_or_create_collection(
    name="Lord_Murugan_hymn_collection", 
    embedding_function=tamil_ef
)
# read the text file and add it to the collection
velmaral = open("../holywalls/lord-muruga/velmaaral.txt", "r", encoding="utf-8").read()
velmaral = velmaral.replace("\n", " ")  # Replace newlines with spaces for better embedding
velmaral = velmaral.strip()  # Remove leading and trailing whitespace

# When you add text, ChromaDB calls the model for you
    
collection.add(
    documents=[velmaral],
    ids=["id1"]
)

results = collection.query(
    query_texts=["தனக்கும்நரர் தமக்கும் உறும் இடுக்கண்வினை சாடும்"], # "Love and God"
    n_results=1
)
print(results)