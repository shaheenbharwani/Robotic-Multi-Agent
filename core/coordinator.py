"""
Mission Coordinator
Orchestrates multi-agent lunar exploration mission
"""
import time

class MissionCoordinator:
    def __init__(self, environment, message_bus, agents):
        self.environment = environment
        self.message_bus = message_bus
        self.agents = agents
        self.mission_active = True
        self.mission_stats = {
            'targets_discovered': 0,
            'targets_collected': 0,
            'decisions_made': 0,
            'distance_traveled': 0
        }
        
    def run_mission(self, max_cycles=50):
        """Run the autonomous mission"""
        print("\n🚀 LUNAR EXPLORATION MISSION INITIATED 🌙")
        print("="*60)
        
        cycle = 0
        while self.mission_active and cycle < max_cycles:
            cycle += 1
            print(f"\n--- Cycle {cycle} ---")
            
            # Each agent processes messages and takes actions
            for agent in self.agents:
                agent.process_messages()
                agent.take_action()
                
            # Update mission statistics
            self._update_stats()
            
            # Check if mission objectives met
            if self._check_mission_complete():
                print("\n✅ MISSION OBJECTIVES ACHIEVED!")
                break
                
            time.sleep(0.1)  # Small delay for readability
        
        self._print_mission_summary()
    
    def _update_stats(self):
        """Update mission statistics"""
        self.mission_stats['targets_discovered'] = len(self.environment.discovered_targets)
        self.mission_stats['targets_collected'] = len(self.environment.collected_targets)
        
    def _check_mission_complete(self):
        """Check if mission objectives are complete"""
        # Mission complete if we've collected at least 10 valuable targets
        return len(self.environment.collected_targets) >= 10
    
    def _print_mission_summary(self):
        """Print final mission statistics"""
        print("\n" + "="*60)
        print("📊 MISSION SUMMARY")
        print("="*60)
        print(f"Targets Discovered: {self.mission_stats['targets_discovered']}")
        print(f"Targets Collected: {self.mission_stats['targets_collected']}")
        print(f"Decisions Made: {self.mission_stats['decisions_made']}")
        print("\n🎯 Mission Value:")
        
        # Calculate mission value based on collected targets
        total_value = 0
        for target_id in self.environment.collected_targets:
            target = self.environment.targets[target_id]
            value = target['size'] * {'basalt': 1, 'anorthosite': 2, 'regolith': 1, 'ice': 5}.get(target['composition'], 1)
            total_value += value
            print(f"  • {target['type'].title()} ({target['composition']}) - Value: {value:.1f}")
        
        print(f"\n💎 Total Mission Value: {total_value:.1f}")
        print("="*60)
