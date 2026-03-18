# # import cv2
# # import os
# # import requests
# # from datetime import datetime
# # from ultralytics import YOLO
# # from playsound import playsound
# # import threading
# #
# # # Load YOLOv8 model
# # model = YOLO(r"E:\firesmokemes based 16-1-26\firesmokemes based\runs\detect\yolov8_mes_fire_smoke\weights\best.pt")
# #
# # # Video path (using webcam 0)
# # cap = cv2.VideoCapture(0)
# #
# # # Video writer setup
# # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# # fps = cap.get(cv2.CAP_PROP_FPS)
# # out = cv2.VideoWriter('output_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
# #
# # # Folder to save frames
# # frame_folder = r"E:\Fasna's Wedding\Edited\firesmoke mea\firesmoke mea\fireandsmoke web\fireandsmoke\media\det\detected_frames"
# # os.makedirs(frame_folder, exist_ok=True)
# #
# # # Django backend endpoint
# # DJANGO_UPLOAD_URL = "http://127.0.0.1:8000/myapp/upload_detection/"
# #
# # # Alarm configuration
# # ALERT_SOUND = r"E:\Fasna's Wedding\Edited\firesmoke mea\firesmoke mea\fireandsmoke web\fireandsmoke\myapp\static\alarm.wav"
# # alarm_thread = None
# # alarm_running = False
# # stop_alarm_flag = False
# #
# # def play_alarm_loop():
# #     global stop_alarm_flag
# #     while not stop_alarm_flag:
# #         try:
# #             playsound(ALERT_SOUND)
# #         except Exception as e:
# #             print(f"Alarm error: {e}")
# #             break
# #
# # # Track last detected labels to avoid repeated alarms/uploads
# # last_detected_labels = set()
# #
# # while cap.isOpened():
# #     ret, frame = cap.read()
# #     if not ret:
# #         break
# #
# #     # Predict with YOLO model
# #     results = model.predict(source=frame, conf=0.25, save=False, show=False)
# #     result = results[0]
# #     high_conf_labels = set()
# #
# #     for box in result.boxes:
# #         x1, y1, x2, y2 = map(int, box.xyxy[0])
# #         cls_id = int(box.cls[0])
# #         conf = float(box.conf[0])
# #         label_name = model.model.names[cls_id].lower()
# #
# #         # Act on fire/smoke/spark with confidence ≥ 0.5
# #         if label_name in ["fire", "smoke"] and conf >= 0.5:
# #             high_conf_labels.add(label_name)
# #
# #         # Draw detection for visualization
# #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
# #         cv2.putText(frame, f"{label_name} {conf:.2f}", (x1, y1 - 10),
# #                     cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
# #
# #     # === Detection trigger ===
# #     if high_conf_labels and high_conf_labels != last_detected_labels:
# #         detection_type = "_".join(sorted(high_conf_labels))  # e.g., fire_smoke, fire_spark, etc.
# #         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
# #         filename = f"detected_{timestamp}.jpg"
# #         filepath = os.path.join(frame_folder, filename)
# #         cv2.imwrite(filepath, frame)
# #
# #         print(f"[DETECTED] {detection_type.upper()} (conf ≥ 0.5) - Sending to Django")
# #
# #         data = {
# #             'label': detection_type,
# #             'image': "/media/det/detected_frames/" + filename
# #         }
# #         try:
# #             response = requests.post(DJANGO_UPLOAD_URL, data=data)
# #             if response.status_code == 200:
# #                 print("✅ Sent to Django successfully")
# #             else:
# #                 print(f"❌ Failed to send: {response.status_code} - {response.text}")
# #         except Exception as e:
# #             print(f"❌ Django POST error: {e}")
# #
# #     # === Alarm control ===
# #     if high_conf_labels:
# #         if not alarm_running:
# #             print("🔊 Starting alarm...")
# #             stop_alarm_flag = False
# #             alarm_thread = threading.Thread(target=play_alarm_loop, daemon=True)
# #             alarm_thread.start()
# #             alarm_running = True
# #     else:
# #         if alarm_running:
# #             print("🔇 Stopping alarm...")
# #             stop_alarm_flag = True
# #             alarm_thread.join(timeout=2)
# #             alarm_running = False
# #
# #     last_detected_labels = high_conf_labels
# #     out.write(frame)
# #     cv2.imshow("Detection", frame)
# #
# #     # Exit on 'q' key
# #     if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
# #         break
# #
# # # Cleanup
# # cap.release()
# # out.release()
# # cv2.destroyAllWindows()
# #
# # # Stop alarm if still running
# #
# # if alarm_running:
# #     stop_alarm_flag = True
# #     alarm_thread.join(timeout=2)
# # import cv2
# # import os
# # import requests
# # from datetime import datetime
# # from ultralytics import YOLO
# # import pygame
# #
# # # ===================== PYGAME AUDIO =====================
# # pygame.mixer.init()
# #
# # NORMAL_ALERT_SOUND = r"E:\Fasna's Wedding\Edited\firesmoke mea\firesmoke mea\fireandsmoke web\fireandsmoke\myapp\static\alarm.wav"
# # FAST_ALERT_SOUND = r"E:\Fasna's Wedding\Edited\firesmoke mea\firesmoke mea\fireandsmoke web\fireandsmoke\myapp\static\alarm_fast.wav"
# #
# # normal_alarm = pygame.mixer.Sound(NORMAL_ALERT_SOUND)
# # fast_alarm = pygame.mixer.Sound(FAST_ALERT_SOUND)
# #
# # current_alarm_type = None  # "normal" | "fast"
# #
# # def play_alarm(alarm_type):
# #     global current_alarm_type
# #     if current_alarm_type != alarm_type:
# #         pygame.mixer.stop()
# #         if alarm_type == "fast":
# #             fast_alarm.play(loops=-1)
# #         else:
# #             normal_alarm.play(loops=-1)
# #         current_alarm_type = alarm_type
# #
# # def stop_alarm():
# #     global current_alarm_type
# #     pygame.mixer.stop()
# #     current_alarm_type = None
# #
# #
# # # ===================== FACE DETECTION =====================
# # face_cascade = cv2.CascadeClassifier(
# #     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# # )
# #
# # def detect_faces(frame):
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# #     return face_cascade.detectMultiScale(
# #         gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
# #     )
# #
# #
# # def is_overlap(box1, box2):
# #     x1, y1, x2, y2 = box1
# #     a1, b1, a2, b2 = box2
# #     return x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1
# #
# #
# # # ===================== MODELS =====================
# # # Fire & Smoke (your trained model)
# # fire_model = YOLO(
# #     r"E:\firesmokemes based 16-1-26\firesmokemes based\runs\detect\yolov8_mes_fire_smoke\weights\best.pt"
# # )
# #
# # # Electronics detection (COCO)
# # device_model = YOLO("yolov8n.pt")
# # SCREEN_CLASSES = {"cell phone", "laptop", "tv", "monitor"}
# #
# #
# # # ===================== VIDEO =====================
# # cap = cv2.VideoCapture(0)
# #
# # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# # fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
# #
# # out = cv2.VideoWriter(
# #     "output_video.mp4",
# #     cv2.VideoWriter_fourcc(*"mp4v"),
# #     fps,
# #     (width, height)
# # )
# #
# # frame_area = width * height
# # FAST_BOX_RATIO = 0.15
# #
# #
# # # ===================== SAVE FRAMES =====================
# # frame_folder = r"E:\Fasna's Wedding\Edited\firesmoke mea\firesmoke mea\fireandsmoke web\fireandsmoke\media\det\detected_frames"
# # os.makedirs(frame_folder, exist_ok=True)
# #
# # DJANGO_UPLOAD_URL = "http://127.0.0.1:8000/myapp/upload_detection/"
# #
# #
# # last_detected_labels = set()
# #
# #
# # # ===================== MAIN LOOP =====================
# # while cap.isOpened():
# #     ret, frame = cap.read()
# #     if not ret:
# #         break
# #
# #     # -------- FACE DETECTION --------
# #     faces = detect_faces(frame)
# #
# #     # -------- SCREEN DETECTION --------
# #     screen_boxes = []
# #     device_results = device_model.predict(frame, conf=0.4, save=False, show=False)[0]
# #
# #     for box in device_results.boxes:
# #         label = device_model.model.names[int(box.cls[0])].lower()
# #         if label in SCREEN_CLASSES:
# #             x1, y1, x2, y2 = map(int, box.xyxy[0])
# #             screen_boxes.append((x1, y1, x2, y2))
# #
# #             # cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
# #             # cv2.putText(frame, label, (x1, y1 - 8),
# #             #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
# #
# #     # -------- FIRE & SMOKE DETECTION --------
# #     results = fire_model.predict(frame, conf=0.25, save=False, show=False)[0]
# #
# #     detected_labels = set()
# #     largest_box_area = 0
# #
# #     for box in results.boxes:
# #         x1, y1, x2, y2 = map(int, box.xyxy[0])
# #         conf = float(box.conf[0])
# #         label = fire_model.model.names[int(box.cls[0])].lower()
# #
# #         box_area = (x2 - x1) * (y2 - y1)
# #         largest_box_area = max(largest_box_area, box_area)
# #
# #         # Face overlap
# #         if any(is_overlap((x1, y1, x2, y2),
# #                           (fx, fy, fx + fw, fy + fh)) for (fx, fy, fw, fh) in faces):
# #             continue
# #
# #         # Screen overlap (IGNORE FIRE)
# #         if label == "fire":
# #             if any(is_overlap((x1, y1, x2, y2), sb) for sb in screen_boxes):
# #                 print("⚠ Fire ignored (screen content)")
# #                 continue
# #             detected_labels.add("fire")
# #
# #
# #         elif label == "smoke" and conf >= 0.6:
# #             detected_labels.add("smoke")
# #
# #         else:
# #             continue
# #
# #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
# #         cv2.putText(frame, f"{label} {conf:.2f}",
# #                     (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.6, (0, 255, 0), 2)
# #
# #
# #     # -------- SAVE & SEND --------
# #     if detected_labels and detected_labels != last_detected_labels:
# #         ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
# #         filename = f"detected_{ts}.jpg"
# #         filepath = os.path.join(frame_folder, filename)
# #         cv2.imwrite(filepath, frame)
# #
# #         try:
# #             requests.post(DJANGO_UPLOAD_URL, data={
# #                 "label": "_".join(sorted(detected_labels)),
# #                 "image": "/media/det/detected_frames/" + filename
# #             }, timeout=2)
# #         except:
# #             pass
# #
# #     # -------- ALARM --------
# #     if detected_labels:
# #         ratio = largest_box_area / frame_area
# #         play_alarm("fast" if ratio >= FAST_BOX_RATIO else "normal")
# #     else:
# #         if current_alarm_type:
# #             stop_alarm()
# #
# #     last_detected_labels = detected_labels
# #
# #     out.write(frame)
# #     cv2.imshow("Fire & Smoke Detection (Screen Safe)", frame)
# #
# #     if cv2.waitKey(1) & 0xFF == ord("q"):
# #         break
# #
# #
# # # ===================== CLEANUP =====================
# # cap.release()
# # out.release()
# # cv2.destroyAllWindows()
# # stop_alarm()
# # pygame.mixer.quit()
# #
#
# import cv2
# import os
# import requests
# import time
# from datetime import datetime
# from ultralytics import YOLO
# import pygame
#
# # ===================== PYGAME AUDIO =====================
# pygame.mixer.init()
#
# NORMAL_ALERT_SOUND = r"E:\Fasna's Wedding\Edited\firesmoke mea\firesmoke mea\fireandsmoke web\fireandsmoke\myapp\static\alarm.wav"
# FAST_ALERT_SOUND = r"E:\Fasna's Wedding\Edited\firesmoke mea\firesmoke mea\fireandsmoke web\fireandsmoke\myapp\static\alarm_fast.wav"
#
# normal_alarm = pygame.mixer.Sound(NORMAL_ALERT_SOUND)
# fast_alarm = pygame.mixer.Sound(FAST_ALERT_SOUND)
#
# current_alarm_type = None  # None | "normal" | "fast"
#
# # 🔑 Alarm persistence
# ALARM_HOLD_TIME = 1.5  # seconds
# last_detection_time = 0
#
#
# def play_alarm(alarm_type):
#     global current_alarm_type
#     if current_alarm_type == alarm_type:
#         return  # already playing
#     pygame.mixer.stop()
#     if alarm_type == "fast":
#         fast_alarm.play(loops=-1)
#     else:
#         normal_alarm.play(loops=-1)
#     current_alarm_type = alarm_type
#
#
# def stop_alarm():
#     global current_alarm_type
#     pygame.mixer.stop()
#     current_alarm_type = None
#
#
# # ===================== FACE DETECTION =====================
# face_cascade = cv2.CascadeClassifier(
#     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
# )
#
#
# def detect_faces(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     return face_cascade.detectMultiScale(
#         gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
#     )
#
#
# def is_overlap(box1, box2):
#     x1, y1, x2, y2 = box1
#     a1, b1, a2, b2 = box2
#     return x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1
#
# def pred(rid,floor):
#
#
#     # ===================== MODELS =====================
#     fire_model = YOLO(
#         r"E:\firesmokemes based 16-1-26\firesmokemes based\runs\detect\yolov8_mes_fire_smoke\weights\best.pt"
#     )
#
#     device_model = YOLO("yolov8m.pt")
#     SCREEN_CLASSES = {"cell phone", "laptop", "tv", "monitor"}
#
#
#     # ===================== VIDEO =====================
#     cap = cv2.VideoCapture(0)
#
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
#
#     out = cv2.VideoWriter(
#         "output_video.mp4",
#         cv2.VideoWriter_fourcc(*"mp4v"),
#         fps,
#         (width, height)
#     )
#
#     frame_area = width * height
#     FAST_BOX_RATIO = 0.15
#
#
#     # ===================== SAVE FRAMES =====================
#     frame_folder = r"E:\Fasna's Wedding\Edited\firesmoke mea\firesmoke mea\fireandsmoke web\fireandsmoke\media\det\detected_frames"
#     os.makedirs(frame_folder, exist_ok=True)
#
#     DJANGO_UPLOAD_URL = "http://127.0.0.1:8000/myapp/upload_detection/"
#
#     last_detected_labels = set()
#
#
#     # ===================== MAIN LOOP =====================
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         frame = cv2.flip(frame, 1)
#         current_time = time.time()
#
#         # -------- FACE DETECTION --------
#         faces = detect_faces(frame)
#
#         # -------- SCREEN DETECTION --------
#         screen_boxes = []
#         device_results = device_model.predict(frame, conf=0.4, save=False, show=False)[0]
#
#         for box in device_results.boxes:
#             label = device_model.model.names[int(box.cls[0])].lower()
#             if label in SCREEN_CLASSES:
#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 screen_boxes.append((x1, y1, x2, y2))
#
#         # -------- FIRE & SMOKE DETECTION --------
#         results = fire_model.predict(frame, conf=0.25, save=False, show=False)[0]
#
#         detected_labels = set()
#         largest_box_area = 0
#
#         for box in results.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             conf = float(box.conf[0])
#             label = fire_model.model.names[int(box.cls[0])].lower()
#
#             box_area = (x2 - x1) * (y2 - y1)
#             largest_box_area = max(largest_box_area, box_area)
#
#             # Ignore face overlap
#             if any(is_overlap((x1, y1, x2, y2),
#                               (fx, fy, fx + fw, fy + fh)) for (fx, fy, fw, fh) in faces):
#                 continue
#
#             # Ignore screen fire
#             if label == "fire":
#                 if any(is_overlap((x1, y1, x2, y2), sb) for sb in screen_boxes):
#                     continue
#                 detected_labels.add("fire")
#
#             elif label == "smoke" and conf >= 0.6:
#                 detected_labels.add("smoke")
#
#             else:
#                 continue
#
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.putText(frame, f"{label} {conf:.2f}",
#                         (x1, y1 - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#
#         # -------- SAVE & SEND --------
#         if detected_labels and detected_labels != last_detected_labels:
#             ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
#             filename = f"detected_{ts}.jpg"
#             filepath = os.path.join(frame_folder, filename)
#             cv2.imwrite(filepath, frame)
#
#             try:
#                 requests.post(DJANGO_UPLOAD_URL, data={
#                     "label": "_".join(sorted(detected_labels)),
#                     "rid":rid,
#                     "floor":floor,
#                     "image": "/media/det/detected_frames/" + filename
#                 }, timeout=2)
#             except:
#                 pass
#
#         # -------- ALARM (FIXED) --------
#         if detected_labels:
#             last_detection_time = current_time
#             ratio = largest_box_area / frame_area
#             play_alarm("fast" if ratio >= FAST_BOX_RATIO else "normal")
#         else:
#             if current_alarm_type and (current_time - last_detection_time) > ALARM_HOLD_TIME:
#                 stop_alarm()
#
#         last_detected_labels = detected_labels
#
#         out.write(frame)
#         cv2.imshow("Fire & Smoke Detection (Screen Safe)", frame)
#
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#
#
#     # ===================== CLEANUP =====================
#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()
#     stop_alarm()
#     pygame.mixer.quit()
#

import cv2
import os
import requests
import time
from datetime import datetime
from ultralytics import YOLO
import pygame
import sys

# ===================== ARGS =====================
lid = sys.argv[1]
floor = sys.argv[2]

# ===================== AUDIO =====================
pygame.mixer.init()

NORMAL_ALERT_SOUND = r"C:\Users\najum\PycharmProjects\yoloearlyhomefiredetection\myapp\static\alarm.wav"
FAST_ALERT_SOUND = r"C:\Users\najum\PycharmProjects\yoloearlyhomefiredetection\myapp\static\alarm_fast.wav"

normal_alarm = pygame.mixer.Sound(NORMAL_ALERT_SOUND)
fast_alarm = pygame.mixer.Sound(FAST_ALERT_SOUND)

current_alarm_type = None
last_detection_time = 0

ALARM_HOLD_TIME = 1.5
FAST_BOX_RATIO = 0.15

# ===================== MODELS =====================
fire_model = YOLO(r"C:\Users\najum\PycharmProjects\yoloearlyhomefiredetection\myapp\runs\detect\yolov8_fire_smoke\weights\best.pt")
device_model = YOLO("yolov8m.pt")
SCREEN_CLASSES = {"cell phone", "laptop", "tv", "monitor"}

# ===================== FACE =====================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ===================== HELPERS =====================
def play_alarm(t):
    global current_alarm_type
    if current_alarm_type == t:
        return
    pygame.mixer.stop()
    (fast_alarm if t == "fast" else normal_alarm).play(loops=-1)
    current_alarm_type = t


def stop_alarm():
    global current_alarm_type
    pygame.mixer.stop()
    current_alarm_type = None


def detect_faces(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))


