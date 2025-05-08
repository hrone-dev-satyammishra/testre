# Next.js + Flask Application for Vercel

This application combines a Next.js frontend with a Flask API backend, designed for deployment on Vercel.

## Features

- Next.js frontend
- Flask API backend with computer vision capabilities
- Webcam access for real-time monitoring
- Object detection using YOLOv8
- Face mesh analysis using MediaPipe

## Local Development

1. Install dependencies:

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

2. Run the development server:

```bash
npm run dev
```

This will start both the Next.js frontend and Flask backend server concurrently.

## Vercel Deployment

### Prerequisites

1. A Vercel account
2. Vercel CLI installed (`npm i -g vercel`)

### Deployment Steps

1. Login to Vercel:

```bash
vercel login
```

2. Deploy the application:

```bash
vercel
```

3. For production deployment:

```bash
vercel --prod
```

## Project Structure

- `/api` - Flask backend
  - `index.py` - Main Flask application
  - `handler.py` - Vercel serverless function handler
- `/src` - Next.js frontend
- `next.config.js` - Next.js configuration with API proxy
- `vercel.json` - Vercel deployment configuration

## Notes

- The Next.js config includes proxy settings to route `/api/*` requests to the Flask backend
- In development, the Flask server runs on port 5000
- In production, Vercel handles routing between the Next.js and Flask serverless functions
