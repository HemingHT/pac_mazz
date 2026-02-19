from pyray import *

class Player:
    def __init__(self, start_x, start_y):
        self.position = Vector2(start_x, start_y)
        self.speed = 2.0  # Reduced speed for safer testing
        self.radius = 13
        self.color = YELLOW
        self.direction = Vector2(0, 0)
        self.next_direction = Vector2(0, 0) # Buffer for input
        self.texture = load_texture("mazz.png")
        self.rectangle = Rectangle(0.0, 0.0, float(self.texture.width), float(self.texture.height))

    # 1. Update now requires the 'board' object
    def update(self, board):
        
        # Handle Input (Store it in "next_direction")
        if is_key_down(KeyboardKey.KEY_RIGHT):
            self.next_direction = Vector2(1, 0)
        elif is_key_down(KeyboardKey.KEY_LEFT):
            self.next_direction = Vector2(-1, 0)
        elif is_key_down(KeyboardKey.KEY_UP):
            self.next_direction = Vector2(0, -1)
        elif is_key_down(KeyboardKey.KEY_DOWN):
            self.next_direction = Vector2(0, 1)

        # 2. Try to move in the Desired Direction
        # Calculate where we WOULD be
        future_x = self.position.x + (self.next_direction.x * self.speed)
        future_y = self.position.y + (self.next_direction.y * self.speed)
        
        # 3. Check Collision
        # We check the CENTER point. (For perfect collision, we usually check 4 corners, 
        # but let's start with center for simplicity).
        if not board.is_wall(future_x, future_y):
            # No wall? Go there!
            self.position.x = future_x
            self.position.y = future_y
            self.direction = self.next_direction # Confirm direction
        
        center_col = int(self.position.x // board.tile_width)
        center_row = int(self.position.y // board.tile_height)
        
        # Ask the board to eat
        board.eat_dot(center_row, center_col)
            
        # If we hit a wall with new direction, try continuing in OLD direction?
        # (This makes movement smoother "cornering")
        # For now, let's just stop if we hit a wall.
        
    def draw(self):
        destRect = Rectangle(float(self.position.x), float(self.position.y), 50.0, 50.0)
        draw_texture_pro(self.texture, self.rectangle, destRect, Vector2(0.0,0.0), 0.0, WHITE)