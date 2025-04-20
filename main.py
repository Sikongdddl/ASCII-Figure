import cv2
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
import os
import time

# 字符集（亮度从低到高）
CHARSET = list(" .'`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$")

# 设置字体路径（使用等宽字体！）
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"  # macOS 默认等宽字体
FONT_SIZE = 12
BLOCK_SIZE = (24,24)
def get_average_color(image):
    """获取图像的平均 RGB 值"""
    np_img = np.array(image)
    w, h, _ = np_img.shape
    return tuple(np_img.reshape((w * h, 3)).mean(axis=0).astype(int))

def get_brightness(color):
    """获取颜色亮度（可以加大对比度）"""
    r, g, b = color
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    return min(255, brightness*3)  # 增强亮度对比度

def frame_to_ascii_image(frame, font, block_size=BLOCK_SIZE):
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    width, height = img.size
    new_width = width - (width % block_size[0])
    new_height = height - (height % block_size[1])
    img = img.resize((new_width, new_height))

    cols = new_width // block_size[0]
    rows = new_height // block_size[1]

    canvas = Image.new("RGB", (cols * FONT_SIZE, rows * FONT_SIZE), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    for row in range(rows):
        for col in range(cols):
            left = col * block_size[0]
            upper = row * block_size[1]
            right = left + block_size[0]
            lower = upper + block_size[1]
            block = img.crop((left, upper, right, lower))

            avg_color = get_average_color(block)
            brightness = get_brightness(avg_color)
            char_idx = int((brightness / 255) * (len(CHARSET) - 1))
            char = CHARSET[char_idx]

            x = col * FONT_SIZE
            y = row * FONT_SIZE
            draw.text((x, y), char, fill=avg_color, font=font)

    return cv2.cvtColor(np.array(canvas), cv2.COLOR_RGB2BGR)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = frame_to_ascii_image(frame, font)
        cv2.imshow("🎨 ASCII Camera", ascii_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
