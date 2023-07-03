import pygame
import random
import gym
from gym import spaces
import numpy as np
from pygame.locals import *
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Define UI text style
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont(None, 30)


def get_closest_neighbors(boid, boids, num_neighbors):
    distances = [(other_boid, boid.position.distance_to(other_boid.position)) for other_boid in boids if other_boid != boid]
    distances.sort(key=lambda x: x[1])  # Sort by distance
    neighbors = [distance[0] for distance in distances[:num_neighbors]]
    return neighbors


class FlockingEnv(gym.Env):
    def __init__(self):
        super(FlockingEnv, self).__init__()

        # Define the action space and observation space
        self.action_space = spaces.Box(low=-1, high=1, shape=(2,))
        self.observation_space = spaces.Box(low=0, high=1, shape=(2,))

        # Initialize other variables here
        self.num_boids = 50
        self.boids = [Boid() for _ in range(self.num_boids)]
        self.collision_threshold = 5

    def reset(self):
        # Reset the environment
        self.boids = [Boid() for _ in range(self.num_boids)]
        # Initialize other variables if needed
        return self._get_observation()

    def step(self, action):
        # Perform a step in the environment based on the given action
        self._handle_events()
        self._update_boids(action)
        self._draw_screen()

        # Compute the reward
        reward = self._calculate_reward()
        done = False
        info = {}

        return self._get_observation(), reward, done, info

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def _update_boids(self, action):
        for boid in self.boids:
            boid.update(self.boids)

    def _draw_screen(self):
        screen.fill((0, 0, 0))
        for boid in self.boids:
            boid.draw()
        pygame.display.flip()

    def _get_observation(self):
        # Compute the average position of all boids
        average_position = pygame.Vector2(0, 0)
        for boid in self.boids:
            average_position += boid.position
        average_position /= len(self.boids)

        # Normalize the position
        normalized_position = np.array([average_position.x / width, average_position.y / height])

        return normalized_position

    def _calculate_reward(self):
        # Calculate the reward based on the boids' positions and behavior
        # Example implementation:
        cohesion_reward = self.calculate_cohesion_reward(self.boids[0], self.boids)
        separation_reward = self.calculate_separation_reward(self.boids[0], self.boids)
        return cohesion_reward + separation_reward

    @staticmethod
    def calculate_cohesion_reward(boid, boids):
        if len(boids) > 1:
            closest_neighbors = get_closest_neighbors(boid, boids, 6)
            center_of_mass = pygame.Vector2(0, 0)
            for neighbor in closest_neighbors:
                center_of_mass += neighbor.position
            center_of_mass /= len(closest_neighbors)
            distance_to_center = boid.position.distance_to(center_of_mass)
            if distance_to_center <= 50:  # Adjust the cohesion threshold as needed
                return 1
        return -1

    @staticmethod
    def calculate_separation_reward(boid, boids):
        separation_distance = 20  # Adjust as needed
        closest_neighbors = get_closest_neighbors(boid, boids, 6)
        for neighbor in closest_neighbors:
            distance = boid.position.distance_to(neighbor.position)
            if distance < separation_distance:
                return -1
        return 1


class Boid:
    def __init__(self):
        self.position = pygame.Vector2(random.randint(0, width), random.randint(0, height))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_velocity = 2

    def update(self, boids):
        neighbors = get_closest_neighbors(self, boids, 6)
        self.flock(neighbors)
        self.position += self.velocity
        self.check_boundaries()

    def flock(self, neighbors):
        alignment = self.align(neighbors)
        cohesion = self.cohere(neighbors)
        separation = self.separate(neighbors)

        self.velocity += alignment + cohesion + separation
        self.velocity.scale_to_length(self.max_velocity)

    def align(self, neighbors):
        if len(neighbors) > 0:
            average_velocity = pygame.Vector2(0, 0)
            for neighbor in neighbors:
                average_velocity += neighbor.velocity
            average_velocity /= len(neighbors)
            average_velocity.scale_to_length(self.max_velocity)
            alignment = average_velocity - self.velocity
            return alignment
        else:
            return pygame.Vector2(0, 0)

    def cohere(self, neighbors):
        if len(neighbors) > 0:
            center_of_mass = pygame.Vector2(0, 0)
            for neighbor in neighbors:
                center_of_mass += neighbor.position
            center_of_mass /= len(neighbors)
            cohesion = center_of_mass - self.position
            cohesion.scale_to_length(0.02)
            return cohesion
        else:
            return pygame.Vector2(0, 0)

    def separate(self, neighbors):
        separation_radius = 30
        separation_vector = pygame.Vector2(0, 0)
        for neighbor in neighbors:
            distance = self.position.distance_to(neighbor.position)
            if distance < separation_radius:
                separation_vector += self.position - neighbor.position
        if separation_vector.length() > 0:
            separation_vector.scale_to_length(0.1)
        return separation_vector

    def check_boundaries(self):
        if self.position.x < 0 or self.position.x > width:
            self.velocity.x *= -1
        if self.position.y < 0 or self.position.y > height:
            self.velocity.y *= -1

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.position.x), int(self.position.y)), 3)

    def render(self, mode='human'):
        pygame.display.update()


# Initialize the environment
env = FlockingEnv()

# Reset the environment
observation = env.reset()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()

    # Get action from the environment (random action for now)
    action = env.action_space.sample()

    # Step the environment
    observation, reward, done, info = env.step(action)

    # Render the environment (optional)
    # env.render()

    # Check if the episode is done
    if done:
        # Reset the environment
        observation = env.reset()

    # Limit the frame rate
    clock.tick(60)
