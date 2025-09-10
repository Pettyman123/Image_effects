import numpy as np
from PIL import Image, ImageDraw
import math

def enhance_color_saturation(r, g, b, saturation_boost=1.5, contrast_boost=1.2):
    r_norm, g_norm, b_norm = r/255.0, g/255.0, b/255.0
    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    diff = max_val - min_val
    
    if max_val == 0:
        saturation = 0
    else:
        saturation = diff / max_val
    
    value = max_val
    
    if diff == 0:
        hue = 0
    elif max_val == r_norm:
        hue = (60 * ((g_norm - b_norm) / diff) + 360) % 360
    elif max_val == g_norm:
        hue = (60 * ((b_norm - r_norm) / diff) + 120) % 360
    else:
        hue = (60 * ((r_norm - g_norm) / diff) + 240) % 360
    
    saturation = min(1.0, saturation * saturation_boost)
    value = min(1.0, value * contrast_boost)
    
    c = value * saturation
    x = c * (1 - abs((hue / 60) % 2 - 1))
    m = value - c
    
    if 0 <= hue < 60:
        r_new, g_new, b_new = c, x, 0
    elif 60 <= hue < 120:
        r_new, g_new, b_new = x, c, 0
    elif 120 <= hue < 180:
        r_new, g_new, b_new = 0, c, x
    elif 180 <= hue < 240:
        r_new, g_new, b_new = 0, x, c
    elif 240 <= hue < 300:
        r_new, g_new, b_new = x, 0, c
    else:
        r_new, g_new, b_new = c, 0, x
    
    r_final = int((r_new + m) * 255)
    g_final = int((g_new + m) * 255)
    b_final = int((b_new + m) * 255)
    
    return max(0, min(255, r_final)), max(0, min(255, g_final)), max(0, min(255, b_final))

