// src/components/VideoDisplay.jsx

import React, { useState, useEffect } from 'react';

const VideoDisplay = () => {
  const [videoSrc, setVideoSrc] = useState('');

  const fetchProcessedVideo = async () => {
    try {
      const response = await fetch('/processed-video');
      if (response.ok) {
        setVideoSrc('/processed-video');
      } else {
        console.error('Failed to fetch processed video');
      }
    } catch (error) {
      console.error('Error fetching video:', error);
    }
  };

  useEffect(() => {
    fetchProcessedVideo();
  }, []); // Empty dependency array means this will run once when the component mounts

  return (
    <div>
      {videoSrc ? (
        <video width="640" height="480" controls>
          <source src={videoSrc} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      ) : (
        <p>No video available</p>
      )}
    </div>
  );
};

export default VideoDisplay;
