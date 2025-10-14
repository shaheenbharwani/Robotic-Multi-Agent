"""
Analyst Agent
Evaluates discovered targets and prioritizes collection
Uses multi-criteria scoring to determine target value
"""

class AnalystAgent:
    def __init__(self, name, environment, message_bus):
        self.name = name
        self.environment = environment
        self.message_bus = message_bus
        self.pending_evaluations = []
        self.evaluated_targets = []
        
    def process_messages(self):
        """Process incoming target discoveries"""
        messages = self.message_bus.get_messages(self.name)
        for msg in messages:
            if msg.msg_type == "TARGET_DISCOVERED":
                self.pending_evaluations.append(msg.content)
    
    def take_action(self):
        """Evaluate pending targets and send recommendations"""
        if not self.pending_evaluations:
            return
        
        # Evaluate each pending target
        for target_data in self.pending_evaluations:
            score = self._evaluate_target(target_data)
            
            evaluation = {
                'target_id': target_data['target_id'],
                'location': target_data['location'],
                'score': score,
                'priority': 'HIGH' if score > 15 else 'MEDIUM' if score > 8 else 'LOW'
            }
            
            self.evaluated_targets.append(evaluation)
            
            print(f"  🧠 {self.name}: Evaluated Target #{target_data['target_id']} - "
                  f"Score: {score:.1f} - Priority: {evaluation['priority']}")
            
            # Send high-priority targets to Executor
            if evaluation['priority'] in ['HIGH', 'MEDIUM']:
                self.message_bus.send_message(
                    self.name,
                    "Executor-1",
                    "COLLECT_TARGET",
                    evaluation
                )
        
        # Clear pending evaluations
        self.pending_evaluations = []
    
    def _evaluate_target(self, target_data):
        """
        Multi-criteria scoring function
        Considers: size, composition rarity, type interest
        """
        score = 0
        
        # Size score (0-10)
        score += target_data['size']
        
        # Composition score (rarer materials = higher score)
        composition_scores = {
            'ice': 10,  # Most valuable - potential water
            'anorthosite': 7,  # Ancient crust material
            'basalt': 4,  # Common volcanic rock
            'regolith': 2  # Surface dust
        }
        score += composition_scores.get(target_data['composition'], 3)
        
        # Type score
        type_scores = {
            'anomaly': 8,  # Unknown - high scientific value
            'crater': 5,  # May reveal subsurface
            'rock': 3  # Standard sample
        }
        score += type_scores.get(target_data['type'], 3)
        
        # Distance penalty (closer is better)
        # Assuming executor starts around (50, 50)
        distance = ((target_data['location'][0] - 50)**2 + 
                   (target_data['location'][1] - 50)**2)**0.5
        distance_penalty = min(distance / 10, 5)
        score -= distance_penalty
        
        return max(score, 0)
