from flask import Flask, send_file
import subprocess
import os

app = Flask(__name__)

@app.route('/capture')
def capture_image():
    # Define the image filename
    image_filename = 'captured_image.jpg'
    
    # Capture the image using libcamera-still
    command = [
        "libcamera-still",
        "-o", image_filename,  # Output to a file
        "--width", "640",
        "--height", "480",
        "--quiet"  # Suppress output
    ]
    
    # Run the command
    subprocess.run(command)
    
    # Send the image file as response
    return send_file(image_filename, mimetype='image/jpeg')

@app.route('/')
def index():
    return "<h1>Raspberry Pi Camera</h1><p>Go to <a href='/capture'>/capture</a> to take a picture.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
