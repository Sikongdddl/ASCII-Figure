from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import os

# 字符集（密度从低到高）
CHARSET = list(" .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")

# 设置字体路径（使用等宽字体！）
FONT_PATH = "C:\\Windows\\Fonts\\consolab.ttf" # 替换为你的字体路径

def adjust_contrast(img, factor=1.0):
    """调整图像对比度，factor > 1.0 提高对比度"""
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)

def get_average_color(image):
    """获取图像的平均 RGB 值"""
    np_img = np.array(image)
    w, h, _ = np_img.shape
    return tuple(np_img.reshape((w * h, 3)).mean(axis=0).astype(int))

def get_density(color):
    r, g, b = color
    # 感知亮度（人眼模型）
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # 颜色饱和度
    saturation = max(r, g, b) - min(r, g, b)
    # 组合指标
    perceived_intensity = (1 - luma / 255.0) * 1.1 + (saturation / 255.0) * 0.7 # 你可以自己调节权重
    return min(perceived_intensity, 1.0)

def image_to_ascii_image(input_path, output_path="ascii_output.png", block_size=(2,4), font_size=12):
    img = Image.open(input_path).convert("RGB")
    
    # 增强对比度
    img = adjust_contrast(img, 1.0) # 你可以自己调节对比度

    width, height = img.size

    # 调整图像尺寸为 block 的倍数
    new_width = width - (width % block_size[0])
    new_height = height - (height % block_size[1])
    img = img.resize((new_width, new_height))

    cols = new_width // block_size[0]
    rows = new_height // block_size[1]

    font = ImageFont.truetype(FONT_PATH, font_size)
    canvas = Image.new("RGB", (cols * (font_size // 2), rows * font_size), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    for row in range(rows):
        for col in range(cols):
            left = col * block_size[0]
            upper = row * block_size[1]
            right = left + block_size[0]
            lower = upper + block_size[1]
            block = img.crop((left, upper, right, lower))

            avg_color = get_average_color(block)
            density = get_density(avg_color)
            char_idx = int(density * (len(CHARSET) - 1))
            char = CHARSET[char_idx]

            x = col * (font_size // 2)
            y = row * font_size
            draw.text((x, y), char, fill=avg_color, font=font)

    canvas.save(output_path)
    print(f"🎉 彩色字符画保存完成：{output_path}")

if __name__ == "__main__":
    image_path = "usage1.jpg"  # 替换为你的图片路径
    output_path = "usage1_result.png"
    image_to_ascii_image(image_path, output_path, (2,4), 12) # 你可以自己调节尺寸
