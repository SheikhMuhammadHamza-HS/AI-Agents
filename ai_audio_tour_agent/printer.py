"""Console output utilities for AI Audio Tour Agent"""
from datetime import datetime
from typing import Optional

class Printer:
    """Utility class for formatted console output"""
    
    @staticmethod
    def print_header(text: str):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"  {text}")
        print("="*60 + "\n")
    
    @staticmethod
    def print_step(step_name: str, message: str):
        """Print a step message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {step_name}: {message}")
    
    @staticmethod
    def print_agent(agent_name: str, message: str):
        """Print an agent message"""
        print(f"\n🤖 {agent_name}:")
        print(f"   {message}\n")
    
    @staticmethod
    def print_error(error_message: str):
        """Print an error message"""
        print(f"\n❌ ERROR: {error_message}\n")
    
    @staticmethod
    def print_success(message: str):
        """Print a success message"""
        print(f"\n✅ SUCCESS: {message}\n")
    
    @staticmethod
    def print_info(message: str):
        """Print an info message"""
        print(f"\nℹ️  INFO: {message}\n")

# Global printer instance
printer = Printer()
