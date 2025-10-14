"""
Lunar Environment Simulator
Simulates lunar surface with rocks, craters, and obstacles
"""
import random
import numpy as np

class LunarEnvironment:
    def __init__(self, width=100, height=100, num_targets=20):
        self.width = width
        self.height = height
        self.targets = self._generate_targets(num_targets)
        self.obstacles = self._generate_obstacles(15)
        self.discovered_targets = []
        self.collected_targets = []
        
    def _generate_targets(self, num):
        """Generate interesting targets (rocks, craters) on lunar surface"""
        targets = []
        for i in range(num):
            target = {
                'id': i,
                'x': random.randint(10, self.width - 10),
                'y': random.randint(10, self.height - 10),
                'type': random.choice(['rock', 'crater', 'anomaly']),
                'size': random.uniform(1, 10),
                'composition': random.choice(['basalt', 'anorthosite', 'regolith', 'ice']),
                'discovered': False,
                'collected': False
            }
            targets.append(target)
        return targets
    
    def _generate_obstacles(self, num):
        """Generate obstacles that robots must avoid"""
        obstacles = []
        for _ in range(num):
            obstacles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'radius': random.uniform(3, 8)
            })
        return obstacles
    
    def discover_target(self, target_id):
        """Mark a target as discovered"""
        if target_id < len(self.targets):
            self.targets[target_id]['discovered'] = True
            if target_id not in self.discovered_targets:
                self.discovered_targets.append(target_id)
            return self.targets[target_id]
        return None
    
    def collect_target(self, target_id):
        """Mark a target as collected"""
        if target_id < len(self.targets):
            self.targets[target_id]['collected'] = True
            if target_id not in self.collected_targets:
                self.collected_targets.append(target_id)
            return True
        return False
    
    def is_obstacle_free(self, x, y):
        """Check if a position is free of obstacles"""
        for obs in self.obstacles:
            dist = np.sqrt((x - obs['x'])**2 + (y - obs['y'])**2)
            if dist < obs['radius']:
                return False
        return True
    
    def get_nearby_targets(self, x, y, radius):
        """Find all targets within radius of position"""
        nearby = []
        for target in self.targets:
            dist = np.sqrt((x - target['x'])**2 + (y - target['y'])**2)
            if dist <= radius:
                nearby.append(target)
        return nearby
