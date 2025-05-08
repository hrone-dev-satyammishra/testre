from flask import Flask, Response, jsonify, request
import cv2
from ultralytics import YOLO
from flask_cors import CORS
import mediapipe as mp
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Initialize models only when needed, not on module load
model = None
face_mesh = None
warning_messages = []
inference_running = True

def initialize_models():
    global model, face_mesh
    if model is None:
        model = YOLO('yolov8n.pt')
    if face_mesh is None:
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

def is_looking_straight(landmarks, frame_width, frame_height):
    nose_tip = landmarks[1]
    left_eye = landmarks[33]
    right_eye = landmarks[263]
    nose_x = int(nose_tip.x * frame_width)
    left_eye_x = int(left_eye.x * frame_width)
    right_eye_x = int(right_eye.x * frame_width)
    face_center = (left_eye_x + right_eye_x) / 2
    deviation = abs(nose_x - face_center)
    return deviation < 20

def gen_frames():
    global warning_messages, inference_running
    initialize_models()
    
    cap = cv2.VideoCapture(0)
    
    while inference_running:
        success, frame = cap.read()
        if not success:
            break
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = model(frame)[0]
        face_results = face_mesh.process(frame_rgb)
        
        boxes = results.boxes
        person_count = 0
        cheating = False
        messages = []
        h, w = frame.shape[:2]
        
        for box in boxes:
            cls_id = int(box.cls[0].item())
            label = results.names[cls_id]
            
            if label in ["person", "cell phone"]:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                color = (0, 255, 0) if label == "person" else (0, 0, 255)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                if label == "person":
                    person_count += 1
                if label == "cell phone":
                    cheating = True
                    
        if person_count > 1:
            messages.append("⚠️ Multiple people detected")
        if cheating:
            messages.append("📱 Cell phone detected")
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                if not is_looking_straight(face_landmarks.landmark, w, h):
                    messages.append("👀 Not looking at screen")
        
        warning_messages = messages
        
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()
    print("🔴 Inference stopped and camera released.")

@app.route('/api/video_feed')
def video_feed():
    global inference_running
    inference_running = True  # Allow restart if stopped
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/warnings')
def get_warnings():
    return jsonify({'warnings': warning_messages})

@app.route('/api/stop')
def stop_inference():
    global inference_running
    inference_running = False
    return jsonify({'message': '🛑 Inference stopped and resources released.'})

# Simple health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({'status': 'ok'})

# For Vercel serverless function handler
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return jsonify({'status': 'API is running', 'path': path})

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000) 