#!/usr/bin/env python3
"""
Create a simple app icon for the Interactive Tracker.
This creates an icon using PIL (if available) or provides instructions.
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def create_icon():
    """Create a simple app icon."""
    if not PIL_AVAILABLE:
        print("PIL (Pillow) not available. To create an app icon:")
        print("1. Install Pillow: pip install Pillow")
        print("2. Run this script again")
        print("3. Or manually create an icon and place it in 'Interactive Tracker.app/Contents/Resources/icon.png'")
        return
    
    # Create a 512x512 icon (standard macOS size)
    size = 512
    img = Image.new('RGBA', (size, size), (70, 130, 180, 255))  # Steel blue background
    draw = ImageDraw.Draw(img)
    
    # Draw a simple design - a book/notebook icon
    margin = size // 8
    
    # Draw book pages (white rectangles)
    page_color = (255, 255, 255, 255)
    page1_rect = [margin, margin, size - margin - 10, size - margin]
    page2_rect = [margin + 10, margin + 10, size - margin, size - margin + 10]
    
    draw.rectangle(page2_rect, fill=(200, 200, 200, 255))  # Shadow page
    draw.rectangle(page1_rect, fill=page_color)  # Main page
    
    # Draw lines on the page
    line_color = (100, 100, 100, 255)
    line_spacing = size // 12
    for i in range(3, 8):
        y = margin + i * line_spacing
        draw.line([margin + 20, y, size - margin - 30, y], fill=line_color, width=3)
    
    # Draw a simple pen/pencil
    pen_color = (50, 50, 50, 255)
    pen_tip_color = (255, 200, 100, 255)
    
    pen_x = size - margin - 60
    pen_y = margin + 40
    pen_length = 100
    pen_width = 8
    
    # Pen body
    draw.rectangle([pen_x, pen_y, pen_x + pen_width, pen_y + pen_length], fill=pen_color)
    # Pen tip
    draw.rectangle([pen_x, pen_y + pen_length, pen_x + pen_width, pen_y + pen_length + 15], fill=pen_tip_color)
    
    # Add text "IT" for Interactive Tracker
    try:
        font_size = size // 6
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "IT"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_x = (size - text_width) // 2
    text_y = size - margin - text_height - 20
    
    # Draw text with shadow
    draw.text((text_x + 2, text_y + 2), text, fill=(0, 0, 0, 128), font=font)  # Shadow
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)  # Main text
    
    # Save the icon
    icon_path = "Interactive Tracker.app/Contents/Resources/icon.png"
    img.save(icon_path, "PNG")
    print(f"App icon created at: {icon_path}")
    
    # Also create smaller sizes for different uses
    sizes = [16, 32, 64, 128, 256, 512]
    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        resized.save(f"Interactive Tracker.app/Contents/Resources/icon_{s}.png", "PNG")
    
    print("Multiple icon sizes created for optimal display")

if __name__ == "__main__":
    create_icon()