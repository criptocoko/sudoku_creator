from PIL import Image, ImageDraw, ImageFont
import json
import os
import colorsys

puzzle_number = 1

class SudokuImageGenerator:
    def __init__(self):
        self.bg_color = (255, 255, 255)  # White
        self.grid_color = (80, 156, 143)  # Teal green
        self.wave_color = (198, 228, 223)  # Light teal for background waves
        
        # Define dimensions for 9x9 Sudoku
        self.cell_size_9x9 = 100
        self.grid_size_9x9 = self.cell_size_9x9 * 9
        self.padding = 150
        self.page_width = 1800
        self.page_height = 2700

        # Define dimensions for 16x16 Sudoku (adjust as needed)
        self.cell_size_16x16 = self.cell_size_9x9  # Smaller cell size for larger grid
        self.grid_size_16x16 = self.cell_size_16x16 * 16
        self.padding_16x16 = self.padding  # Adjust padding if needed
        self.page_width_16x16 = 1800 # Adjust as needed for A4 landscape
        self.page_height_16x16 = 2700

        
        self.difficulty_bg_colors = {
            "easy": '#45a049',
            "medium": "#1976D2",
            "hard": "#F57C00",
            "extreme": "#C2185B",
            "impossible": "#7B1FA2"
        }
        
        try:
            self.font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 48)
            self.title_font = ImageFont.truetype("fonts/Montserrat-Bold.ttf", 52)
            self.solution_font = ImageFont.truetype("fonts/Roboto-Bold.ttf", 30)

        except Exception:
            self.font = ImageFont.load_default()
            self.title_font = ImageFont.load_default()
            self.solution_font = ImageFont.load_default()
            print("An error occurred on loading the fonts, the system is using the default font")

    def lighten_color(self, hex_color, factor=0.8):
        """Lightens the given color."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = min(1.0, l + (1.0 - l) * factor)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f'#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}'

    def draw_waves(self, draw, width, height):
        """Draw the wavy background pattern."""
        for y in range(0, height, 100):
            draw.ellipse([-50, y, width+50, y+200], fill=self.wave_color)

    def draw_grid(self, draw, start_x, start_y, cell_size, grid_size, num_cells):
        """Draw the sudoku grid (supports both 9x9 and 16x16)."""
        for i in range(num_cells + 1):
            if num_cells == 9:
                line_width = 4 if i % 3 == 0 else 1
            else: # 16x16 grid
                line_width = 4 if i % 4 == 0 else 1

            # Vertical lines
            draw.line([(start_x + i * cell_size, start_y),
                       (start_x + i * cell_size, start_y + grid_size)],
                      fill=self.grid_color, width=line_width)
            # Horizontal lines
            draw.line([(start_x, start_y + i * cell_size),
                      (start_x + grid_size, start_y + i * cell_size)],
                      fill=self.grid_color, width=line_width)

    def draw_numbers(self, draw, puzzle, start_x, start_y, cell_size, font):
        """Draw the numbers in the grid (supports both 9x9 and 16x16)."""
        num_cells = len(puzzle)
        for row in range(num_cells):
            for col in range(num_cells):
                number = puzzle[row][col]
                if number is not None:
                    # Convert number to string (for 16x16, handles A, B, C, etc.)
                    text = str(number)
                    text_bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    x = start_x + col * cell_size + (cell_size - text_width) // 2
                    y = start_y + row * cell_size + (cell_size - text_height) // 2 - text_height//2
                    draw.text((x + 1, y), text, fill="black", font=font)
    def generage_footer(self, draw, page_number, page_width, page_height, padding):
        """Generate the footer for the page"""
        footer_height = page_height - padding//2
        # Create new image with white background
        draw.line([(padding, footer_height), (page_width//2-padding, footer_height)], fill="black", width=5)
        # footer line 2
        draw.line([(page_width//2 + padding, footer_height), (page_width - padding, footer_height)], fill="black", width=5)
        page_number_str = str(page_number)
        text_bbox = draw.textbbox((0, 0), page_number_str, font=self.title_font)
        text_width = text_bbox[2] - text_bbox[0]
        # write the page number
        draw.text(
            (page_width//2-text_width/len(page_number_str), page_height - padding//1.2),
            page_number_str,
            fill="black",
            font=self.title_font
        )

    def generate_9x9_page(self, puzzles, output_path, page_number, difficulty):
        """Generate a page with two 9x9 sudoku boards."""
        img = Image.new('RGB', (self.page_width, self.page_height), self.lighten_color(self.difficulty_bg_colors[difficulty.lower()]))
        draw = ImageDraw.Draw(img)

        remaining_space = self.page_height - (2 * self.grid_size_9x9)
        actual_padding = remaining_space // 3
        
        top_grid_y = actual_padding
        bottom_grid_y = actual_padding + self.grid_size_9x9 + actual_padding

        left_x = self.page_width // 3 - self.grid_size_9x9 // 2
        right_x = self.page_width // 1.5 - self.grid_size_9x9 // 2
        if page_number % 2 != 0:
            positions = [(left_x, top_grid_y), (right_x, bottom_grid_y)]
        else:
            positions = [(right_x, top_grid_y), (left_x, bottom_grid_y)]

        title = f"Difficulty Level:     {difficulty}"
        title_bbox = draw.textbbox((0, 0), title, font=self.title_font)
        title_height = title_bbox[3] - title_bbox[1]
        title_y = top_grid_y + self.grid_size_9x9 + (actual_padding - title_height) // 2
       
        draw.text((self.padding, title_y), title, fill="black", font=self.title_font)
        draw.line([(self.padding, self.padding//2), (self.page_width - self.padding, self.padding//2)], fill="black", width=5)

        self.generage_footer(draw, page_number, self.page_width, self.page_height, self.padding)

        for i, (start_x, start_y) in enumerate(positions):
            self.draw_grid(draw, start_x, start_y, self.cell_size_9x9, self.grid_size_9x9, 9)
            if i < len(puzzles) and puzzles[i] is not None:
                self.draw_numbers(draw, puzzles[i], start_x, start_y, self.cell_size_9x9, self.font)
                global puzzle_number
                right_x = start_x + self.grid_size_9x9 + self.padding
                left_x = start_x - self.padding
                if page_number % 2 == 1:
                    position_x = right_x if not i % 2 else left_x
                else:
                    position_x = left_x if not i % 2 else right_x

                text_bbox = draw.textbbox((0, 0), str(puzzle_number), font=self.title_font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                circle_radius = max(text_width, text_height) // 2 + 15
                circle_top_left = (position_x - circle_radius, start_y - circle_radius + text_height//1.5)
                circle_bottom_right = (position_x + circle_radius, start_y + circle_radius + text_height//1.5)
                draw.ellipse([circle_top_left, circle_bottom_right], outline="black", width=2)
                draw.text((position_x - text_width//2, start_y-7), str(puzzle_number), fill="black", font=self.title_font)
                puzzle_number += 1

        img.save(output_path, 'PNG', dpi=(300, 300))


    def generate_16x16_page(self, puzzle, output_path, page_number, difficulty):
        """Generate a single page with one 16x16 sudoku board."""
        global puzzle_number
        img = Image.new('RGB', (self.page_width_16x16, self.page_height_16x16), self.lighten_color(self.difficulty_bg_colors[difficulty.lower()]))
        draw = ImageDraw.Draw(img)

        # Center the grid
        start_x = (self.page_width_16x16 - self.grid_size_16x16) // 2
        start_y = (self.page_height_16x16 - self.grid_size_16x16) // 2
         # header line
        draw.line([(self.padding_16x16, self.padding_16x16//2), (self.page_width_16x16 - self.padding_16x16, self.padding_16x16//2)], fill="black", width=5)

        # Draw title at the top, centered
        title = f"Difficulty Level: {difficulty} - Puzzle #{puzzle_number}"
        title_bbox = draw.textbbox((0, 0), title, font=self.title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.page_width_16x16 - title_width) // 2
        draw.text((title_x, self.padding_16x16 // 2), title, fill="black", font=self.title_font)  # Adjusted y-coordinate

        # Draw grid and numbers
        self.draw_grid(draw, start_x, start_y, self.cell_size_16x16, self.grid_size_16x16, 16)  # Use 16 for 16x16 grid
        if puzzle is not None:
            self.draw_numbers(draw, puzzle, start_x, start_y, self.cell_size_16x16, self.font)  # Use font_16x16
        
        self.generage_footer(draw, page_number, self.page_width_16x16, self.page_height_16x16, self.padding_16x16)
        # Increment the puzzle number
        puzzle_number += 1

        # Save the image
        img.save(output_path, 'PNG', dpi=(300, 300))

    def generate_9x9_solution_page(self, solutions, start_puzzle_num, page_number, output_path):
        """Generate a page with 9x9 solution grids (3x3 layout)."""
        img = Image.new('RGB', (self.page_width, self.page_height), self.bg_color)
        draw = ImageDraw.Draw(img)

        solution_cell_size = 50
        solution_grid_size = solution_cell_size * 9
        
        horizontal_spacing = (self.page_width - (3 * solution_grid_size)) // 4
        vertical_spacing = (self.page_height - (4 * solution_grid_size) - self.padding * 2) // 5

        title = f"Solutions {start_puzzle_num}-{start_puzzle_num + len(solutions) - 1}"
        draw.text((self.padding, self.padding//2), title, fill="black", font=self.title_font)

        draw.line([(self.padding, self.padding), (self.page_width - self.padding, self.padding)], fill="black", width=5)

        for i, solution in enumerate(solutions):
            if i >= 12:
                break
                
            row = i // 3
            col = i % 3
            
            start_x = horizontal_spacing + col * (solution_grid_size + horizontal_spacing)
            start_y = self.padding + vertical_spacing + row * (solution_grid_size + vertical_spacing)

            self.draw_grid(draw, start_x, start_y, solution_cell_size, solution_grid_size, 9)
            self.draw_numbers(draw, solution, start_x, start_y, solution_cell_size, self.solution_font)
            
            puzzle_num = start_puzzle_num + i
            draw.text((start_x + solution_grid_size + 10, start_y), f"#{puzzle_num}", fill="black", font=self.solution_font)

        self.generage_footer(draw, page_number, self.page_width, self.page_height, self.padding)
        img.save(output_path, 'PNG', dpi=(300, 300))

    def generate_16x16_solution_page(self, solutions, start_puzzle_num, page_number, output_path):
        """Generate a page with 16x16 solution grids (4x4 layout)."""
        img = Image.new('RGB', (self.page_width_16x16, self.page_height_16x16), self.bg_color) # Use 16x16 dimensions
        draw = ImageDraw.Draw(img)

        # Smaller cell size for solutions
        solution_cell_size = 42
        solution_grid_size = solution_cell_size * 16  # 16x16 grid

        # Calculate spacing (fit 4x4 solutions)
        horizontal_spacing = (self.page_width_16x16 - (2 * solution_grid_size)) // 3
        vertical_spacing = (self.page_height_16x16 - (2 * solution_grid_size) ) // 3


        # Draw title (Solutions)
        title = f"Solutions {start_puzzle_num}-{start_puzzle_num + len(solutions) - 1}"
        draw.text((self.padding_16x16, self.padding_16x16 // 2), title, fill="black", font=self.title_font) #Use 16x16 paddings
        # header line
        draw.line([(self.padding_16x16, self.padding_16x16), (self.page_width_16x16 - self.padding_16x16, self.padding_16x16)], fill="black", width=5)


        for i, solution in enumerate(solutions):
            if i >= 4:  # Maximum 16 solutions per page
                break

            row = i // 2  # 4 solutions per row
            col = i % 2

            start_x = horizontal_spacing + col * (solution_grid_size + horizontal_spacing)
            start_y = self.padding_16x16 + vertical_spacing + row * (solution_grid_size + vertical_spacing)


            # Draw grid and numbers
            self.draw_grid(draw, start_x, start_y, solution_cell_size, solution_grid_size, 16)  # 16x16 grid
            self.draw_numbers(draw, solution, start_x, start_y, solution_cell_size, self.solution_font)  # Use solution_font_16x16

            # Draw puzzle number
            puzzle_num = start_puzzle_num + i
            draw.text((start_x + solution_grid_size + 10, start_y), f"#{puzzle_num}", fill="black", font=self.solution_font)
        
        self.generage_footer(draw, page_number, self.page_width_16x16, self.page_height_16x16, self.padding_16x16)
        img.save(output_path, 'PNG', dpi=(300, 300))

def main():
    global puzzle_number
    # --- 9x9 Sudoku Generation ---
    with open('all_sudokus.json', 'r') as f:
        data_9x9 = json.load(f)
    
    puzzles_9x9 = data_9x9['puzzles']
    generator = SudokuImageGenerator()
    
    puzzle_number = 1  # Reset for each section
    counter_page_9x9 = 1
    for i in range(0, len(puzzles_9x9), 2):
        if i + 1 < len(puzzles_9x9):
            if 'skip' in puzzles_9x9[i]:
                print(f"Skipping 9x9 page {counter_page_9x9}")
                counter_page_9x9 += 1
                continue
            games = [puzzle['puzzle'] for puzzle in puzzles_9x9[i:i+2]]
            generator.generate_9x9_page(games, f'book/page_{counter_page_9x9}.png', counter_page_9x9, puzzles_9x9[i]['difficulty_level'])
            counter_page_9x9 += 1
        else:
            break

    # --- 9x9 Solution Generation ---
    solutions_per_page_9x9 = 12
    filtered_solutions_9x9 = [puzzle['solution'] for puzzle in puzzles_9x9 if 'skip' not in puzzle]

    puzzle_number = 1
    counter_page_9x9_sol = 1
    for i in range(0, len(filtered_solutions_9x9), solutions_per_page_9x9):
        solutions_batch = filtered_solutions_9x9[i:i + solutions_per_page_9x9]
        if solutions_batch:
            generator.generate_9x9_solution_page(solutions_batch, i + 1, counter_page_9x9_sol, f'book/page_sol_{counter_page_9x9_sol}.png')
            counter_page_9x9_sol += 1

    # --- 16x16 Sudoku Generation ---
    with open('all_sudokus_B.json', 'r') as f:
        data_16x16 = json.load(f)

    puzzles_16x16 = data_16x16['puzzles']

    puzzle_number = 1  # Reset for 16x16
    counter_page_16x16 = 1
    for puzzle in puzzles_16x16:
        if 'skip' in puzzle:
            print(f"Skipping 16x16 page {counter_page_16x16}")
            counter_page_16x16 += 1
            continue
        generator.generate_16x16_page(puzzle['puzzle'], f'book/page_16x16_{counter_page_16x16}.png', counter_page_16x16, puzzle['difficulty_level'])
        counter_page_16x16 += 1

    # --- 16x16 Solution Generation ---
    solutions_per_page_16x16 = 4  # One page per 4x4 solutions
    filtered_solutions_16x16 = [p['solution'] for p in puzzles_16x16 if 'skip' not in p]

    puzzle_number = 1
    counter_page_16x16_sol = 1
    for i in range(0, len(filtered_solutions_16x16), solutions_per_page_16x16):
        solutions_batch = filtered_solutions_16x16[i : i + solutions_per_page_16x16]
        if solutions_batch:
            generator.generate_16x16_solution_page(solutions_batch, i + 1, counter_page_16x16_sol, f'book/page_16x16_sol_{counter_page_16x16_sol}.png')
            counter_page_16x16_sol += 1


if __name__ == "__main__":
    main()