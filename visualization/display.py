"""
Mission Visualization
Real-time display of lunar exploration mission
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np

class MissionVisualizer:
    def __init__(self, environment, agents):
        self.environment = environment
        self.agents = agents
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        
    def setup_plot(self):
        """Initialize the plot"""
        self.ax.set_xlim(0, self.environment.width)
        self.ax.set_ylim(0, self.environment.height)
        self.ax.set_aspect('equal')
        self.ax.set_facecolor('#1a1a2e')
        self.fig.patch.set_facecolor('#16213e')
        self.ax.set_title('🌙 AUTONOMOUS LUNAR EXPLORATION MISSION 🚀', 
                         fontsize=16, color='white', pad=20)
        self.ax.set_xlabel('Longitude (m)', fontsize=12, color='white')
        self.ax.set_ylabel('Latitude (m)', fontsize=12, color='white')
        self.ax.tick_params(colors='white')
        
    def draw_static_elements(self):
        """Draw obstacles and targets"""
        # Draw obstacles
        for obs in self.environment.obstacles:
            circle = patches.Circle((obs['x'], obs['y']), obs['radius'], 
                                   color='#6c5b7b', alpha=0.7, label='Obstacle')
            self.ax.add_patch(circle)
        
        # Draw all targets
        for target in self.environment.targets:
            if target['collected']:
                color = '#00ff41'  # Collected - bright green
                marker = 'o'
                size = 100
            elif target['discovered']:
                color = '#ffa500'  # Discovered - orange
                marker = '^'
                size = 80
            else:
                color = '#888888'  # Undiscovered - gray
                marker = 's'
                size = 40
            
            self.ax.scatter(target['x'], target['y'], c=color, marker=marker, 
                          s=size, alpha=0.8, edgecolors='white', linewidths=0.5)
    
    def draw_agents(self):
        """Draw agent positions"""
        agent_colors = {
            'Scout': '#00d4ff',     # Cyan
            'Analyst': '#ff00ff',   # Magenta
            'Executor': '#ffff00'   # Yellow
        }
        
        for agent in self.agents:
            # Only draw agents that have position (x, y)
            if not hasattr(agent, 'x') or not hasattr(agent, 'y'):
                continue
                
            # Get agent name and position
            agent_name = agent.name
            color = agent_colors.get(agent_name.split('-')[0], '#ffffff')
            
            # Draw agent
            self.ax.scatter(agent.x, agent.y, c=color, marker='*', 
                          s=400, edgecolors='white', linewidths=2, 
                          label=agent_name, zorder=10)
            
            # Draw sensor/action range
            if hasattr(agent, 'sensor_range'):
                circle = patches.Circle((agent.x, agent.y), agent.sensor_range,
                                      color=color, alpha=0.1, linestyle='--',
                                      fill=True)
                self.ax.add_patch(circle)
    
    def create_static_visualization(self):
        """Create a single frame visualization"""
        self.setup_plot()
        self.draw_static_elements()
        self.draw_agents()
        
        # Add legend
        handles, labels = self.ax.get_legend_handles_labels()
        # Remove duplicates
        by_label = dict(zip(labels, handles))
        self.ax.legend(by_label.values(), by_label.keys(), 
                      loc='upper right', facecolor='#16213e', 
                      edgecolor='white', fontsize=10)
        
        # Add mission stats
        stats_text = f"Discovered: {len(self.environment.discovered_targets)} | "
        stats_text += f"Collected: {len(self.environment.collected_targets)}"
        self.ax.text(0.02, 0.98, stats_text, transform=self.ax.transAxes,
                    fontsize=12, verticalalignment='top', color='white',
                    bbox=dict(boxstyle='round', facecolor='#16213e', alpha=0.8))
        
        plt.tight_layout()
        return self.fig
    
    def show(self):
        """Display the visualization"""
        plt.show()
    
    def save(self, filename='lunar_mission.png'):
        """Save the visualization"""
        plt.savefig(filename, dpi=300, facecolor='#16213e')
        print(f"\n📸 Visualization saved to {filename}")
