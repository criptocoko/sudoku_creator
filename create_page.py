from PIL import Image, ImageDraw, ImageFont
import json
import os
import colorsys

puzzle_number = 1

class SudokuImageGenerator:
    def __init__(self):
        # Existing initialization code remains the same
        self.bg_color = (255, 255, 255)  # White
        self.grid_color = (80, 156, 143)  # Teal green from template
        self.wave_color = (198, 228, 223)  # Light teal for background waves
        
        # Define dimensions
        self.cell_size = 100  # Size of each sudoku cell
        self.grid_size = self.cell_size * 9
        self.padding = 150  # Padding around the page edges
        self.page_width = 1800
        self.page_height = 2700
        self.difficulty_bg_colors = {
            "easy": '#45a049',
            "medium": "#1976D2",
            "hard": "#F57C00",
            "extreme": "#C2185B",
            "impossible": "#7B1FA2"
        }
        
        # Modify font sizes to be larger
        try:
            self.font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 48)  # Increased from 30
            self.title_font = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 52)
            self.solution_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 30)  # Increased from 20
        except:
            self.font = ImageFont.load_default()
            self.title_font = ImageFont.load_default()
            self.solution_font = ImageFont.load_default()

    def lighten_color(self, hex_color, factor=0.8):
        """Lightens the given color by converting it to HLS and increasing the lightness."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = min(1.0, l + (1.0 - l) * factor)  # Increase lightness
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f'#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}'

    # Existing methods remain the same...
    def draw_waves(self, draw, width, height):
        """Draw the wavy background pattern"""
        for y in range(0, height, 100):
            draw.ellipse([-50, y, width+50, y+200], fill=self.wave_color)

    def draw_grid(self, draw, start_x, start_y, cell_size=None):
        """Draw the sudoku grid"""
        if cell_size is None:
            cell_size = self.cell_size
        grid_size = cell_size * 9
        
        for i in range(10):
            # Increase the line width for 3x3 grid borders
            line_width = 4 if i % 3 == 0 else 1  # Changed from 2 to 4
            # Vertical lines
            draw.line([(start_x + i * cell_size, start_y),
                      (start_x + i * cell_size, start_y + grid_size)],
                     fill=self.grid_color, width=line_width)
            # Horizontal lines
            draw.line([(start_x, start_y + i * cell_size),
                      (start_x + grid_size, start_y + i * cell_size)],
                     fill=self.grid_color, width=line_width)

    def draw_numbers(self, draw, puzzle, start_x, start_y, cell_size=None, font=None):
        """Draw the numbers in the grid"""
        if cell_size is None:
            cell_size = self.cell_size
        if font is None:
            font = self.font
            
        for row in range(9):
            for col in range(9):
                number = puzzle[row][col]
                if number is not None:
                    text_bbox = draw.textbbox((0, 0), str(number), font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    x = start_x + col * cell_size + (cell_size - text_width) // 2
                    y = start_y + row * cell_size + (cell_size - text_height) // 2 - text_height//2
                    draw.text((x+1, y), str(number), fill="black", font=font)

    def generage_footer(self, draw, page_number):
        """Generate the footer for the page"""
        footer_height = self.page_height - self.padding//2
        # Create new image with white background
        draw.line([(self.padding, footer_height), (self.page_width//2-self.padding, footer_height)], fill="black", width=5)
        # footer line 2
        draw.line([(self.page_width//2 + self.padding, footer_height), (self.page_width - self.padding, footer_height)], fill="black", width=5)
        page_number_str = str(page_number)
        text_bbox = draw.textbbox((0, 0), page_number_str, font=self.title_font)
        text_width = text_bbox[2] - text_bbox[0]
        # write the page number
        draw.text(
            (self.page_width//2-text_width/len(page_number_str), self.page_height - self.padding//1.2),
            page_number_str,
            fill="black",
            font=self.title_font
        )


    def generate_page(self, puzzles, output_path, page_number, difficulty):
        """Generate a page with either one or two sudoku boards"""
        # Create new image with white background
        img = Image.new('RGB', (self.page_width, self.page_height), self.lighten_color(self.difficulty_bg_colors[difficulty.lower()]))
        draw = ImageDraw.Draw(img)

        # Draw background waves
        #self.draw_waves(draw, self.page_width, self.page_height)

        # Calculate exact vertical positions
        # The formula is: padding + grid + padding + grid + padding = page_height
        # Therefore: total_remaining_space = page_height - (2 * grid_size)
        # And this space should be divided into 3 equal parts (top, middle, bottom padding)
        
        remaining_space = self.page_height - (2 * self.grid_size)
        actual_padding = remaining_space // 3  # This ensures exactly equal spacing
        
        # Calculate Y positions for grids
        top_grid_y = actual_padding
        bottom_grid_y = actual_padding + self.grid_size + actual_padding

        # Determine horizontal positions based on page number
        left_x = self.page_width // 3 - self.grid_size // 2
        right_x = self.page_width // 1.5 - self.grid_size // 2
        if page_number % 2 != 0:  # odd page (left page)
            positions = [
                (left_x, top_grid_y),    # First board
                (right_x, bottom_grid_y)  # Second board
            ]
        else:  # even page (right page)
            positions = [
                (right_x, top_grid_y),    # First board
                (left_x, bottom_grid_y)   # Second board
            ]

        # Draw title in the exact center between the grids
        title = f"Difficulty Level:     {difficulty}"
        title_bbox = draw.textbbox((0, 0), title, font=self.title_font)
        title_height = title_bbox[3] - title_bbox[1]
        title_y = top_grid_y + self.grid_size + (actual_padding - title_height) // 2
       
        draw.text(
            (self.padding, title_y),
            title,
            fill="black",
            font=self.title_font
        )
        # header line
        draw.line([(self.padding, self.padding//2), (self.page_width - self.padding, self.padding//2)], fill="black", width=5)

        self.generage_footer(draw, page_number)
        # Draw grids and numbers
        for i, (start_x, start_y) in enumerate(positions):
            self.draw_grid(draw, start_x, start_y)
            if i < len(puzzles) and puzzles[i] is not None:
                self.draw_numbers(draw, puzzles[i], start_x, start_y)
                # Calculate position for puzzle number
                global puzzle_number
                right_x = start_x + self.grid_size + self.padding
                left_x = start_x - self.padding
                if page_number % 2 == 1:
                    position_x = right_x if not i % 2 else left_x
                else:
                    position_x = left_x if not i % 2 else right_x
                
                # Get text dimensions for centering the circle
                text_bbox = draw.textbbox((0, 0), str(puzzle_number), font=self.title_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # Draw circle first (so it's behind the text)
                circle_radius = max(text_width, text_height) // 2 + 15  # Add some padding
                circle_top_left = (
                    position_x - circle_radius,
                    start_y - circle_radius + text_height//1.5
                )
                circle_bottom_right = (
                    position_x + circle_radius,
                    start_y + circle_radius + text_height//1.5
                )
                draw.ellipse([circle_top_left, circle_bottom_right], outline="black", width=2)
                
                # Draw the number (in the same position as before)
                draw.text(
                    (position_x - text_width//2, start_y-7),
                    str(puzzle_number),
                    fill="black",
                    font=self.title_font
                )
                puzzle_number += 1

        # Save the image
        img.save(output_path, 'PNG', dpi=(300, 300))


    def generate_solution_page(self, solutions, start_puzzle_num, page_number, output_path):
        """Generate a page with 9 solution grids (3x3)"""
        # Create new image with white background
        img = Image.new('RGB', (self.page_width, self.page_height), self.bg_color)
        draw = ImageDraw.Draw(img)
        # paint the background
        

        # Draw background waves
        self.draw_waves(draw, self.page_width, self.page_height)

        # Calculate cell size for solutions (larger than before)
        solution_cell_size = 50  # Increased from 25
        solution_grid_size = solution_cell_size * 9
        
        # Calculate spacing
        horizontal_spacing = (self.page_width - (3 * solution_grid_size)) // 4
        vertical_spacing = (self.page_height - (4 * solution_grid_size) - self.padding * 2) // 5

        # Draw title
        title = f"Solutions {start_puzzle_num}-{start_puzzle_num + len(solutions) - 1}"
        draw.text(
            (self.padding, self.padding//2),
            title,
            fill="black",
            font=self.title_font
        )

        # Draw header line
        draw.line([(self.padding, self.padding), 
                   (self.page_width - self.padding, self.padding)], 
                  fill="black", width=5)

        # Draw solutions in 3x3 grid
        for i, solution in enumerate(solutions):
            if i >= 12:  # Maximum 9 solutions per page
                break
                
            row = i // 3
            col = i % 3
            
            start_x = horizontal_spacing + col * (solution_grid_size + horizontal_spacing)
            start_y = self.padding + vertical_spacing + row * (solution_grid_size + vertical_spacing)

            # Draw grid and numbers
            self.draw_grid(draw, start_x, start_y, solution_cell_size)
            self.draw_numbers(draw, solution, start_x, start_y, solution_cell_size, self.solution_font)
            
            # Draw puzzle number
            puzzle_num = start_puzzle_num + i
            draw.text(
                (start_x + solution_grid_size + 10, start_y),
                f"#{puzzle_num}",
                fill="black",
                font=self.solution_font
            )

        # Draw footer
        self.generage_footer(draw, page_number)

        # Save the image
        img.save(output_path, 'PNG', dpi=(300, 300))

def main():
    # Load puzzle data from JSON
    with open('all_sudokus.json', 'r') as f:
        data = json.load(f)
    
    puzzles = data['puzzles']
    generator = SudokuImageGenerator()
    
    # Generate regular puzzle pages
    counter_page = 1
    for i in range(0, len(puzzles), 2):
        if i + 1 < len(puzzles):
            if 'skip' in puzzles[i]:
                print(f"Skipping page {counter_page}")
                counter_page += 1
                continue
            games = [puzzle['puzzle'] for puzzle in puzzles[i:i+2]]
            generator.generate_page(games, f'book/page_{counter_page}.png', counter_page, puzzles[i]['difficulty_level'])
            counter_page += 1
        else:
            break

    # Generate solution pages
    solutions_per_page = 12
    filtered_solutions = [puzzle['solution'] for puzzle in puzzles if 'skip' not in puzzle]

    counter_page = 1
    for i in range(0, len(filtered_solutions), solutions_per_page):
        solutions_batch = filtered_solutions[i:i + solutions_per_page]
        
        if solutions_batch:  # Ensure there's something to process
            generator.generate_solution_page(
                solutions_batch,
                i + 1,  # Start puzzle number
                counter_page,
                f'book/page_sol_{counter_page}.png'
            )
            counter_page += 1


if __name__ == "__main__":
    main()