"""
Scout Agent
Explores lunar surface and identifies potential targets
Uses intelligent exploration patterns to maximize coverage
"""
import numpy as np
import random

class ScoutAgent:
    def __init__(self, name, environment, message_bus, start_x=20, start_y=20):
        self.name = name
        self.environment = environment
        self.message_bus = message_bus
        self.x = start_x
        self.y = start_y
        self.sensor_range = 15
        self.visited_areas = set()
        self.exploration_phase = "sweep"
        
    def process_messages(self):
        """Process incoming messages from other agents"""
        messages = self.message_bus.get_messages(self.name)
        for msg in messages:
            if msg.msg_type == "REQUEST_EXPLORATION":
                print(f"  🔭 {self.name}: Received exploration request for area {msg.content}")
    
    def take_action(self):
        """Explore and identify targets"""
        # Mark current area as visited
        grid_cell = (int(self.x / 10), int(self.y / 10))
        self.visited_areas.add(grid_cell)
        
        # Scan for nearby targets
        nearby_targets = self.environment.get_nearby_targets(self.x, self.y, self.sensor_range)
        
        for target in nearby_targets:
            if not target['discovered']:
                # Discover new target
                self.environment.discover_target(target['id'])
                print(f"  🔭 {self.name}: DISCOVERED {target['type']} at ({target['x']:.1f}, {target['y']:.1f})")
                
                # Send discovery message to Analyst
                self.message_bus.send_message(
                    self.name, 
                    "Analyst", 
                    "TARGET_DISCOVERED",
                    {
                        'target_id': target['id'],
                        'location': (target['x'], target['y']),
                        'type': target['type'],
                        'size': target['size'],
                        'composition': target['composition']
                    }
                )
        
        # Move to next exploration position using intelligent pattern
        self._move_to_next_position()
    
    def _move_to_next_position(self):
        """Intelligent movement to unexplored areas"""
        # Find least visited neighboring cells
        possible_moves = []
        for dx, dy in [(10, 0), (-10, 0), (0, 10), (0, -10), (7, 7), (-7, 7), (7, -7), (-7, -7)]:
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Check bounds
            if 0 <= new_x < self.environment.width and 0 <= new_y < self.environment.height:
                # Check for obstacles
                if self.environment.is_obstacle_free(new_x, new_y):
                    grid_cell = (int(new_x / 10), int(new_y / 10))
                    # Prefer unvisited areas
                    priority = 0 if grid_cell not in self.visited_areas else 1
                    possible_moves.append((new_x, new_y, priority))
        
        if possible_moves:
            # Sort by priority (unvisited first) and add some randomness
            possible_moves.sort(key=lambda m: (m[2], random.random()))
            self.x, self.y, _ = possible_moves[0]
            print(f"  🔭 {self.name}: Moving to ({self.x:.1f}, {self.y:.1f})")
