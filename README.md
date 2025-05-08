# ByteForce-HR1AI

ByteForce-HR1AI is a Next.js and Python-based HR management application with AI-powered features for candidate assessment and monitoring.

## Features

- AI-powered candidate assessment
- Real-time monitoring with computer vision
- User authentication with Clerk
- Database integration with Supabase
- PDF parsing and analysis
- Interactive UI with Shadcn UI and NextUI components

## Tech Stack

### Frontend
- Next.js
- React
- TypeScript
- Tailwind CSS
- Shadcn UI & NextUI components
- Clerk for authentication

### Backend
- Python (Flask)
- Computer Vision (OpenCV, YOLOv8, MediaPipe)
- OpenAI integration
- Supabase

## Getting Started

### Prerequisites
- Node.js (v18 or later)
- Python 3.8+
- Yarn
- Docker (optional, for containerized setup)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ByteForce-HR1AI.git
cd ByteForce-HR1AI
```

2. Install frontend dependencies:
```bash
yarn install
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Create necessary environment variables (refer to `.env.example` if available)

### Running the Application

#### Development Mode

1. Start the frontend:
```bash
yarn dev
```

2. Start the Python server:
```bash
python server.py
```

#### Using Docker

Make sure Docker Desktop is running and the Docker CLI is in your PATH. If you're using Docker Desktop on macOS and the `docker` command isn't found, you can add it to your PATH:

```bash
# Add Docker to your PATH (add this to your ~/.zshrc or ~/.bash_profile)
export PATH=$PATH:/Applications/Docker.app/Contents/Resources/bin
```

Then build and run the application:

```bash
# Build and run the container
docker build -t byteforce-hr1ai .
docker run -p 3000:3000 -p 5000:5000 byteforce-hr1ai

# Or using docker-compose
docker-compose up --build
```

### Troubleshooting

#### OpenCV Issues in Docker
If you encounter issues with OpenCV (`cv2`) in the Docker container related to missing libraries such as `libGL.so.1`, ensure the Dockerfile includes the necessary dependencies:

```dockerfile
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Acknowledgments

- YOLOv8 for object detection
- MediaPipe for face landmark detection
- OpenAI for AI capabilities
- NextUI and Shadcn UI for component libraries
