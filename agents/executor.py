"""
Executor Agent
Plans optimal routes and executes sample collection
Uses greedy nearest-neighbor algorithm with obstacle avoidance
"""
import numpy as np

class ExecutorAgent:
    def __init__(self, name, environment, message_bus, start_x=50, start_y=50):
        self.name = name
        self.environment = environment
        self.message_bus = message_bus
        self.x = start_x
        self.y = start_y
        self.collection_queue = []
        self.current_target = None
        self.carrying_capacity = 15
        self.collected_count = 0
        
    def process_messages(self):
        """Process collection requests from Analyst"""
        messages = self.message_bus.get_messages(self.name)
        for msg in messages:
            if msg.msg_type == "COLLECT_TARGET":
                # Add to queue, sorted by priority
                target_info = msg.content
                # Insert based on score (higher score = higher priority)
                inserted = False
                for i, item in enumerate(self.collection_queue):
                    if target_info['score'] > item['score']:
                        self.collection_queue.insert(i, target_info)
                        inserted = True
                        break
                if not inserted:
                    self.collection_queue.append(target_info)
    
    def take_action(self):
        """Execute collection mission"""
        # If at capacity, skip collection
        if self.collected_count >= self.carrying_capacity:
            print(f"  🤖 {self.name}: At maximum carrying capacity ({self.carrying_capacity})")
            return
        
        # If no current target, select next from queue
        if not self.current_target and self.collection_queue:
            self.current_target = self.collection_queue.pop(0)
            target_id = self.current_target['target_id']
            target_loc = self.current_target['location']
            print(f"  🤖 {self.name}: New mission - Target #{target_id} at ({target_loc[0]:.1f}, {target_loc[1]:.1f})")
        
        # If we have a target, move towards it
        if self.current_target:
            target_loc = self.current_target['location']
            target_id = self.current_target['target_id']
            
            # Calculate distance to target
            distance = np.sqrt((self.x - target_loc[0])**2 + (self.y - target_loc[1])**2)
            
            # If close enough, collect target
            if distance < 3:
                success = self.environment.collect_target(target_id)
                if success:
                    self.collected_count += 1
                    print(f"  🤖 {self.name}: ✅ COLLECTED Target #{target_id} "
                          f"({self.collected_count}/{self.carrying_capacity})")
                    
                    # Notify mission coordinator
                    self.message_bus.broadcast(
                        self.name,
                        "TARGET_COLLECTED",
                        {'target_id': target_id, 'location': target_loc}
                    )
                
                self.current_target = None
            else:
                # Move towards target
                self._move_towards(target_loc[0], target_loc[1])
    
    def _move_towards(self, target_x, target_y):
        """Move towards target with obstacle avoidance"""
        # Calculate direction vector
        dx = target_x - self.x
        dy = target_y - self.y
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # Normalize and scale movement
            move_speed = min(5, distance)
            dx = (dx / distance) * move_speed
            dy = (dy / distance) * move_speed
            
            new_x = self.x + dx
            new_y = self.y + dy
            
            # Check for obstacles
            if self.environment.is_obstacle_free(new_x, new_y):
                self.x = new_x
                self.y = new_y
                print(f"  🤖 {self.name}: Moving to ({self.x:.1f}, {self.y:.1f}) "
                      f"[{distance:.1f}m from target]")
            else:
                # Try alternative paths if direct path is blocked
                alternatives = [
                    (self.x + dy/distance * move_speed, self.y - dx/distance * move_speed),  # Perpendicular
                    (self.x - dy/distance * move_speed, self.y + dx/distance * move_speed),  # Other perpendicular
                ]
                for alt_x, alt_y in alternatives:
                    if self.environment.is_obstacle_free(alt_x, alt_y):
                        self.x = alt_x
                        self.y = alt_y
                        print(f"  🤖 {self.name}: Avoiding obstacle, moving to ({self.x:.1f}, {self.y:.1f})")
                        break
