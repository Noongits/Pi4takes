
from flask import Flask, Response
from picamera import PiCamera
import time

app = Flask(__name__)

# Initialize the camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
time.sleep(2)  # Allow the camera to warm up

def generate_frames():
    while True:
        # Capture frames from the camera
        frame = camera.capture_continuous('frame.jpg', format='jpeg', use_video_port=True)
        with open('frame.jpg', 'rb') as f:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + f.read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>Raspberry Pi Camera Stream</title>
        </head>
        <body>
            <h1>Raspberry Pi Camera Stream</h1>
            <img src="{{ url_for('video_feed') }}">
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
