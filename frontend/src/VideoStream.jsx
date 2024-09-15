import React, { useEffect, useRef, useState } from 'react';
import './VideoStream.css'; // Import external CSS file

const VideoStream = () => {
  const imgRef = useRef(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const img = imgRef.current;
    const videoUrl = 'http://localhost:5001/video_feed';
    console.log('Attempting to load video stream from:', videoUrl);
    
    img.src = videoUrl;

    const handleLoad = () => {
      console.log('Video stream loaded successfully');
    };

    const handleError = () => {
      const errorMsg = `Failed to load video stream from ${videoUrl}`;
      setError(errorMsg);
      console.error(errorMsg);
    };

    img.addEventListener('load', handleLoad);
    img.addEventListener('error', handleError);

    return () => {
      img.removeEventListener('load', handleLoad);
      img.removeEventListener('error', handleError);
    };
  }, []);

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="video-stream-container">
      <img 
        ref={imgRef} 
        alt="Video Stream" 
        className="video-stream"
      />
    </div>
  );
};

export default VideoStream;
