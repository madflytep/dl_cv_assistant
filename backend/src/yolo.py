import json
import logging
import time

import cv2
import numpy
import torch
from ultralytics import YOLO

logging.getLogger("ultralytics").setLevel(logging.ERROR)

model = YOLO("storage/weights/120_epochs.pt")
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model.to(device)

with open("storage/maps/our_signs_map.json") as json_file:
    signs_map = json.load(json_file)
with open("storage/maps/text_info_mapping.json") as json_file:
    text_info_map = json.load(json_file)
with open("storage/maps/high_priority_mapping.json") as json_file:
    priority_map = json.load(json_file)


def _predict_img(img: numpy.ndarray):
    result = model(img, conf=0.5, imgsz=1280, device=device)
    return result[0]


def priority_flag(sign_name: str) -> int:
    if sign_name in priority_map.keys():
        return 1
    else:
        return 0


async def predict_video(
    input_video_path: str, out_video_path: str, logs_file, frames_in_row: int = 10, frame_slip: int = 5
):
    time_start = time.time()

    cap = cv2.VideoCapture(input_video_path)

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    video_shape = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*"vp80"), video_fps, video_shape)

    frame_count = 0
    detected_signs = {}
    shown_signs = {}

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        res = _predict_img(frame)
        out.write(res.plot())

        names = []
        detection_count = res.boxes.shape[0]
        for i in range(detection_count):
            cls = int(res.boxes.cls[i].item())
            names.append(res.names[cls])

        del_keys = set(detected_signs) - set(names)
        for del_key in del_keys:
            if del_key in shown_signs:
                shown_signs[del_key] += 1
            else:
                shown_signs[del_key] = 1

            if shown_signs[del_key] > frame_slip:
                del detected_signs[del_key]
                del shown_signs[del_key]

        for name in names:
            if name in detected_signs:
                detected_signs[name] += 1
            else:
                detected_signs[name] = 1

            shown_signs.pop(name, None)

            if detected_signs[name] == frames_in_row:
                if name in signs_map and name in text_info_map:
                    await logs_file.write(
                        f"{round(frame_count / video_fps, 2)},{name},{signs_map[name]},"
                        f"{text_info_map[name]},{priority_flag(name)}\n"
                    )

    cap.release()

    print("Task completed")
    print(f"Video duration: {frame_count / video_fps} seconds")
    print(f"FPS: {video_fps}")
    print(f"Task completion time: {time.time() - time_start} seconds")
    print("--------------------------------------------------")
