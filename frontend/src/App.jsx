
import VideoStream from './VideoStream';
import React, { useState, useEffect } from 'react';
import axios from 'axios'; 

const DisplayBox = () => {
  const [logs, setLogs] = useState([]);
  const [toolCounts, setToolCounts] = useState({
    toolsInField: 0,
    toolsInUse: 0,
    toolsDiscarded: 0,
  });

  // Fetch logs and tool counts from the backend
  useEffect(() => {
    const fetchData = async () => {
      try {
        const logsResponse = await axios.get('http://localhost:5001/logs');
        setLogs(logsResponse.data);

        // Fetch tool counts
        const countsResponse = await axios.get('http://localhost:5001/tool_counts');
        setToolCounts(countsResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    // Set an interval to fetch data every 2 seconds (for live updates)
    const intervalId = setInterval(fetchData, 20);

    // Clear interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="bg-white rounded-lg p-4 shadow-md h-full">
      <h2 className="text-lg font-bold mb-4">Item Location</h2>
      <div className="grid grid-cols-3 gap-4 h-40">
        <div className="bg-gray-100 rounded p-2">
          <h3 className="font-semibold mb-2">Operation:</h3>
          <p>Tools in Field: {toolCounts.toolsInField}</p>
        </div>
        <div className="bg-gray-100 rounded p-2">
          <h3 className="font-semibold mb-2">Tools:</h3>
          
          <p>Tools in Use: {toolCounts.toolsInUse}</p>
          
        </div>
        <div className="bg-gray-100 rounded p-2">
          <h3 className="font-semibold mb-2">Discard:</h3>
          <p>Tools Discarded: {toolCounts.toolsDiscarded}</p>
        </div>
      </div>

      {/* Display the log entries */}
      <div className="bg-gray-100 rounded mt-4 p-2 h-40 overflow-auto">
        <h3 className="font-semibold mb-2">Live Logs:</h3>
        <ul>
          {logs.map((log, index) => (
            <li key={index} className="text-sm mb-2">{log}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};


const VerticalButtons = () => {
  const reinitializeToolCounts = async () => {
    try {
      const response = await axios.post('/reinitialize_tool_counts');
      alert(response.data.status);
    } catch (error) {
      alert('Failed to reinitialize tool counts');
    }
  };

  const downloadLatestLog = async () => {
    try {
      const response = await axios.get('http://localhost:5001/latest_log', {
        responseType: 'blob', // Important for handling file downloads
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'latest_log.txt'); // Set the filename as needed
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      alert('Failed to download the latest log');
    }
  };

  return (
    <div className="grid grid-cols-2 gap-4">
      <button
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        onClick={reinitializeToolCounts}
      >
        Reinitialize Tool Counts
      </button>
      <button
        className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
        onClick={downloadLatestLog} // Add this line
      >
        Download Latest Log
      </button>
      <button className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600">
        Button 3
      </button>
      <button className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
        Button 4
      </button>
    </div>
  );
};



const App = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-400 to-purple-500 p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Row for VideoStream and DisplayBox side by side */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <VideoStream />
          </div>
          <div>
            <DisplayBox />
          </div>
        </div>

        {/* Buttons row (4 buttons in 2 columns layout) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <VerticalButtons />
        </div>

        {/* Text display box */}
        <div className="bg-white rounded-lg p-4 shadow-md w-full">
          <p>Text display box</p>
        </div>
      </div>
    </div>
  );
};

export default App;
