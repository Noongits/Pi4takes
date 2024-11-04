from flask import Flask, Response
import subprocess

app = Flask(__name__)

def generate_frames():
    # Using libcamera to capture frames
    command = ["libcamera-vid", "--width", "640", "--height", "480", "--framerate", "30", "--inline", "--output", "/dev/stdout"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        frame = process.stdout.read(640 * 480 * 3)  # Read raw RGB frame
        if not frame:
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "<h1>Raspberry Pi Camera Stream</h1><img src='/video_feed' />"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
