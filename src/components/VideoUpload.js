// src/components/VideoUpload.jsx

import React from 'react';

const VideoUpload = ({ onUpload }) => {
  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      if (response.ok) {
        onUpload(); // Notify parent to update display
      } else {
        console.error(data.error);
      }
    } catch (error) {
      console.error('Error uploading video:', error);
    }
  };

  return (
    <div>
      <input type="file" accept="video/mp4" onChange={handleFileChange} />
    </div>
  );
};

export default VideoUpload;
