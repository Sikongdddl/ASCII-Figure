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

def get_density(color):
    r, g, b = color
    # 感知亮度（人眼模型）
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    # 颜色饱和度
    saturation = max(r, g, b) - min(r, g, b)
    # 组合指标
    perceived_intensity = (1 - luma / 255.0) * 1.1 + (saturation / 255.0) * 0.7 # 你可以自己调节权重
    return min(perceived_intensity, 1.0)

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
            density = get_density(avg_color)
            char_idx = int(density * (len(CHARSET) - 1))
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
