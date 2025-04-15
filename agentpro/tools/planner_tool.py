from agentpro.tools.base import Tool
from agentpro import AgentPro, ares_tool, code_tool, youtube_tool, slide_tool

sub_agent = AgentPro(tools=[ares_tool, code_tool, youtube_tool, slide_tool])

class PlannerTool(Tool):
    name: str = "teacher_agent_tool"
    description: str = (
        "Acts as a teacher assistant: recommends YouTube videos, summarizes content, "
        "plans learning paths, and helps make study notes for any topic."
    )
    arg: str = "Instruction like 'plan deep learning', 'recommend videos on transformers', or 'summarize a topic'."


    def run(self, prompt: str) -> str:
        intent, _, topic = prompt.partition(" ")
        intent = intent.strip().lower()
        topic = topic.strip()

        if not topic:
            return "Please provide a topic along with the instruction."

        if intent in ["plan", "learning", "learn"]:
            return self.plan_learning(topic)
        elif intent in ["recommend", "video", "videos"]:
            return self.recommend_videos(topic)
        elif intent in ["summarize", "notes", "note"]:
            return self.summarize_and_note(topic)
        else:
            return "I didn't understand that. Try: 'plan deep learning', 'recommend videos on transformers', or 'summarize quantum mechanics'."

    def plan_learning(self, topic: str) -> str:
        # Use `ares_tool` via sub_agent to decompose topic
        prompt = f"Break down the topic '{topic}' into a step-by-step learning plan with subtopics."
        return sub_agent(prompt)

    def recommend_videos(self, topic: str) -> str:
        # Use `youtube_tool`
        prompt = f"Find top YouTube videos to learn about {topic} effectively."
        return sub_agent(prompt)

    def summarize_and_note(self, topic: str) -> str:
        # Use `ares_tool` + `slide_tool` to fetch content and make notes
        prompt = f"Search and summarize key points from online resources and make concise notes on {topic}."
        return sub_agent(prompt)
