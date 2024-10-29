
#################### Usage ####################
# 1. pip install bounding_box opencv-python
# 2. modify "Img_Dir" "Save_Dir" "Draw_Tags"
# 3. python main.py
#################### Usage ####################

import json
import cv2
import os
from bounding_box import bounding_box as bbox_plot

Img_Dir = r'D:/vott_label/target/vott-json-export'  # 使用原始字符串避免路径错误
Label_json = r'D:/vott_label/target/vott-json-export/video-export.json'
Save_Dir = r'D:/vott_label/results'
Draw_Tags = ['person']


def make_video(imgs_dir, img_size=(1920, 1080), fps=5):
    file_path = os.path.join(Save_Dir, "demo.mp4")
    filelist = os.listdir(imgs_dir)  # 获取该目录下的所有文件
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4v 编码格式
    video = cv2.VideoWriter(file_path, fourcc, fps, img_size)

    for item in filelist:
        if item.endswith('.jpg'):  # 判断图片后缀是否是.jpg
            item_path = os.path.join(imgs_dir, item)  # 修正为正确的路径连接方式
            img = cv2.imread(item_path)  # 使用opencv读取图像
            if img is not None:
                video.write(img)  # 把图片写进视频
            else:
                print(f"无法读取图像文件: {item_path}")

    video.release()  # 释放


def draw_one_img(img_name, img_timestamp, labels_list):
    img_path = os.path.join(Img_Dir, img_name)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    if img is None:
        print(f"无法读取图像: {img_path}")
        return

    for label in labels_list:
        tag = label['tags'][0]
        if tag not in Draw_Tags:
            continue
        bbox = label['boundingBox']
        left = bbox['left']
        top = bbox['top']
        right = left + bbox['width']
        bottom = top + bbox['height']
        bbox_plot.add(img, left, top, right, bottom, tag, 'red')

    save_name = 'time%s.jpg' % format(img_timestamp, '.2f').replace('.', '')
    save_path = os.path.join(Save_Dir, save_name)
    cv2.imwrite(save_path, img)
    print(save_name, "ok~")


def main():
    with open(Label_json, 'r', encoding='utf-8') as f:  # 加载JSON文件时指定编码
        labels_dict = json.load(f)

    assets = labels_dict['assets']
    size = None

    for k, v in assets.items():
        img_name = v['asset']['name']
        img_timestamp = v['asset']['timestamp']
        if size is None:
            w = v['asset']['size']['width']
            h = v['asset']['size']['height']
            size = (w, h)

        labels_list = v['regions']
        draw_one_img(img_name, img_timestamp, labels_list)

    make_video(Save_Dir, img_size=size)


if __name__ == '__main__':
    main()
