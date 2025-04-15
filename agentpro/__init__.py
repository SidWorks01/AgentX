from .agent import AgentPro
from agentpro.tools import AresInternetTool, CodeEngine, YouTubeSearchTool, SlideGenerationTool, PlannerTool, NoteManager
from sentence_transformers import SentenceTransformer
import faiss
import os

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
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
note_store = []
faiss_index = faiss.IndexFlatIP(embedding_model.get_sentence_embedding_dimension())
vector_db = FAISSVectorDB(faiss_index, note_store)

youtube_tool_instance = YouTubeSearchTool()

common_tools = [
    AresInternetTool(),
    CodeEngine(),
    youtube_tool_instance,
    SlideGenerationTool()
]

# Optional tools
tools = common_tools.copy()

if os.environ.get("TRAVERSAAL_ARES_API_KEY"):
    note_manager_tool = NoteManager(
        vector_db=vector_db,
        embedding_model=embedding_model,
        youtube_tool=youtube_tool_instance,
        ares_tool=common_tools[0]  # AresInternetTool
    )
    tools.append(note_manager_tool)

# Create a sub-agent with all common tools (for planner)
sub_agent = AgentPro(tools=common_tools)

# Add the PlannerTool with the sub-agent injected
planner_tool = PlannerTool(sub_agent=sub_agent)
tools.append(planner_tool)

__all__ = ['AgentPro', 'ares_tool', 'code_tool', 'youtube_tool', 'slide_tool', 'note_manager_tool', 'planner_tool']