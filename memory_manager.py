import os

try:
    import chromadb
except ImportError:
    chromadb = None

class MemoryManager:
    def __init__(self):
        self.client = None
        self.collection = None
        if chromadb:
            try:
                # Use a local directory for persistence
                persist_directory = os.path.join(os.path.dirname(__file__), "chroma_db")
                self.client = chromadb.PersistentClient(path=persist_directory)
                self.collection = self.client.get_or_create_collection(name="ghost_memory")
            except Exception as e:
                print(f"Error initializing ChromaDB: {e}")

    def add_memory(self, text, metadata=None):
        if not self.collection:
            return False
        
        # Simple ID generation based on count
        try:
            count = self.collection.count()
            self.collection.add(
                documents=[text],
                metadatas=[metadata] if metadata else [{"source": "chat"}],
                ids=[f"mem_{count}"]
            )
            return True
        except Exception as e:
            print(f"Error adding memory: {e}")
            return False

    def query_memory(self, query, n_results=3):
        if not self.collection:
            return []
        
        try:
            if self.collection.count() == 0:
                return []
                
            results = self.collection.query(
                query_texts=[query],
                n_results=min(n_results, self.collection.count())
            )
            
            if results and results['documents'] and results['documents'][0]:
                return results['documents'][0]
            return []
        except Exception as e:
            print(f"Error querying memory: {e}")
            return []

memory_manager = MemoryManager()
