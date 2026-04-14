import chromadb
from chromadb.utils import embedding_functions

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="deepsearch_memory"
        )

    def add(self, query, answer):
        self.collection.add(
            documents=[answer],
            metadatas=[{"query": query}],
            ids=[str(hash(query))]
        )

    def search(self, query, n_results=2):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        return results.get("documents", [])