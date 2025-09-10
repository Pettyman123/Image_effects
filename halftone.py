import numpy as np
from PIL import Image, ImageDraw

def create_perfect_dots(input_image_path, output_image_path, dot_spacing=4, dot_radius=1.8):
    """
    Create perfectly circular, uniform dots with precise positioning.
    """
    img = Image.open(input_image_path).convert('RGB')
    
    # Calculate grid dimensions
    grid_width = img.width // dot_spacing
    grid_height = img.height // dot_spacing
    output_width = grid_width * dot_spacing
    output_height = grid_height * dot_spacing
    
    # Resize image to match grid
    img = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)
    img_array = np.array(img)
    
    # Get background color from corners
    corners = [
        img_array[0, 0], 
        img_array[0, -1], 
        img_array[-1, 0], 
        img_array[-1, -1]
    ]
    bg_color = tuple(np.mean(corners, axis=0).astype(int))
    
    # Create output image
    output_img = Image.new('RGB', (output_width, output_height), bg_color)
    draw = ImageDraw.Draw(output_img)
    
    # Process each pixel
    for y in range(grid_height):
        for x in range(grid_width):
            r, g, b = img_array[y, x]
            dot_color = (int(r), int(g), int(b))
            
            # Calculate center position
            center_x = x * dot_spacing + dot_spacing // 2
            center_y = y * dot_spacing + dot_spacing // 2
            
            # Create perfect circle
            draw.ellipse([
                center_x - dot_radius,
                center_y - dot_radius,
                center_x + dot_radius,
                center_y + dot_radius
            ], fill=dot_color)
    
    output_img.save(output_image_path, quality=95)
    return output_img

def create_variable_dots(input_image_path, output_image_path, dot_spacing=4, min_radius=1.0, max_radius=2.5):
    """
    Create dots with variable sizes based on contrast from background.
    """
    img = Image.open(input_image_path).convert('RGB')
    
    # Calculate grid dimensions
    grid_width = img.width // dot_spacing
    grid_height = img.height // dot_spacing
    output_width = grid_width * dot_spacing
    output_height = grid_height * dot_spacing
    
    # Resize image to match grid
    img = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)
    img_array = np.array(img)
    
    # Get background color
    corners = [
        img_array[0, 0], 
        img_array[0, -1], 
        img_array[-1, 0], 
        img_array[-1, -1]
    ]
    bg_color = tuple(np.mean(corners, axis=0).astype(int))
    
    # Create output image
    output_img = Image.new('RGB', (output_width, output_height), bg_color)
    draw = ImageDraw.Draw(output_img)
    
    # Process each pixel
    for y in range(grid_height):
        for x in range(grid_width):
            r, g, b = img_array[y, x]
            dot_color = (int(r), int(g), int(b))
            
            # Calculate color difference from background
            color_diff = np.sqrt((r - bg_color[0])**2 + (g - bg_color[1])**2 + (b - bg_color[2])**2)
            
            # Variable dot size based on contrast
            size_factor = min(color_diff / 100.0, 1.0)
            dot_radius = min_radius + (max_radius - min_radius) * size_factor
            
            # Only draw significant dots
            if color_diff > 10:
                center_x = x * dot_spacing + dot_spacing // 2
                center_y = y * dot_spacing + dot_spacing // 2
                
                draw.ellipse([
                    center_x - dot_radius,
                    center_y - dot_radius,
                    center_x + dot_radius,
                    center_y + dot_radius
                ], fill=dot_color)
    
    output_img.save(output_image_path, quality=95)
    return output_img

def create_dense_dots(input_image_path, output_image_path, dot_spacing=3, dot_radius=1.5):
    """
    Create dense, uniform dots for maximum detail.
    """
    img = Image.open(input_image_path).convert('RGB')
    
    # Calculate grid dimensions
    grid_width = img.width // dot_spacing
    grid_height = img.height // dot_spacing
    output_width = grid_width * dot_spacing
    output_height = grid_height * dot_spacing
    
    # Resize image to match grid
    img = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)
    img_array = np.array(img)
    
    # Get background color from edges
    top_row = img_array[0, :]
    bottom_row = img_array[-1, :]
    left_col = img_array[:, 0]
    right_col = img_array[:, -1]
    
    edge_pixels = np.vstack([top_row, bottom_row, left_col, right_col])
    bg_color = tuple(np.median(edge_pixels, axis=0).astype(int))
    
    # Create output image
    output_img = Image.new('RGB', (output_width, output_height), bg_color)
    draw = ImageDraw.Draw(output_img)
    
    # Process each pixel
    for y in range(grid_height):
        for x in range(grid_width):
            r, g, b = img_array[y, x]
            dot_color = (int(r), int(g), int(b))
            
            center_x = x * dot_spacing + dot_spacing // 2
            center_y = y * dot_spacing + dot_spacing // 2
            
            draw.ellipse([
                center_x - dot_radius,
                center_y - dot_radius,
                center_x + dot_radius,
                center_y + dot_radius
            ], fill=dot_color)
    
    output_img.save(output_image_path, quality=95)
    return output_img

if __name__ == "__main__":
    # Perfect uniform circles
    # create_perfect_dots("edit/6.jpg", "output_perfect.jpg", 
    #                    dot_spacing=9, dot_radius=5)
    
    # Variable sized dots
    # create_variable_dots("edit/3.jpg", "output_variable.jpg", 
    #                     dot_spacing=4, min_radius=1.0, max_radius=2.5)
    
    # # Dense dots for detail
    # create_dense_dots("edit/3.jpg", "output_dense.jpg", 
    #                  dot_spacing=3, dot_radius=1.5)
    create_perfect_dots("edit/11.jpg", "output_perfect.jpg", 
                       dot_spacing=9, dot_radius=5)