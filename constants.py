# constants.py
# Game constants and configuration

# Color definitions (RGB values)
COLORS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 0),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'DARK_GRAY': (64, 64, 64),
    'LIGHT_GRAY': (200, 200, 200),
}

# Button configurations
BUTTON_ORDER = ['RED', 'GREEN', 'BLUE', 'YELLOW']
BUTTON_COLORS = {
    'RED': COLORS['RED'],
    'GREEN': COLORS['GREEN'],
    'BLUE': COLORS['BLUE'],
    'YELLOW': COLORS['YELLOW']
}
BUTTON_HIGHLIGHT = {
    'RED': (255, 100, 100),
    'GREEN': (100, 255, 100),
    'BLUE': (100, 100, 255),
    'YELLOW': (255, 255, 100)
}

# Game settings
SEQUENCE_DELAY = 0.5  # Seconds between sequence flashes
BUTTON_FLASH_DURATION = 0.3  # Seconds button stays highlighted
LEVEL_UP_DELAY = 1.0  # Seconds before starting new sequence
GAME_OVER_DELAY = 2.0  # Seconds to show game over screen
MAX_SEQUENCE_LENGTH = 50  # Maximum sequence length

# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Simon Says - Color Sequence Game"

# UI settings
FONT_SIZE = 36
SMALL_FONT_SIZE = 24
BUTTON_RADIUS = 120
BUTTON_SPACING = 20
GAME_TITLE = "SIMON SAYS"
