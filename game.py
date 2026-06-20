# game.py
# Main game logic and state management

import random
import time
import pygame
from constants import (
    BUTTON_ORDER, BUTTON_COLORS, BUTTON_HIGHLIGHT,
    SEQUENCE_DELAY, BUTTON_FLASH_DURATION, LEVEL_UP_DELAY,
    GAME_OVER_DELAY, MAX_SEQUENCE_LENGTH,
    WINDOW_WIDTH, WINDOW_HEIGHT
)
from colors import ColorManager

class SimonGame:
    """Main game class managing state and logic"""
    
    def __init__(self):
        """Initialize the game"""
        self.sequence = []
        self.player_sequence = []
        self.current_step = 0
        self.score = 0
        self.high_score = 0
        self.is_game_over = False
        self.is_player_turn = False
        self.is_showing_sequence = False
        self.is_waiting = False
        self.last_flash_time = 0
        self.flash_index = 0
        self.flash_color = None
        
        # Load high score from file if it exists
        self.load_high_score()
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open('highscore.txt', 'r') as f:
                self.high_score = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            self.high_score = 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))
        except IOError:
            pass
    
    def start_new_game(self):
        """Start a new game"""
        self.sequence = []
        self.player_sequence = []
        self.current_step = 0
        self.score = 0
        self.is_game_over = False
        self.is_player_turn = False
        self.is_showing_sequence = False
        self.is_waiting = False
        self.flash_index = 0
        self.flash_color = None
        
        # Generate first sequence
        self.add_to_sequence()
        self.show_sequence()
    
    def add_to_sequence(self):
        """Add a random color to the sequence"""
        new_color = random.choice(BUTTON_ORDER)
        self.sequence.append(new_color)
        
        # Check if we've reached the maximum
        if len(self.sequence) > MAX_SEQUENCE_LENGTH:
            self.is_game_over = True
            self.is_player_turn = False
    
    def show_sequence(self):
        """Start showing the sequence to the player"""
        self.is_showing_sequence = True
        self.is_player_turn = False
        self.flash_index = 0
        self.last_flash_time = time.time()
        self.flash_color = self.sequence[0] if self.sequence else None
    
    def update_sequence_display(self):
        """Update the sequence display animation"""
        if not self.is_showing_sequence:
            return None
        
        current_time = time.time()
        
        # If we've shown all colors in sequence
        if self.flash_index >= len(self.sequence):
            self.is_showing_sequence = False
            self.is_player_turn = True
            self.player_sequence = []
            self.current_step = 0
            return None
        
        # Check if it's time to flash the next color
        if current_time - self.last_flash_time >= SEQUENCE_DELAY:
            # Turn off previous flash
            if self.flash_color is not None:
                self.flash_color = None
            
            # Flash next color in sequence
            if self.flash_index < len(self.sequence):
                self.flash_color = self.sequence[self.flash_index]
                self.last_flash_time = current_time
                self.flash_index += 1
                
                # Schedule next flash
                return {
                    'action': 'flash',
                    'color': self.flash_color,
                    'duration': BUTTON_FLASH_DURATION
                }
        
        # Keep current flash active
        if self.flash_color is not None:
            # Check if flash duration has elapsed
            if current_time - self.last_flash_time >= BUTTON_FLASH_DURATION:
                self.flash_color = None
                self.last_flash_time = current_time
        
        return None
    
    def handle_player_input(self, color_name):
        """Handle player clicking a color button"""
        if not self.is_player_turn or self.is_game_over:
            return False
        
        # Add player's input
        self.player_sequence.append(color_name)
        
        # Check if player input matches sequence
        expected_color = self.sequence[self.current_step]
        
        if color_name != expected_color:
            # Wrong color - game over
            self.end_game()
            return False
        
        # Correct input
        self.current_step += 1
        
        # Check if player completed the sequence
        if self.current_step == len(self.sequence):
            # Level complete
            self.score += 1
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            
            # Wait a moment then add to sequence
            self.is_player_turn = False
            self.is_waiting = True
            self.last_flash_time = time.time()
            
            return True
        
        return True
    
    def end_game(self):
        """End the current game"""
        self.is_game_over = True
        self.is_player_turn = False
        self.is_showing_sequence = False
        self.last_flash_time = time.time()
        
        # Update high score if needed
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
    
    def update(self):
        """Update game state"""
        # Handle waiting after level completion
        if self.is_waiting:
            current_time = time.time()
            if current_time - self.last_flash_time >= LEVEL_UP_DELAY:
                self.is_waiting = False
                self.add_to_sequence()
                self.show_sequence()
        
        # Update sequence display
        if self.is_showing_sequence:
            result = self.update_sequence_display()
            return result
        
        return None
    
    def get_button_state(self, color_name):
        """Get the state of a button (normal, highlighted, etc.)"""
        if self.is_showing_sequence and self.flash_color == color_name:
            return 'highlighted'
        return 'normal'
    
    def get_score(self):
        """Get current score"""
        return self.score
    
    def get_high_score(self):
        """Get high score"""
        return self.high_score
    
    def get_sequence_length(self):
        """Get current sequence length"""
        return len(self.sequence)
    
    def is_over(self):
        """Check if game is over"""
        return self.is_game_over
    
    def is_player_turn(self):
        """Check if it's player's turn"""
        return self.is_player_turn