def create_dot_matrix_art(input_image_path, output_image_path, dot_spacing=8, max_dot_size=6, min_dot_size=1, background_color=(240, 240, 240)):
    img = Image.open(input_image_path)
    
    output_width = (img.width // dot_spacing) * dot_spacing
    output_height = (img.height // dot_spacing) * dot_spacing
    
    img = img.resize((output_width // dot_spacing, output_height // dot_spacing), Image.Resampling.LANCZOS)
    
    output_img = Image.new('RGB', (output_width, output_height), background_color)
    draw = ImageDraw.Draw(output_img)
    
    img_array = np.array(img)
    
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    
    for y in range(img_array.shape[0]):
        for x in range(img_array.shape[1]):
            pixel_color = img_array[y, x]
            
            luminance = 0.299 * pixel_color[0] + 0.587 * pixel_color[1] + 0.114 * pixel_color[2]
            darkness = 255 - luminance
            dot_size = min_dot_size + (darkness / 255.0) * (max_dot_size - min_dot_size)
            
            center_x = x * dot_spacing + dot_spacing // 2
            center_y = y * dot_spacing + dot_spacing // 2
            
            if dot_size > 0.5:
                dot_color = tuple(pixel_color.astype(int))
                
                left = center_x - dot_size
                top = center_y - dot_size
                right = center_x + dot_size
                bottom = center_y + dot_size
                
                draw.ellipse([left, top, right, bottom], fill=dot_color)
    
    output_img.save(output_image_path, quality=95)
    return output_img

def create_advanced_dot_matrix_art(input_image_path, output_image_path, dot_spacing=6, max_dot_size=5, min_dot_size=0.5):
    img = Image.open(input_image_path).convert('RGB')
    
    grid_width = img.width // dot_spacing
    grid_height = img.height // dot_spacing
    output_width = grid_width * dot_spacing
    output_height = grid_height * dot_spacing
    
    img = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)
    
    output_img = Image.new('RGB', (output_width, output_height), (245, 245, 245))
    draw = ImageDraw.Draw(output_img)
    
    img_array = np.array(img)
    
    for y in range(grid_height):
        for x in range(grid_width):
            r, g, b = img_array[y, x]
            
            brightness = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
            dot_size = min_dot_size + (1 - brightness) * (max_dot_size - min_dot_size)
            
            center_x = x * dot_spacing + dot_spacing // 2
            center_y = y * dot_spacing + dot_spacing // 2
            
            if dot_size > 0.3:
                dot_r = max(0, min(255, int(r * 0.8)))
                dot_g = max(0, min(255, int(g * 0.8)))
                dot_b = max(0, min(255, int(b * 0.8)))
                dot_color = (dot_r, dot_g, dot_b)
                
                bbox = [
                    center_x - dot_size,
                    center_y - dot_size,
                    center_x + dot_size,
                    center_y + dot_size
                ]
                draw.ellipse(bbox, fill=dot_color)
    
    output_img.save(output_image_path, quality=95)
    return output_img

def create_vibrant_dot_matrix(input_image_path, output_image_path, dot_spacing=8, max_dot_size=6, 
                             saturation_boost=1.8, contrast_boost=1.3, color_enhancement=True):
    img = Image.open(input_image_path).convert('RGB')
    
    grid_width = img.width // dot_spacing
    grid_height = img.height // dot_spacing
    output_width = grid_width * dot_spacing
    output_height = grid_height * dot_spacing
    
    img = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)
    
    output_img = Image.new('RGB', (output_width, output_height), (240, 240, 240))
    draw = ImageDraw.Draw(output_img)
    
    img_array = np.array(img)
    
    for y in range(grid_height):
        for x in range(grid_width):
            r, g, b = img_array[y, x]
            
            if color_enhancement:
                r, g, b = enhance_color_saturation(r, g, b, saturation_boost, contrast_boost)
            
            brightness = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0
            dot_size = (1 - brightness) * max_dot_size
            
            if dot_size > 0.3:
                center_x = x * dot_spacing + dot_spacing // 2
                center_y = y * dot_spacing + dot_spacing // 2
                
                dot_color = (r, g, b)
                
                bbox = [
                    center_x - dot_size,
                    center_y - dot_size,
                    center_x + dot_size,
                    center_y + dot_size
                ]
                draw.ellipse(bbox, fill=dot_color)
    
    output_img.save(output_image_path, quality=95)
    return output_img

def create_multi_color_dot_matrix(input_image_path, output_image_path, dot_spacing=8, max_dot_size=6):
    img = Image.open(input_image_path).convert('RGB')
    
    grid_width = img.width // dot_spacing
    grid_height = img.height // dot_spacing
    output_width = grid_width * dot_spacing
    output_height = grid_height * dot_spacing
    
    img = img.resize((grid_width, grid_height), Image.Resampling.LANCZOS)
    
    output_img = Image.new('RGB', (output_width, output_height), (250, 250, 250))
    draw = ImageDraw.Draw(output_img)
    
    img_array = np.array(img)
    
    for y in range(grid_height):
        for x in range(grid_width):
            r, g, b = img_array[y, x]
            
            brightness = (r + g + b) / (3 * 255.0)
            dot_size = (1 - brightness) * max_dot_size
            
            if dot_size > 0.5:
                center_x = x * dot_spacing + dot_spacing // 2
                center_y = y * dot_spacing + dot_spacing // 2
                
                dot_color = (
                    max(0, min(255, int(r * 0.9))),
                    max(0, min(255, int(g * 0.9))),
                    max(0, min(255, int(b * 0.9)))
                )
                
                bbox = [
                    center_x - dot_size,
                    center_y - dot_size,
                    center_x + dot_size,
                    center_y + dot_size
                ]
                draw.ellipse(bbox, fill=dot_color)
    
    output_img.save(output_image_path, quality=95)
    return output_img

if __name__ == "__main__":
    create_vibrant_dot_matrix("edit/3.jpg", "output_vibrant.jpg", dot_spacing=8, max_dot_size=6, 
                             saturation_boost=1.8, contrast_boost=1.3)