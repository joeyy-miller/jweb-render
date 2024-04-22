import re
from PIL import Image, ImageDraw, ImageFont

# Additional HTML elements like Header, Link, and structural elements
html_content = """
<html>
<body>
<header style='background-color: grey; text-align: center; color: white;'>Page Title</header>
<p style='background-color: lightblue; text-align: left; color: black;'>Welcome to our page!<br><br>Enjoy your stay.</p>
<div style='background-color: blue; text-align: center; color: white;'><i>Blue Box</i></div>
<a href='http://example.com' style=''>Visit Our Site</a>
</body>
</html>
"""

class HTMLElement:
    def __init__(self, tag, styles, content):
        self.tag = tag
        self.styles = self.parse_styles(styles)
        self.content = content.strip()
        self.children = []

    def parse_styles(self, style_str):
        styles = {}
        for part in style_str.split(';'):
            if ':' in part:
                key, value = part.split(':', 1)
                styles[key.strip()] = value.strip()
        return styles

    def render(self, draw, top_left, available_width):
        font = self.get_font()
        text = self.get_text()
        color = self.styles.get('background-color', 'white')
        text_color = self.styles.get('color', 'black')
        align = self.styles.get('text-align', 'left')

        # Measure text size using textbbox, starting from the provided top_left coordinate
        text_box = draw.textbbox((top_left[0], top_left[1]), text, font=font)
        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]

        # Calculate text position based on alignment
        if align == 'center':
            x = (available_width - text_width) // 2
        elif align == 'left':
            x = 0
        elif align == 'right':
            x = 800
        else:
            x = available_width - text_width

        # Draw the background rectangle and the text
        draw.rectangle([top_left[0], top_left[1], top_left[0] + available_width, top_left[1] + text_height + 20], fill=color)
        draw.text((top_left[0] + x, top_left[1]), text, font=font, fill=text_color)
        return text_height + 20

    def get_font(self):
        return ImageFont.load_default()

    def get_text(self):
        return self.content.replace('<br>', '\n')

class BoldText(HTMLElement):
    def get_font(self):
        return ImageFont.truetype("Arial Bold", 16)

    def get_text(self):
        return super().get_text().replace("<b>", "").replace("</b>", "")

class ItalicText(HTMLElement):
    def get_font(self):
        return ImageFont.truetype("Arial Italic", 16)

    def get_text(self):
        return super().get_text().replace("<i>", "").replace("</i>", "")

class Header(HTMLElement):
    def get_font(self):
        return ImageFont.truetype("Arial Bold", 24)

class Link(HTMLElement):
    def get_text(self):
        # Simulate link by underlining and changing color
        self.styles['color'] = 'blue'
        return super().get_text().replace("<a>", "").replace("</a>", "")

# Improved regex
tags = re.findall(r"<(div|p|header|body|html|a|i|b)(.*?style='(.*?)')?>(.*?)<\/(div|p|header|body|html|a|i|b)>", html_content, re.DOTALL)

img = Image.new('RGB', (800, 600), 'white')
d = ImageDraw.Draw(img)
y = 10

# Process each tag
for tag, _, styles, content, _ in tags:
    content = re.sub(r"<(\/)?(b|i)>", "", content)  # Remove inner tags from content
    if tag == "header":
        element = Header(tag, styles, content)
    elif tag == "a":
        element = Link(tag, styles, content)
    elif tag == "b":
        element = BoldText(tag, styles, content)
    elif tag == "i":
        element = ItalicText(tag, styles, content)
    else:
        element = HTMLElement(tag, styles, content)

    element_height = element.render(d, (0, y), 800)
    y += element_height + 10

img.save('enhanced_rendered_website.png')