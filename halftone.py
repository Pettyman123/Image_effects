import numpy as np
from PIL import Image, ImageDraw

def create_bubble_dots(input_image_path, output_image_path, dot_spacing=6, max_dot_size=4):
    """
    Convert image to circular dots while preserving original colors.
    Creates a bubbly effect without any color enhancement.
    """
    img = Image.open(input_image_path).convert('RGB')
    
    # Calculate grid dimensions
    grid_width = img.width // dot_spacing
    grid_height = img.height // dot_spacing
    output_width = grid_width * dot_spacing
    output_height = grid_height * dot_spacing
    
    # Resize image to match grid
    img = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)
    
    # Create output image with white background
    output_img = Image.new('RGB', (output_width, output_height), (255, 255, 255))
    draw = ImageDraw.Draw(output_img)
    
    # Convert to numpy array for easier pixel access
    img_array = np.array(img)
    
    # Process each pixel
    for y in range(grid_height):
        for x in range(grid_width):
            # Get original pixel color (no modification)
            r, g, b = img_array[y, x]
            dot_color = (int(r), int(g), int(b))
            
            # Calculate dot size based on brightness (darker = larger dots)
            brightness = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
            dot_size = (1 - brightness) * max_dot_size
            
            # Only draw dots that are visible
            if dot_size > 0.5:
                center_x = x * dot_spacing + dot_spacing // 2
                center_y = y * dot_spacing + dot_spacing // 2
                
                # Draw circular dot
                bbox = [
                    center_x - dot_size,
                    center_y - dot_size,
                    center_x + dot_size,
                    center_y + dot_size
                ]
                draw.ellipse(bbox, fill=dot_color)
    
    # Save the result
    output_img.save(output_image_path, quality=95)
    return output_img

def create_uniform_bubble_dots(input_image_path, output_image_path, dot_spacing=6, dot_size=3):
    """
    Create uniform-sized circular dots for every pixel.
    All dots are the same size, only colors vary.
    """
    img = Image.open(input_image_path).convert('RGB')
    
    # Calculate grid dimensions
    grid_width = img.width // dot_spacing
    grid_height = img.height // dot_spacing
    output_width = grid_width * dot_spacing
    output_height = grid_height * dot_spacing
    
    # Resize image to match grid
    img = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)
    
    # Create output image with white background
    output_img = Image.new('RGB', (output_width, output_height), (255, 255, 255))
    draw = ImageDraw.Draw(output_img)
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Process each pixel
    for y in range(grid_height):
        for x in range(grid_width):
            # Get original pixel color (no modification)
            r, g, b = img_array[y, x]
            dot_color = (int(r), int(g), int(b))
            
            center_x = x * dot_spacing + dot_spacing // 2
            center_y = y * dot_spacing + dot_spacing // 2
            
            # Draw uniform circular dot
            bbox = [
                center_x - dot_size,
                center_y - dot_size,
                center_x + dot_size,
                center_y + dot_size
            ]
            draw.ellipse(bbox, fill=dot_color)
    
    # Save the result
    output_img.save(output_image_path, quality=95)
    return output_img

if __name__ == "__main__":
    create_uniform_bubble_dots("edit/3.jpg", "edit_o/output_uniform_b3.jpg", dot_spacing=6, dot_size=3)