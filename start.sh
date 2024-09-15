#!/bin/bash
# Navigate to the frontend directory and start the React application
echo "Starting React frontend..."
cd ../frontend || exit
npm install
npm run dev
