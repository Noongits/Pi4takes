from flask import Flask, send_file, jsonify
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
    
    try:
        # Run the command and wait for it to complete
        subprocess.run(command, check=True)

        # Check if the file was created
        if os.path.exists(image_filename):
            return send_file(image_filename, mimetype='image/jpeg')
        else:
            return jsonify({"error": "Image capture failed."}), 500

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to capture image.", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An error occurred.", "details": str(e)}), 500

@app.route('/')
def index():
    return "<h1>Raspberry Pi Camera</h1><p>Go to <a href='/capture'>/capture</a> to take a picture.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
