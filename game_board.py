from pyray import *
from levels import BoardStructure

class GameBoard:
    def __init__(self, screen_width, screen_height, level):
        self.level = level
        self.board = level.board
        
        # Calculate Tile Size
        # We reserve 50px at the bottom for score/lives
        SCORE_OFFSET = 50
        self.tile_height = (screen_height - SCORE_OFFSET) // level.height
        self.tile_width = screen_width // level.width
        
        # Flicker State (for Big Dots)
        self.flick = False
        self.flicker_timer = 0
        
        # Pre-define colors to save processing time
        # (Assuming your level object has tuples like (0,0,255))
        self.wall_color = self._to_raylib_color(level.wall_color)
        self.gate_color = self._to_raylib_color(level.gate_color)
        
        # Wall Thickness
        self.thick = 3.0
        
        self.score = 0

    def _to_raylib_color(self, color_tuple):
        """Converts (R, G, B) tuple to Raylib Color"""
        return Color(color_tuple[0], color_tuple[1], color_tuple[2], 255)

    def _calculate_flick(self):
        self.flicker_timer += 1
        # Flip every 15 frames (adjust for speed)
        if self.flicker_timer > 15:
            self.flick = not self.flick
            self.flicker_timer = 0

    def render_level(self):
        self._calculate_flick()
        
        # Cache standard sizes
        half_w = self.tile_width / 2.0
        half_h = self.tile_height / 2.0
        
        # CORNER LOGIC: 
        # (Origin Offset X, Origin Offset Y, Start Angle, End Angle)
        # 0 = Left/Top edge, 1 = Right/Bottom edge
        corner_rules = {
            BoardStructure.TOP_RIGHT_CORNER.value:    (0, 1, 270, 360), # ┐
            BoardStructure.TOP_LEFT_CORNER.value:     (1, 1, 180, 270), # ┌
            BoardStructure.BOTTOM_LEFT_CORNER.value:  (1, 0, 90,  180), # └
            BoardStructure.BOTTOM_RIGHT_CORNER.value: (0, 0, 0,   90),  # ┘
        }

        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                
                # Top-left pixel of this tile
                x = j * self.tile_width
                y = i * self.tile_height
                center = Vector2(x + half_w, y + half_h)

                # --- 1. DOTS ---
                if cell == BoardStructure.DOT.value:
                    draw_circle_v(center, 4, self.gate_color)
                
                elif cell == BoardStructure.BIG_DOT.value:
                    if not self.flick:
                        draw_circle_v(center, 10, self.gate_color)

                # --- 2. WALLS (Straight) ---
                elif cell == BoardStructure.VERTICAL_WALL.value:
                    start = Vector2(center.x, y)
                    end = Vector2(center.x, y + self.tile_height)
                    draw_line_ex(start, end, self.thick, self.wall_color)

                elif cell == BoardStructure.HORIZONTAL_WALL.value:
                    start = Vector2(x, center.y)
                    end = Vector2(x + self.tile_width, center.y)
                    draw_line_ex(start, end, self.thick, self.wall_color)
                
                elif cell == BoardStructure.GATE.value:
                    start = Vector2(x, center.y)
                    end = Vector2(x + self.tile_width, center.y)
                    draw_line_ex(start, end, self.thick, self.gate_color)

                # --- 3. CORNERS (Curved) ---
                elif cell in corner_rules:
                    ox, oy, start_ang, end_ang = corner_rules[cell]
                    
                    # Calculate the pivot point for the arc
                    origin = Vector2(x + (ox * self.tile_width), y + (oy * self.tile_height))
                    
                    # Draw Ring: (center, inner_radius, outer_radius, start_angle, end_angle, segments, color)
                    # Inner/Outer radius creates the line thickness
                    draw_ring(origin, half_w - 1.5, half_w + 1.5, start_ang, end_ang, 16, self.wall_color)
            
    # Add this inside class GameBoard:
    
    def is_wall(self, x, y):
        # 1. Convert pixel coordinates (e.g., 340, 400) to grid coordinates (e.g., Row 10, Col 5)
        col = int(x // self.tile_width)
        row = int(y // self.tile_height)
        
        # 2. Safety Check: Keep inside the array bounds
        if col < 0 or col >= self.level.width or row < 0 or row >= self.level.height:
            return True # Treat "out of bounds" as a wall
            
        # 3. Check the map value
        cell_value = self.board[row][col]
        
        # 4. Return True if it is NOT empty and NOT a dot/gate
        # (Meaning: It is a wall or corner)
        # Note: We treat GATE as a wall for Pac-Man
        safe_tiles = [
            BoardStructure.EMPTY.value,
            BoardStructure.DOT.value, 
            BoardStructure.BIG_DOT.value
        ]
        
        return cell_value not in safe_tiles
    
    def eat_dot(self, row, col):
        # 1. Get what is at this position
        cell = self.board[row][col]
        
        # 2. If it is a small dot
        if cell == BoardStructure.DOT.value:
            self.board[row][col] = BoardStructure.EMPTY.value  # Delete it
            self.score += 10                                   # Points!
            return True # "Yes, I ate something"
            
        # 3. If it is a Big Dot
        elif cell == BoardStructure.BIG_DOT.value:
            self.board[row][col] = BoardStructure.EMPTY.value
            self.score += 50
            # TODO: Make ghosts scared here later
            return True
            
        return False