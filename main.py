from agentpro import AgentPro, ares_tool, youtube_tool
from agentpro.tools import AresInternetTool, CodeEngine, YouTubeSearchTool, SlideGenerationTool, NoteManager, PlannerTool
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import os
import dotenv

class FAISSVectorDB:
    def __init__(self, index, note_store):
        self.index = index
        self.note_store = note_store

    def similarity_search(self, query_embedding, k=5):
        query_vector = np.array(query_embedding).astype("float32").reshape(1, -1)
        scores, indices = self.index.search(query_vector, k)
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.note_store):
                results.append({
                    "text": self.note_store[idx]["text"],
                    "score": float(scores[0][i])
                })
        return results
    
def main():
    
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    note_store = []
    faiss_index = faiss.IndexFlatIP(embedding_model.get_sentence_embedding_dimension())
    vector_db = FAISSVectorDB(faiss_index, note_store)
    dotenv.load_dotenv()
 
    use_openrouter = os.getenv("OPENROUTER_API_KEY") is not None

    if use_openrouter:
        print('Using OpenRouter API')
        client_details = {
            "api_key": os.getenv("OPENROUTER_API_KEY"),
            "api_base": "https://openrouter.ai/api/v1",
            "MODEL": os.getenv("MODEL_NAME"),
            "api_type": "openrouter"
        }
    else:
        if not os.environ.get("OPENAI_API_KEY"):
            print("Error: OPENAI_API_KEY environment variable is not set.")
            print("Please set it before running the agent.")
            return
        
        client_details = {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "api_base": "https://api.openai.com/v1/",
            "MODEL": os.getenv("MODEL_NAME"),
            "api_type": "openai"
        }
        
    if not os.environ.get("TRAVERSAAL_ARES_API_KEY"):
        print("Warning: TRAVERSAAL_ARES_API_KEY environment variable is not set.")
        print("AresInternetTool will not be available.")
        tools = [CodeEngine(client_details), YouTubeSearchTool(client_details=client_details), SlideGenerationTool(client_details=client_details)]
    else:
        tools = [
            AresInternetTool(),
            CodeEngine(client_details), 
            YouTubeSearchTool(client_details), 
            SlideGenerationTool(client_details=client_details),
            NoteManager(vector_db=vector_db, embedding_model=embedding_model, youtube_tool=youtube_tool),
            PlannerTool()
        ]
    
    agent = AgentPro(tools=tools, client_details=client_details if use_openrouter else None)
    
    print("AgentPro is initialized and ready. Enter 'quit' to exit.")
    print("Available tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")
    
    while True:
        user_input = input("\nEnter your query: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            break
            
        try:
            response = agent(user_input)
            print(f"\nAgent Response:\n{response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting AgentPro...")
    main()
