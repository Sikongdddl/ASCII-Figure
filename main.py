from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 字符集合（从复杂到简单）
CHARACTER_SET = list(" .`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")

# 字体设置（你可以改成自己的字体路径）
FONT_SIZE = 10
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"

# 生成每个字符的灰度图模板
def generate_char_templates(font_size=FONT_SIZE, image_size=(1, 2)):
    templates = {}
    font = ImageFont.truetype(FONT_PATH, font_size)
    for char in CHARACTER_SET:
        img = Image.new('L', image_size, color=255)
        draw = ImageDraw.Draw(img)
        bbox = draw.textbbox((0, 0), char, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((image_size[0] - w) // 2 - bbox[0], (image_size[1] - h) // 2 - bbox[1]),
            char,
            font=font,
            fill=0
        )
        templates[char] = np.array(img, dtype=np.float32)

    return templates

# 块与模板图像的相似度（均方误差）
def best_match(block, templates):
    block = block.astype(np.float32)
    best_char = ' '
    min_diff = float('inf')
    for char, tmpl in templates.items():
        diff = np.mean((block - tmpl) ** 2)
        if diff < min_diff:
            min_diff = diff
            best_char = char
    return best_char

# 主函数：结构匹配 ASCII 画生成
def image_to_structured_ascii(image_path, block_size=(2, 2)):
    image = Image.open(image_path).convert('L')
    width, height = image.size

    # 对图像缩放，使其适配 block 尺寸
    new_width = width - (width % block_size[0])
    new_height = height - (height % block_size[1])
    image = image.resize((new_width, new_height))
    image_data = np.array(image)

    # 生成字符模板
    templates = generate_char_templates(image_size=block_size)

    ascii_result = ""
    for y in range(0, new_height, block_size[1]):
        for x in range(0, new_width, block_size[0]):
            block = image_data[y:y+block_size[1], x:x+block_size[0]]
            char = best_match(block, templates)
            ascii_result += char
        ascii_result += '\n'
    return ascii_result

# 示例运行
if __name__ == "__main__":
    path = "usage1.jpg"
    ascii_img = image_to_structured_ascii(path, (7, 14))
    print("\n====== 输出结果 ======\n")
    print(ascii_img)
