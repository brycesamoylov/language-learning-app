# Language Learning Application

A comprehensive language learning platform that helps users learn new languages through interactive lessons, gamification, and community features.

## Features

- User Profiles with personalized learning goals
- Interactive Lessons (reading, writing, listening, speaking)
- Gamification (points, badges, leaderboards)
- Vocabulary Builder with spaced repetition
- Speaking Practice with speech recognition
- Language Exchange with native speakers
- Progress Tracking Dashboard
- Cultural Insights
- Offline Access
- Push Notifications
- Community Features
- Integration with external language tools

## Tech Stack

### Backend
- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (migrations)
- Python-Socket.IO (real-time features)
- Speech Recognition

### Frontend
- React
- Redux Toolkit
- Material-UI
- Socket.IO Client
- React Router

## Getting Started

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the backend directory with:
```
DATABASE_URL=postgresql://user:password@localhost/language_learning
SECRET_KEY=your-secret-key
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Documentation

Once the backend server is running, visit `http://localhost:8000/docs` for the interactive API documentation.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
