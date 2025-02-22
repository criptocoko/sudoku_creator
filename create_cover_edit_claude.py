from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import math
from typing import Tuple, List

class BookCoverGenerator:
    def __init__(self, width: int = 1800, height: int = 2700):
        self.WIDTH = width
        self.HEIGHT = height
        self.GOLDEN_RATIO = 1.618
        
    def create_gradient(self, start_color: Tuple[int, int, int], 
                       end_color: Tuple[int, int, int], height: int) -> List[Tuple[int, int, int]]:
        """Create a smooth gradient between two colors"""
        gradient = []
        for i in range(height):
            ratio = i / height
            new_color = tuple(int(start + (end - start) * ratio)
                            for start, end in zip(start_color, end_color))
            gradient.append(new_color)
        return gradient

    def draw_grid(self, draw: ImageDraw, x: int, y: int, size: int, cells: int, 
                  line_width: int = 2, color: Tuple[int, int, int] = (0, 0, 0), 
                  fill_numbers: bool = False) -> None:
        """Draw a Sudoku grid with optional numbers"""
        cell_size = size // cells
        
        # Draw grid lines
        for i in range(cells):
            width = line_width * 2 if i % (int(math.sqrt(cells))) == 0 else line_width
            draw.line([(x, y + i*cell_size), (x + size, y + i*cell_size)], 
                     fill=color, width=width)
            draw.line([(x + i*cell_size, y), (x + i*cell_size, y + size)], 
                     fill=color, width=width)
        draw.line([(x, y + size), (x + size, y + size)], fill=color, width=2*width)  # Bottom edge
        draw.line([(x + size, y), (x + size, y + size)], fill=color, width=2*width)  # Right edge
        # Optional: Fill some numbers for visual interest
        if fill_numbers:
            number_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", int(cell_size * 0.6))
            sample_numbers = [(0, 0, "5"), (2, 1, "3"), (1, 2, "9"), 
                            (3, 3, "1"), (2, 4, "7")]
            for row, col, num in sample_numbers:
                num_x = x + col * cell_size + cell_size // 3
                num_y = y + row * cell_size + cell_size // 6
                draw.text((num_x, num_y), num, fill=color, font=number_font)

    def create_front_cover(self) -> Image:
        """Generate the front cover design"""
        cover = Image.new("RGB", (self.WIDTH, self.HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(cover)
        
        # Create sophisticated gradient background
        gradient = self.create_gradient((240, 244, 255), (220, 230, 255), self.HEIGHT)
        for y, color in enumerate(gradient):
            draw.line([(0, y), (self.WIDTH, y)], fill=color)
            
        # Add subtle pattern overlay
        pattern_size = 20
        for x in range(0, self.WIDTH, pattern_size):
            for y in range(0, self.HEIGHT, pattern_size):
                if (x + y) % 40 == 0:
                    draw.rectangle([(x, y), (x+2, y+2)], fill=(200, 210, 255))
        
        # Title with enhanced typography
        title_font = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 310)
        subtitle_font = ImageFont.truetype("fonts/Montserrat-SemiBold.ttf", 75)
        
        draw.text((193, 113), "SUDOKU", fill=(0, 0, 64, 100), font=title_font)
        draw.text((190, 110), "SUDOKU", fill=(0, 0, 128), font=title_font)
        
        # Subtitle with accent color
        draw.text((454, 480), "MASTERMIND EDITION", fill=(70, 90, 180), font=subtitle_font)
        
        # Feature text with custom styling
        feature_font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 50)
        # Main decorative grid
        self.draw_grid(draw, 200, 850, 1400, 16, line_width=2, 
                      color=(0, 0, 90), fill_numbers=True)
        
        # Smaller accent grids
        self.draw_grid(draw, 200, 500, 200, 9, line_width=1, color=(70, 90, 180))
        self.draw_grid(draw, 1400, 500, 200, 9, line_width=1, color=(70, 90, 180))
        feature1 = "120 CHALLENGING PUZZLES"
        feature2 = "5 DIFFICULTY LEVELS"
        draw.text((570, 580), feature1, fill=(100, 100, 130), font=feature_font)
        draw.text((652, 630), feature2, fill=(100, 100, 130), font=feature_font)
        self.draw_grid(draw, 200, 2400, 200, 9, line_width=1, color=(70, 90, 180))
        self.draw_grid(draw, 1400, 2400, 200, 9, line_width=1, color=(70, 90, 180))
        feature_font = ImageFont.truetype("fonts/Montserrat-SemiBold.ttf", 70)
        feature3 = "WITH SOLUTIONS"
        feature4 = "COMES WITH 5 EXTRA 16x16 PUZZLES"
        draw.text((618, 2400), feature3, fill=(70, 90, 180), font=feature_font)
        feature_font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 50)

        draw.text((457, 2500), feature4, fill=(100, 100, 130), font=feature_font)

        

        return cover

def main():
    generator = BookCoverGenerator()
    front_cover = generator.create_front_cover()
    
    front_cover.save("book/covers/sudoku_front_cover.png", "PNG", quality=95)
    
if __name__ == "__main__":
    main()