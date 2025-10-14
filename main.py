"""
Autonomous Lunar Exploration System
Multi-Agent Coordination for Extreme Environments

Market Applications:
- Mining automation (underground, deep sea, asteroid) - $10B+ TAM
- Disaster response robotics (search & rescue) - $5B+ TAM  
- Military/defense autonomous systems - $15B+ TAM
- Infrastructure inspection - $8B+ TAM
- Agricultural robotics - $12B+ TAM
TOTAL TAM: $50B+ across autonomous multi-robot systems
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.environment import LunarEnvironment
from core.message_bus import MessageBus
from core.coordinator import MissionCoordinator
from agents.scout import ScoutAgent
from agents.analyst import AnalystAgent
from agents.executor import ExecutorAgent
from visualization.display import MissionVisualizer

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║       🌙 AUTONOMOUS LUNAR EXPLORATION SYSTEM 🚀           ║
    ║                                                           ║
    ║   Multi-Agent Coordination for Extreme Environments      ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Demo: Coordinated robots exploring lunar surface
    Market: $50B+ TAM across autonomous robotics sectors
    
    Technology Demonstration:
    ✓ Autonomous decision-making without human input
    ✓ Multi-agent coordination via message passing
    ✓ Intelligent task allocation and prioritization
    ✓ Dynamic route planning with obstacle avoidance
    ✓ Real-time adaptation to discoveries
    
    """)
    
    # Initialize environment
    print("🌑 Initializing lunar environment...")
    environment = LunarEnvironment(width=100, height=100, num_targets=20)
    
    # Initialize communication infrastructure
    print("📡 Setting up agent communication network...")
    message_bus = MessageBus()
    
    # Deploy autonomous agents
    print("🤖 Deploying autonomous agents...")
    scout = ScoutAgent("Scout-1", environment, message_bus, start_x=20, start_y=20)
    analyst = AnalystAgent("Analyst", environment, message_bus)
    executor = ExecutorAgent("Executor-1", environment, message_bus, start_x=50, start_y=50)
    
    agents = [scout, analyst, executor]
    
    # Initialize mission coordinator
    coordinator = MissionCoordinator(environment, message_bus, agents)
    
    # Run autonomous mission
    coordinator.run_mission(max_cycles=40)
    
    # Generate visualization
    print("\n📊 Generating mission visualization...")
    visualizer = MissionVisualizer(environment, agents)
    fig = visualizer.create_static_visualization()
    visualizer.save('lunar_mission_result.png')
    
    # Show visualization
    print("\n🖼️  Opening visualization window...")
    visualizer.show()
    
    print("\n✨ Mission Complete! ✨\n")

if __name__ == "__main__":
    main()
