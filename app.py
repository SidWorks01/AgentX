import gradio as gr
from agentpro import AgentPro, ares_tool, code_tool, youtube_tool ,slide_tool, note_manager_tool, planner_tool 

def gradio_interface(user_input):
    """
    Interface layer calling the core agent logic.
    """
    agent = AgentPro(tools=[ares_tool, code_tool, youtube_tool, slide_tool,note_manager_tool, planner_tool])
    output = agent(user_input)
    return output

demo = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(lines=3, placeholder="Type your input here..."),
    outputs="text",
    title="Traversaal-x AI Hackathon",
    description="A Gradio demo for our optimized agent pipeline.",
)

if __name__ == "__main__":
    demo.launch()
