# 🎯 Your Personal AI Fitness Coach

<div align="center">

[🌐 Live Demo](https://fitness-ai-dsgq.onrender.com)  •
[🐛 Report Bug](issues/)

</div>

---

## 📋 Project Overview

FitAI is a complete fitness ecosystem that combines AI-powered workout generation, progress tracking, social features, and gamification. Users can get personalized workout plans, track meals, earn achievements, connect with friends, and enjoy workout-optimized music.

---

## ✨ Key Features

### 🔐 1. Secure Authentication
- Email + OTP verification with 10-minute expiry
- Rate limiting (5 attempts/minute) to prevent brute force
- Session management with Flask-Login
- Password hashing with SHA-256 + salt

### 🤖 2. AI-Powered Workout Generator
- Generates unique 5-day plans based on user profile
- Multiple AI models with fallback (Llama 3.3, Llama 3.1, Gemma 2, Gemini)
- Personalized for age, weight, height, fitness level
- Equipment-specific exercises
- Goal-oriented (Weight Loss, Muscle Gain, Strength)

### 📊 3. Progress Tracking
- Log workouts with duration, calories, exercises
- Track meals with calories and macros
- Monitor weight progress over time
- Calculate streaks and consistency
- Visual charts and analytics

### 🏆 4. Achievements & Gamification
- Unlock badges for milestones (First Workout, 10 Workouts, 7-Day Streak)
- Level system based on XP (10 XP per workout, 5 XP per meal)
- Visual progress bars for each badge
- Locked/unlocked states with progress indicators

### 👥 5. Social Community
- Send/accept friend requests
- Activity feed with posts and likes
- Leaderboard ranking by workout count
- Share workout achievements

### 🎯 6. Goal Setting
- Create custom goals (weight, workout frequency, strength)
- Track progress with visual percentage bars
- Auto-complete when target reached
- View completed goals history

### 📅 7. Calendar Integration
- Visual monthly calendar view
- Add workout/meal events to specific dates
- Color-coded event types
- Click to view daily events

### 🎵 8. Music Player
- Workout playlists categorized by BPM
- Mood-based filtering (Power, Cardio, Strength, Recovery)
- Real audio playback with progress bar
- Play/Pause/Next/Previous controls

### 🌙 9. Dark Mode
- Toggle between light/dark themes
- Persists across all pages via localStorage
- Saves preference in database

### ☀️ 10. Weather Integration
- Real-time weather for user's location
- Temperature, condition, humidity display
- Auto-refresh every 30 minutes
- Fallback mock data when API unavailable

### 🥗 11. Nutrition Tips
- Daily rotating nutrition tips
- Icon-based display for each tip
- Refresh button for new tips
- Science-backed fitness advice

---

## 🛠️ Technology Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js, Font Awesome |
| **Backend** | Python Flask 2.3.0, Flask-Login, Flask-Mail, Flask-Limiter |
| **Database** | PostgreSQL 16, SQLAlchemy ORM |
| **AI Models** | Groq API (Llama 3.3, Llama 3.1, Gemma 2), OpenRouter (Gemini) |
| **APIs** | SendGrid (Email), OpenWeatherMap (Weather) |
| **Deployment** | Render.com, Gunicorn |

---

