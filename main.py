# main.py
# Main entry point - Simon Says Color Sequence Game

import pygame
import sys
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE,
    BUTTON_ORDER, BUTTON_COLORS, BUTTON_HIGHLIGHT,
    BUTTON_RADIUS, BUTTON_SPACING, FONT_SIZE,
    SMALL_FONT_SIZE, GAME_TITLE, COLORS,
    GAME_OVER_DELAY
)
from game import SimonGame
from colors import ColorManager

class SimonGameUI:
    """UI class for rendering the Simon Says game"""
    
    def __init__(self):
        """Initialize Pygame and UI components"""
        pygame.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.game = SimonGame()
        
        # Fonts
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)
        
        # Calculate button positions (square layout)
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        offset = BUTTON_RADIUS + BUTTON_SPACING // 2
        
        self.button_positions = {
            'RED': (center_x - offset, center_y - offset),
            'GREEN': (center_x + offset, center_y - offset),
            'BLUE': (center_x - offset, center_y + offset),
            'YELLOW': (center_x + offset, center_y + offset)
        }
        
        # Game over flag
        self.game_over_timer = 0
        
        # Start game
        self.game.start_new_game()
    
    def draw_button(self, color_name, position, state='normal'):
        """Draw a single button"""
        x, y = position
        
        # Select color based on state
        if state == 'highlighted':
            color = BUTTON_HIGHLIGHT[color_name]
        else:
            color = BUTTON_COLORS[color_name]
        
        # Draw button circle
        pygame.draw.circle(self.screen, color, (x, y), BUTTON_RADIUS)
        
        # Draw border
        border_color = COLORS['WHITE'] if state == 'highlighted' else COLORS['DARK_GRAY']
        pygame.draw.circle(self.screen, border_color, (x, y), BUTTON_RADIUS, 3)
        
        # Add shadow effect
        shadow_offset = 2
        pygame.draw.circle(
            self.screen, 
            COLORS['DARK_GRAY'], 
            (x + shadow_offset, y + shadow_offset), 
            BUTTON_RADIUS, 
            1
        )
        
        # Label the button
        color_name_display = color_name[0]  # First letter only
        text = self.font.render(color_name_display, True, COLORS['WHITE'])
        text_rect = text.get_rect(center=(x, y))
        self.screen.blit(text, text_rect)
    
    def draw_scoreboard(self):
        """Draw the score and high score"""
        # Score
        score_text = self.small_font.render(
            f"Score: {self.game.get_score()}", 
            True, 
            COLORS['WHITE']
        )
        score_rect = score_text.get_rect(
            center=(WINDOW_WIDTH // 2 - 100, 50)
        )
        self.screen.blit(score_text, score_rect)
        
        # High Score
        high_score_text = self.small_font.render(
            f"High Score: {self.game.get_high_score()}", 
            True, 
            COLORS['GOLD'] if hasattr(COLORS, 'GOLD') else COLORS['YELLOW']
        )
        high_score_rect = high_score_text.get_rect(
            center=(WINDOW_WIDTH // 2 + 100, 50)
        )
        self.screen.blit(high_score_text, high_score_rect)
        
        # Level / Sequence length
        level_text = self.small_font.render(
            f"Level: {self.game.get_sequence_length()}", 
            True, 
            COLORS['LIGHT_GRAY']
        )
        level_rect = level_text.get_rect(
            center=(WINDOW_WIDTH // 2, 25)
        )
        self.screen.blit(level_text, level_rect)
    
    def draw_title(self):
        """Draw the game title"""
        title_text = self.font.render(GAME_TITLE, True, COLORS['WHITE'])
        title_rect = title_text.get_rect(
            center=(WINDOW_WIDTH // 2, 85)
        )
        self.screen.blit(title_text, title_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = self.font.render(
            "GAME OVER!", 
            True, 
            COLORS['RED']
        )
        text_rect = game_over_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60)
        )
        self.screen.blit(game_over_text, text_rect)
        
        # Score
        score_text = self.small_font.render(
            f"Final Score: {self.game.get_score()}", 
            True, 
            COLORS['WHITE']
        )
        score_rect = score_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        self.screen.blit(score_text, score_rect)
        
        # High Score
        high_score_text = self.small_font.render(
            f"High Score: {self.game.get_high_score()}", 
            True, 
            COLORS['YELLOW']
        )
        high_score_rect = high_score_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
        )
        self.screen.blit(high_score_text, high_score_rect)
        
        # Restart instructions
        restart_text = self.small_font.render(
            "Press SPACE to restart", 
            True, 
            COLORS['LIGHT_GRAY']
        )
        restart_rect = restart_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100)
        )
        self.screen.blit(restart_text, restart_rect)
    
    def draw_turn_indicator(self):
        """Draw turn indicator"""
        if self.game.is_player_turn and not self.game.is_over():
            text = self.small_font.render(
                "Your Turn!", 
                True, 
                COLORS['GREEN']
            )
        elif self.game.is_showing_sequence and not self.game.is_over():
            text = self.small_font.render(
                "Watch the sequence...", 
                True, 
                COLORS['YELLOW']
            )
        elif self.game.is_over():
            text = self.small_font.render(
                "Game Over!", 
                True, 
                COLORS['RED']
            )
        else:
            text = self.small_font.render(
                "Waiting...", 
                True, 
                COLORS['GRAY']
            )
        
        text_rect = text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30)
        )
        self.screen.blit(text, text_rect)
    
    def handle_click(self, position):
        """Handle mouse click on buttons"""
        if self.game.is_over():
            return
        
        if not self.game.is_player_turn:
            return
        
        # Check which button was clicked
        for color_name, pos in self.button_positions.items():
            x, y = pos
            # Calculate distance from click to button center
            distance = ((position[0] - x) ** 2 + (position[1] - y) ** 2) ** 0.5
            
            if distance <= BUTTON_RADIUS:
                self.game.handle_player_input(color_name)
                break
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game.is_over():
                            self.game.start_new_game()
                    elif event.key == pygame.K_r:
                        self.game.start_new_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # Update game state
            self.game.update()
            
            # Clear screen
            self.screen.fill(COLORS['BLACK'])
            
            # Draw background
            # Draw a subtle grid or pattern
            for i in range(0, WINDOW_WIDTH, 50):
                pygame.draw.line(
                    self.screen, 
                    COLORS['DARK_GRAY'], 
                    (i, 0), 
                    (i, WINDOW_HEIGHT), 
                    1
                )
            for i in range(0, WINDOW_HEIGHT, 50):
                pygame.draw.line(
                    self.screen, 
                    COLORS['DARK_GRAY'], 
                    (0, i), 
                    (WINDOW_WIDTH, i), 
                    1
                )
            
            # Draw title
            self.draw_title()
            
            # Draw scoreboard
            self.draw_scoreboard()
            
            # Draw buttons
            for color_name, position in self.button_positions.items():
                state = self.game.get_button_state(color_name)
                self.draw_button(color_name, position, state)
            
            # Draw turn indicator
            self.draw_turn_indicator()
            
            # Draw game over screen if needed
            if self.game.is_over():
                self.draw_game_over()
            
            # Update display
            pygame.display.flip()
            
            # Cap frame rate
            self.clock.tick(60)
        
        # Clean up
        pygame.quit()
        sys.exit()

def main():
    """Main entry point"""
    game_ui = SimonGameUI()
    game_ui.run()

if __name__ == "__main__":
    main()