def is_overlap(a, b):
    x1,y1,x2,y2 = a
    a1,b1,a2,b2 = b
    return x1<a2 and x2>a1 and y1<b2 and y2>b1

# ===================== MAIN =====================
cap = cv2.VideoCapture(0)

width = int(cap.get(3))
height = int(cap.get(4))
frame_area = width * height

frame_folder = r"C:\Users\najum\PycharmProjects\yoloearlyhomefiredetection\media\det\detected_frames"
os.makedirs(frame_folder, exist_ok=True)

UPLOAD_URL = "http://127.0.0.1:8000/myapp/upload_detection/"
last_labels = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    now = time.time()

    faces = detect_faces(frame)

    # ---------- SCREEN ----------
    screen_boxes = []
    dev_res = device_model.predict(frame, conf=0.4, verbose=False)[0]
    for box in dev_res.boxes:
        lbl = device_model.model.names[int(box.cls[0])].lower()
        if lbl in SCREEN_CLASSES:
            screen_boxes.append(tuple(map(int, box.xyxy[0])))

    # ---------- FIRE & SMOKE ----------
    res = fire_model.predict(frame, conf=0.25, verbose=False)[0]

    labels = set()
    max_area = 0

    for box in res.boxes:
        x1,y1,x2,y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        lbl = fire_model.model.names[int(box.cls[0])].lower()

        area = (x2-x1)*(y2-y1)
        max_area = max(max_area, area)

        if any(is_overlap((x1,y1,x2,y2),(fx,fy,fx+fw,fy+fh)) for fx,fy,fw,fh in faces):
            continue

        if lbl == "fire" and conf >= 0.4 and not any(is_overlap((x1,y1,x2,y2),sb) for sb in screen_boxes):
            labels.add("fire")

        if lbl == "smoke" and conf >= 0.8:
            labels.add("smoke")

        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

    # ---------- SAVE & SEND ----------
    if labels and labels != last_labels:
        name = f"det_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.jpg"
        cv2.imwrite(os.path.join(frame_folder,name), frame)

        try:
            requests.post(UPLOAD_URL, data={
                "label":"_".join(labels),
                "lid":lid,
                "image":"/media/det/detected_frames/"+name
            }, timeout=2)
        except:
            pass

    # ---------- ALARM ----------
    if labels:
        last_detection_time = now
        play_alarm("fast" if max_area/frame_area >= FAST_BOX_RATIO else "normal")
    else:
        if current_alarm_type and now-last_detection_time > ALARM_HOLD_TIME:
            stop_alarm()

    last_labels = labels
    cv2.imshow("Fire & Smoke Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
stop_alarm()
pygame.mixer.quit()
