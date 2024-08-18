from flask import Flask, request, jsonify, send_from_directory, abort
import os
from werkzeug.utils import secure_filename
from AiTrainer import main as process_video  # Import the main function from AiTrainer

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSING_FOLDER = 'backend/processedREAL'  # Folder where processed video is stored
ALLOWED_EXTENSIONS = {'mp4'}
VIDEO_FOLDER = os.path.join(os.path.dirname(__file__), 'backend', 'processedREAL')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSING_FOLDER'] = PROCESSING_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'video.mp4')
        file.save(filepath)

        # Check if the file was successfully saved
        if os.path.exists(filepath):
            # Process the video
            process_video(filepath)  # Call the main function from AiTrainer with the correct path
            
            return jsonify({'message': 'File successfully uploaded and processed'}), 200
        else:
            return jsonify({'error': 'Failed to save file'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/video/<filename>')
def serve_video(filename):
    try:
        return send_from_directory(VIDEO_FOLDER, filename)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    # Ensure the existing folders exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['PROCESSING_FOLDER']):
        os.makedirs(app.config['PROCESSING_FOLDER'])
    app.run(debug=True)