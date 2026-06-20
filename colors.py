# colors.py
# Color utilities and theme management

from constants import COLORS, BUTTON_ORDER

class ColorManager:
    """Manages color themes and conversions"""
    
    @staticmethod
    def rgb_to_hex(rgb):
        """Convert RGB tuple to hex color string"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
    
    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert hex color string to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    @staticmethod
    def get_color_scheme():
        """Return a dictionary of color names to RGB values"""
        return {name: value for name, value in COLORS.items()}
    
    @staticmethod
    def get_button_colors():
        """Return colors for all game buttons"""
        from constants import BUTTON_COLORS
        return BUTTON_COLORS
    
    @staticmethod
    def get_highlight_colors():
        """Return highlight colors for all game buttons"""
        from constants import BUTTON_HIGHLIGHT
        return BUTTON_HIGHLIGHT
    
    @staticmethod
    def get_color_name(rgb):
        """Find the name of a color by its RGB value"""
        for name, value in COLORS.items():
            if value == rgb:
                return name
        return None
    
    @staticmethod
    def blend_colors(color1, color2, ratio=0.5):
        """Blend two colors together"""
        return tuple(
            int(c1 * (1 - ratio) + c2 * ratio)
            for c1, c2 in zip(color1, color2)
        )
    
    @staticmethod
    def is_dark_color(rgb):
        """Determine if a color is dark (for text contrast)"""
        brightness = sum(rgb) / 3
        return brightness < 128
    
    @staticmethod
    def get_contrast_color(rgb):
        """Return white or black for contrast with given color"""
        return COLORS['WHITE'] if ColorManager.is_dark_color(rgb) else COLORS['BLACK']
