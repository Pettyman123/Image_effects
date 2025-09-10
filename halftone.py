# from PIL import Image, ImageDraw
# import numpy as np

# def create_bold_halftone(image_path, grid_size=10, scale=5, dot_scale=1.5, contrast=1.5):
#     """
#     Creates a BOLD and VIBRANT color halftone effect with large, overlapping circular dots.

#     Args:
#         image_path (str): Path to the input image.
#         grid_size (int): The area to sample for each dot. Larger number = chunkier look.
#         scale (int): The resolution multiplier for the output. Higher = smoother circles.
#         dot_scale (float): The main size controller for dots. > 1.0 makes dots overlap.
#         contrast (float): Exaggerates the size difference between light and dark dots.
    
#     Returns:
#         PIL.Image.Image: The final, high-resolution halftone image.
#     """
#     try:
#         img = Image.open(image_path).convert('RGB')
#     except FileNotFoundError:
#         print(f"Error: The file '{image_path}' was not found.")
#         return None

#     width, height = img.size
    
#     # Create the high-resolution output canvas
#     output_width = width * scale
#     output_height = height * scale
#     halftone_img = Image.new('RGB', (output_width, output_height), 'white')
#     draw = ImageDraw.Draw(halftone_img)
    
#     pixels = np.array(img)
    
#     # Define the maximum possible radius for a dot before scaling
#     max_radius_base = (grid_size / 2) * scale

#     print("Generating BOLD halftone...")
#     for y in range(0, height, grid_size):
#         for x in range(0, width, grid_size):
#             cell = pixels[y:y + grid_size, x:x + grid_size]
            
#             if cell.size == 0:
#                 continue

#             # --- 1. VIBRANT COLOR SAMPLING ---
#             # Reshape cell into a list of [R, G, B] pixels
#             pixel_list = cell.reshape(-1, 3)
            
#             # Filter out pure blacks and pure whites to prevent them from washing out the color
#             # This is key to preserving the vibrant colors of the jacket and tie
#             color_pixels = pixel_list[
#                 (np.any(pixel_list > 20, axis=1)) & (np.any(pixel_list < 235, axis=1))
#             ]
            
#             if len(color_pixels) == 0:
#                 # If the patch is pure black or white, use the average of the whole patch
#                 sample_color = np.mean(pixel_list, axis=0)
#             else:
#                 # For colored areas, find the median of the TRUE colors
#                 sample_color = np.median(color_pixels, axis=0)
            
#             r, g, b = sample_color.astype(int)
#             dot_color = (r, g, b)
            
#             # --- 2. BOLD DOT SIZING ---
#             # Calculate brightness from the sampled color
#             brightness = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
            
#             # Apply contrast. A higher contrast makes light areas lighter and dark areas darker.
#             # This makes the size difference between dots much more dramatic.
#             adjusted_brightness = brightness ** contrast
            
#             # The final radius is controlled by the adjusted brightness AND the dot_scale
#             radius = (1.0 - adjusted_brightness) * max_radius_base * dot_scale

#             if radius < 1:
#                 continue # Don't draw dots that are too small to see

#             center_x = (x + grid_size / 2) * scale
#             center_y = (y + grid_size / 2) * scale
            
#             box = [
#                 center_x - radius, 
#                 center_y - radius, 
#                 center_x + radius, 
#                 center_y + radius
#             ]
#             draw.ellipse(box, fill=dot_color)

#     print("Process complete.")
#     return halftone_img

# if __name__ == '__main__':
#     # --- Configuration ---
#     input_image_path = 'edit/3.jpg' 
    
#     # --- PLAY WITH THESE VALUES TO GET THE PERFECT LOOK! ---

#     # 1. Grid Size: How "chunky" the effect is. Larger numbers mean fewer, bigger dots.
#     #    A value around 10-12 will give a nice, bold pattern.
#     sampling_grid_size = 9
    
#     # 2. Output Resolution: Keeps circles smooth. 5 is a good balance.
#     output_resolution = 10

#     # 3. DOT SCALE (MAKE THEM BIG): This is the most important setting for you.
#     #    1.0 = dots will just touch in black areas.
#     #    1.5 = dots are 50% bigger and will overlap significantly.
#     #    2.0 = very large, overlapping dots.
#     #    Let's start with a bold 1.6!
#     dot_size_multiplier = 1.1

#     # 4. Contrast: Makes the effect "pop".
#     #    1.0 = normal.
#     #    1.5 or 2.0 = punchy and graphic.
#     image_contrast = 5
    
#     # --- Execution ---
#     halftone_result = create_bold_halftone(
#         input_image_path,
#         grid_size=sampling_grid_size,
#         scale=output_resolution,
#         dot_scale=dot_size_multiplier,
#         contrast=image_contrast
#     )
    
#     if halftone_result:
#         output_image_path = 'halftone_output_BOLD.png'
#         halftone_result.save(output_image_path)
#         print(f"Bold halftone image saved as '{output_image_path}'")
        
#         try:
#             halftone_result.show()
#         except Exception as e:
#             print(f"Could not display the image automatically: {e}")


