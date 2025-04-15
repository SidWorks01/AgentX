from .agent import AgentPro
from typing import Any
from agentpro.tools import AresInternetTool, CodeEngine, YouTubeSearchTool, SlideGenerationTool, PlannerTool , NoteManager # add more tools when available
ares_tool = AresInternetTool()
code_tool = CodeEngine()
youtube_tool = YouTubeSearchTool()
slide_tool = SlideGenerationTool()
note_manager_tool=NoteManager()
planner_tool=PlannerTool()
__all__ = ['AgentPro', 'ares_tool', 'code_tool', 'youtube_tool', 'slide_tool','note_manager_tool','planner_tool'] # add more tools when available