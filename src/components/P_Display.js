import React, { useEffect, useState } from 'react';

const P_Display = () => {
  const [videoUrl, setVideoUrl] = useState(null);

  useEffect(() => {
    const checkVideoExistence = async () => {
      try {
        const response = await fetch('http://localhost:5000/video/PVideo.mp4');
        if (response.ok) {
          setVideoUrl('http://localhost:5000/video/PVideo.mp4');
        } else {
          setVideoUrl(null);
        }
      } catch (error) {
        console.error('Error checking video existence:', error);
        setVideoUrl(null);
      }
    };

    // Poll every 5 seconds
    const intervalId = setInterval(checkVideoExistence, 5000);

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  return (
    <div>
      {videoUrl ? (
        <video width="600" controls>
          <source src={videoUrl} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      ) : (
        <p>Video not available yet. Please check back later.</p>
      )}
    </div>
  );
};

export default P_Display;
