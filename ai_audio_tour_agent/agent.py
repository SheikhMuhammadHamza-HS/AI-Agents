"""AI Agent definitions using Google Gemini"""
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.googlesearch import GoogleSearch
from config import config
from printer import printer

def create_planner_agent() -> Agent:
    """Create the planner agent that allocates time for different interests"""
    printer.print_info("Creating Planner Agent...")
    
    return Agent(
        name="Tour Planner",
        model=Gemini(id="gemini-2.5-flash", api_key=config.get_gemini_api_key()),
        description="Plans the tour structure and time allocation based on user interests",
        instructions=[
            "You are a tour planning expert.",
            "Analyze the user's interests and tour duration.",
            "Create a time allocation plan for each selected interest area.",
            "Ensure the total time matches the requested duration.",
            "Provide a clear breakdown of how much time to spend on each topic.",
            "Consider the importance and depth of each interest area."
        ],
        markdown=True,
    )

def create_architecture_agent() -> Agent:
    """Create the architecture specialist agent"""
    printer.print_info("Creating Architecture Agent...")
    
    return Agent(
        name="Architecture Specialist",
        model=Gemini(id="gemini-2.5-flash", api_key=config.get_gemini_api_key()),
        tools=[GoogleSearch()],
        description="Expert in architectural history, styles, and building design",
        instructions=[
            "You are an architecture expert and historian.",
            "Research and provide detailed information about architectural landmarks.",
            "Explain architectural styles, techniques, and historical context.",
            "Use web search to find accurate and current information.",
            "Focus on interesting facts, design elements, and cultural significance.",
            "Make the content engaging and accessible to general audiences."
        ],
        markdown=True,
        show_tool_calls=True,
    )

def create_history_agent() -> Agent:
    """Create the history specialist agent"""
    printer.print_info("Creating History Agent...")
    
    return Agent(
        name="History Specialist",
        model=Gemini(id="gemini-2.5-flash", api_key=config.get_gemini_api_key()),
        tools=[GoogleSearch()],
        description="Expert in historical events, figures, and cultural heritage",
        instructions=[
            "You are a history expert and storyteller.",
            "Research and provide fascinating historical information about locations.",
            "Include important events, historical figures, and cultural context.",
            "Use web search to ensure accuracy and find interesting details.",
            "Tell engaging stories that bring history to life.",
            "Connect historical events to their broader significance."
        ],
        markdown=True,
        show_tool_calls=True,
    )

def create_culinary_agent() -> Agent:
    """Create the culinary specialist agent"""
    printer.print_info("Creating Culinary Agent...")
    
    return Agent(
        name="Culinary Specialist",
        model=Gemini(id="gemini-2.5-flash", api_key=config.get_gemini_api_key()),
        tools=[GoogleSearch()],
        description="Expert in local cuisine, food culture, and culinary traditions",
        instructions=[
            "You are a culinary expert and food culture specialist.",
            "Research and describe local cuisine, traditional dishes, and food culture.",
            "Include information about famous restaurants, markets, and food experiences.",
            "Use web search to find current and authentic culinary information.",
            "Explain the cultural significance of local food traditions.",
            "Make recommendations for must-try dishes and dining experiences."
        ],
        markdown=True,
        show_tool_calls=True,
    )

def create_culture_agent() -> Agent:
    """Create the culture specialist agent"""
    printer.print_info("Creating Culture Agent...")
    
    return Agent(
        name="Culture Specialist",
        model=Gemini(id="gemini-2.5-flash", api_key=config.get_gemini_api_key()),
        tools=[GoogleSearch()],
        description="Expert in local culture, traditions, arts, and social customs",
        instructions=[
            "You are a cultural anthropologist and local culture expert.",
            "Research and explain local customs, traditions, and cultural practices.",
            "Include information about arts, music, festivals, and social norms.",
            "Use web search to find authentic and current cultural information.",
            "Highlight unique cultural aspects that make the location special.",
            "Help visitors understand and respect local culture."
        ],
        markdown=True,
        show_tool_calls=True,
    )

def create_orchestrator_agent() -> Agent:
    """Create the orchestrator agent that combines all content into a cohesive tour"""
    printer.print_info("Creating Orchestrator Agent...")
    
    return Agent(
        name="Tour Orchestrator",
        model=Gemini(id="gemini-2.5-flash", api_key=config.get_gemini_api_key()),
        description="Combines all research into a cohesive, engaging audio tour narrative",
        instructions=[
            "You are a professional tour guide and storyteller.",
            "Combine all the specialist content into a single, flowing narrative.",
            "Create an engaging audio tour script that sounds natural when spoken.",
            "Use a warm, friendly, and enthusiastic tone.",
            "Include smooth transitions between different topics.",
            "Start with a welcoming introduction and end with a memorable conclusion.",
            "Make the tour feel like a conversation with a knowledgeable friend.",
            "Ensure the content flows logically and maintains listener engagement.",
            "Use vivid descriptions that help listeners visualize the location.",
            "The final tour should be ready to be read aloud as an audio guide."
        ],
        markdown=True,
    )

def get_all_agents() -> dict:
    """Get all available specialist agents"""
    return {
        "Architecture": create_architecture_agent,
        "History": create_history_agent,
        "Culinary": create_culinary_agent,
        "Culture": create_culture_agent,
    }
