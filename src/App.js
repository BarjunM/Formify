import React, { useState } from 'react';
import axios from 'axios';
import './App.css';  // Ensure you have some CSS styles if needed

function App() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.message === 'File successfully uploaded and processed') {
        // Update the video URL to fetch the processed video
        setVideoUrl('http://localhost:5000/processed-video');
      }
    } catch (err) {
      console.error('Upload failed:', err.response ? err.response.data : err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="App">
      <h1>Video Upload and Processing</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? 'Uploading...' : 'Upload Video'}
      </button>
      {videoUrl && (
        <div>
          <h2>Processed Video:</h2>
          <video width="600" controls>
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
}

export default App;
