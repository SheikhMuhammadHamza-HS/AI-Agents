"""Tour orchestration logic for AI Audio Tour Agent"""
from typing import List, Dict
from agent import (
    create_planner_agent,
    create_orchestrator_agent,
    get_all_agents
)
from printer import printer

class TourManager:
    """Manages the tour generation process"""
    
    def __init__(self):
        self.planner = None
        self.orchestrator = None
        self.specialists = {}
    
    def generate_tour(
        self,
        location: str,
        interests: List[str],
        duration: int
    ) -> str:
        """
        Generate a complete audio tour
        
        Args:
            location: The city, landmark, or location to tour
            interests: List of interest areas (Architecture, History, Culinary, Culture)
            duration: Tour duration in minutes
            
        Returns:
            Complete tour narrative as a string
        """
        try:
            printer.print_header(f"Generating Tour for {location}")
            
            # Step 1: Create planner and get time allocation
            printer.print_step("Step 1", "Planning tour structure...")
            self.planner = create_planner_agent()
            
            planning_prompt = f"""
            Create a time allocation plan for a {duration}-minute audio tour of {location}.
            
            The tour should cover these interests: {', '.join(interests)}
            
            Provide a clear breakdown of:
            1. How many minutes to allocate to each interest area
            2. The order in which topics should be presented
            3. Any special considerations for this location
            
            Make sure the total time adds up to exactly {duration} minutes.
            """
            
            planning_response = self.planner.run(planning_prompt)
            time_allocation = planning_response.content
            
            printer.print_agent("Planner", f"Created time allocation plan:\n{time_allocation}")
            
            # Step 2: Get specialist content for each interest
            printer.print_step("Step 2", "Gathering specialist content...")
            specialist_content = {}
            available_agents = get_all_agents()
            
            for interest in interests:
                if interest in available_agents:
                    printer.print_info(f"Researching {interest}...")
                    
                    # Create the specialist agent
                    agent = available_agents[interest]()
                    
                    # Create research prompt
                    research_prompt = f"""
                    Research and provide detailed, engaging content about {interest.lower()} 
                    aspects of {location}.
                    
                    This content will be part of a {duration}-minute audio tour.
                    Based on the time allocation plan, focus on the most interesting and 
                    important information.
                    
                    Time Allocation Plan:
                    {time_allocation}
                    
                    Provide rich, engaging content that would be interesting to hear in an 
                    audio tour. Include specific facts, stories, and details that bring 
                    the topic to life.
                    """
                    
                    response = agent.run(research_prompt)
                    specialist_content[interest] = response.content
                    
                    printer.print_agent(
                        f"{interest} Specialist",
                        f"Research complete ({len(response.content)} characters)"
                    )
            
            # Step 3: Orchestrate final tour
            printer.print_step("Step 3", "Creating final tour narrative...")
            self.orchestrator = create_orchestrator_agent()
            
            orchestration_prompt = f"""
            Create a complete, engaging audio tour script for {location}.
            
            Duration: {duration} minutes
            Interests covered: {', '.join(interests)}
            
            Time Allocation Plan:
            {time_allocation}
            
            Specialist Content:
            
            """
            
            for interest, content in specialist_content.items():
                orchestration_prompt += f"\n--- {interest} ---\n{content}\n"
            
            orchestration_prompt += f"""
            
            Your task:
            1. Combine all this content into a single, flowing audio tour narrative
            2. Create smooth transitions between topics
            3. Start with a warm welcome and introduction to {location}
            4. End with a memorable conclusion
            5. Make it sound natural and engaging when read aloud
            6. Ensure the pacing feels right for a {duration}-minute tour
            7. Use a conversational, friendly tone throughout
            
            The final output should be a complete script ready to be read as an audio tour.
            """
            
            final_response = self.orchestrator.run(orchestration_prompt)
            final_tour = final_response.content
            
            printer.print_success(f"Tour generated successfully! ({len(final_tour)} characters)")
            
            return final_tour
            
        except Exception as e:
            printer.print_error(f"Error generating tour: {str(e)}")
            raise

def create_tour_manager() -> TourManager:
    """Factory function to create a TourManager instance"""
    return TourManager()
