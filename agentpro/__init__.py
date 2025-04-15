from .agent import AgentPro
from agentpro.tools import AresInternetTool, CodeEngine, YouTubeSearchTool, SlideGenerationTool, PlannerTool, NoteManager
from sentence_transformers import SentenceTransformer
import faiss

ares_tool = AresInternetTool()
code_tool = CodeEngine()
youtube_tool = YouTubeSearchTool()
slide_tool = SlideGenerationTool()
planner_tool = PlannerTool()

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  
note_store = []  
index = faiss.IndexFlatL2(embedding_model.get_sentence_embedding_dimension())
vector_db = NoteManager.FAISSVectorDB(index, note_store)
note_manager_tool = NoteManager(vector_db, embedding_model, youtube_tool)

__all__ = ['AgentPro', 'ares_tool', 'code_tool', 'youtube_tool', 'slide_tool', 'note_manager_tool', 'planner_tool']