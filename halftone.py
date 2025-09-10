from PIL import Image, ImageDraw
import numpy as np

def halftone_color_enhanced(image_path, output_path, cell_size=8, shape="circle", gamma=0.8, border=False):
    """
    Enhanced halftone effect with color preservation & contrast boost.

    Parameters:
        image_path (str): Input image path
        output_path (str): Output image path
        cell_size (int): Grid size (smaller = more detail)
        shape (str): "circle" or "diamond"
        gamma (float): Contrast/gamma correction
        border (bool): Draw black border around dots
    """
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    pixels = np.array(img, dtype=np.float32) / 255.0  # normalize [0,1]

    # Gamma correction
    pixels = np.power(pixels, gamma)

    halftone_img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(halftone_img)

    for y in range(0, height, cell_size):
        for x in range(0, width, cell_size):
            cell = pixels[y:y+cell_size, x:x+cell_size]
            if cell.size == 0:
                continue

            # Median color (keeps vibrancy)
            avg_color = tuple((np.median(cell.reshape(-1, 3), axis=0) * 255).astype(int))

            # Perceived brightness
            brightness = np.mean(avg_color) / 255.0

            # Non-linear radius mapping (more balanced dots)
            radius = int((1 - brightness**1.5) * (cell_size // 2))

            cx, cy = x + cell_size // 2, y + cell_size // 2

            if radius > 0:
                if shape == "circle":
                    bbox = (cx-radius, cy-radius, cx+radius, cy+radius)
                    if border:
                        draw.ellipse(bbox, fill=avg_color, outline="black", width=1)
                    else:
                        draw.ellipse(bbox, fill=avg_color)

                elif shape == "diamond":
                    pts = [(cx, cy-radius),
                           (cx+radius, cy),
                           (cx, cy+radius),
                           (cx-radius, cy)]
                    if border:
                        draw.polygon(pts, fill=avg_color, outline="black")
                    else:
                        draw.polygon(pts, fill=avg_color)

    halftone_img.save(output_path)
    halftone_img.show()


# Example usage
halftone_color_enhanced("edit/1.png", "halftone_enhanced.png", cell_size=6, shape="circle", gamma=0.7, border=True)
