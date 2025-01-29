from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import math
from typing import Tuple, List

class BookCoverGenerator:
    def __init__(self, width: int = 1200, height: int = 1800):
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
        for i in range(cells + 1):
            width = line_width * 2 if i % (int(math.sqrt(cells))) == 0 else line_width
            draw.line([(x, y + i*cell_size), (x + size, y + i*cell_size)], 
                     fill=color, width=width)
            draw.line([(x + i*cell_size, y), (x + i*cell_size, y + size)], 
                     fill=color, width=width)
        
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
        title_font = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 120)
        subtitle_font = ImageFont.truetype("fonts/Montserrat-SemiBold.ttf", 36)
        
        # Add subtle shadow effect to title
        shadow_offset = 3
        draw.text((103, 103), "SUDOKU", fill=(0, 0, 64, 100), font=title_font)
        draw.text((100, 100), "SUDOKU", fill=(0, 0, 128), font=title_font)
        
        # Subtitle with accent color
        draw.text((100, 240), "MASTERMIND EDITION", fill=(70, 90, 180), font=subtitle_font)
        
        # Feature text with custom styling
        feature_font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 28)
        features = "74 CHALLENGING PUZZLES • 5 DIFFICULTY LEVELS • COMPLETE SOLUTIONS"
        draw.text((100, 300), features, fill=(100, 100, 130), font=feature_font)
        
        # Main decorative grid
        self.draw_grid(draw, 150, 400, 900, 16, line_width=2, 
                      color=(0, 0, 90), fill_numbers=True)
        
        # Smaller accent grids
        self.draw_grid(draw, 50, 1400, 200, 9, line_width=1, color=(70, 90, 180))
        self.draw_grid(draw, 950, 1400, 200, 9, line_width=1, color=(70, 90, 180))
        
        return cover

    def create_back_cover(self) -> Image:
        """Generate the back cover design"""
        back = Image.new("RGB", (self.WIDTH, self.HEIGHT), (255, 255, 255))
        draw = ImageDraw.Draw(back)
        
        # Subtle gradient background
        gradient = self.create_gradient((250, 252, 255), (240, 244, 255), self.HEIGHT)
        for y, color in enumerate(gradient):
            draw.line([(0, y), (self.WIDTH, y)], fill=color)
        
        # Header
        header_font = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 48)
        draw.text((100, 100), "Master the Art of Sudoku", fill=(0, 0, 128), font=header_font)
        
        # Description
        desc_font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 28)
        description = """Embark on an exciting journey through 74 meticulously crafted Sudoku puzzles, 
including five exceptional 16x16 grids that will push your skills to new heights. 

This carefully curated collection features:"""
        
        draw.multiline_text((100, 200), description, fill=(60, 60, 90), 
                           font=desc_font, spacing=40)
        
        # Feature boxes with icons
        features = [
            "🎯 Progressive difficulty system with color-coded levels",
            "🧩 Special 16x16 grids for ultimate challenges",
            "📝 Step-by-step solutions with detailed explanations",
            "🎨 Clear, high-contrast design for easy solving",
            "✨ Bonus techniques and strategies included"
        ]
        
        feature_font = ImageFont.truetype("fonts/Roboto-Medium.ttf", 28)
        for i, feature in enumerate(features):
            y_pos = 400 + i * 80
            draw.rectangle([(80, y_pos), (self.WIDTH-80, y_pos+60)], 
                         fill=(245, 247, 255))
            draw.text((100, y_pos+15), feature, fill=(60, 60, 90), font=feature_font)
        
        # Sample grid with some filled numbers
        self.draw_grid(draw, 100, 900, 300, 9, line_width=2, 
                      color=(70, 90, 180), fill_numbers=True)
        
        # Author bio placeholder
        bio_font = ImageFont.truetype("fonts/Roboto-Italic.ttf", 24)
        draw.text((500, 900), "Created by puzzle enthusiasts for puzzle enthusiasts", 
                 fill=(100, 100, 130), font=bio_font)
        
        # ISBN and barcode area
        draw.rectangle([(self.WIDTH-350, self.HEIGHT-200), 
                       (self.WIDTH-100, self.HEIGHT-100)], fill=(240, 240, 240))
        isbn_font = ImageFont.truetype("fonts/Roboto-Regular.ttf", 24)
        draw.text((self.WIDTH-340, self.HEIGHT-180), "ISBN: 978-0-000000-0-0", 
                 fill=(60, 60, 90), font=isbn_font)
        
        return back

def main():
    generator = BookCoverGenerator()
    front_cover = generator.create_front_cover()
    back_cover = generator.create_back_cover()
    
    front_cover.save("sudoku_front_cover.png", "PNG", quality=95)
    back_cover.save("sudoku_back_cover.png", "PNG", quality=95)
    
if __name__ == "__main__":
    main()