from agentpro import AgentPro
from agentpro.tools import AresInternetTool, CodeEngine, YouTubeSearchTool, SlideGenerationTool
import os
import dotenv

def main():
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
            SlideGenerationTool(client_details=client_details)
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
