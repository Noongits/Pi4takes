
from flask import Flask, Response
import subprocess

app = Flask(__name__)

def generate_frames():
    # Start libcamera-vid and pipe the output to stdout
    command = [
        'libcamera-vid',
        '--inline',
        '--framerate', '30',
        '--width', '640',
        '--height', '480',
        '--output', '-'
    ]

    # Start the subprocess
    with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
        while True:
            # Read a frame from stdout
            frame = process.stdout.read(640 * 480 * 3)  # Adjust for RGB frames
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
    return '''
    <html>
        <head>
            <title>IP Camera Feed</title>
        </head>
        <body>
            <h1>Raspberry Pi CSI Camera Feed</h1>
            <img src="/video_feed">
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
