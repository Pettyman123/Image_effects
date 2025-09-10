import numpy as np
from PIL import Image, ImageDraw

def comic_ben_day_dots(input_image_path, output_image_path, dot_spacing=8, dot_scale=0.9, sample="center"):
    """
    Create a comic-style Ben-Day halftone with clean circular colored dots.

    Parameters:
      dot_spacing - distance between dot centers (larger = fewer, bigger dots)
      dot_scale   - 0..1, fraction of cell size that dot should fill
      sample      - 'center' or 'mean': how to choose the cell's color
    """
    img = Image.open(input_image_path).convert('RGB')
    width, height = img.size
    
    # Output canvas, same size as input
    output_img = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(output_img)
    
    img_array = np.array(img)
    
    for y in range(0, height, dot_spacing):
        for x in range(0, width, dot_spacing):
            x2 = min(x + dot_spacing, width)
            y2 = min(y + dot_spacing, height)
            
            if sample == "mean":
                block = img_array[y:y2, x:x2]
                r, g, b = np.mean(block.reshape(-1, 3), axis=0)
            else:  # center
                cx = x + (x2 - x)//2
                cy = y + (y2 - y)//2
                r, g, b = img_array[cy, cx]
            
            dot_color = (int(r), int(g), int(b))
            
            # Dot radius (fills most of cell)
            radius = dot_spacing * dot_scale / 2
            cx = x + dot_spacing // 2
            cy = y + dot_spacing // 2
            
            bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
            draw.ellipse(bbox, fill=dot_color)
    
    output_img.save(output_image_path, quality=95)
    return output_img

# Example usage
comic_ben_day_dots("edit/6.jpg", "comic_.jpg", dot_spacing=8, dot_scale=0.95, sample="center")
