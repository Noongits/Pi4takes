from flask import Flask, Response
import cv2

app = Flask(__name__)

# Initialize the camera using libcamera
def generate_frames():
    # Start the video stream using libcamera
    cap = cv2.VideoCapture("libcamera-vid -t 0 --inline --width 640 --height 480 --framerate 30 --codec h264 --output - | ffmpeg -i pipe:0 -f mjpeg -")

    while True:
        # Read the frame from the video capture
        success, frame = cap.read()
        if not success:
            break
        else:
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Yield the frame in the appropriate format
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
                <title>IP Camera Stream</title>
            </head>
            <body>
                <h1>Raspberry Pi Camera Stream</h1>
                <img src="/video_feed">
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
