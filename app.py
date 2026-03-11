from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import random
import requests
import json
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# ===== REPLACE WITH THIS =====
# Database configuration - Works with both SQLite and PostgreSQL
database_url = os.environ.get('DATABASE_URL', 'sqlite:///fitness.db')

# Fix for Render's PostgreSQL URL format
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Mail configuration for OTP
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
mail = Mail(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    fitness_level = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    current_weight = db.Column(db.Float)
    date = db.Column(db.Date)
    notes = db.Column(db.Text)

class WorkoutSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    schedule_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Add these with your other database models (User, UserProgress, etc.)

class UserProfile(db.Model):
    """Extended user profile"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    profile_pic = db.Column(db.String(200), default='default.jpg')
    bio = db.Column(db.Text)
    fitness_goal = db.Column(db.String(100))
    target_weight = db.Column(db.Float)
    target_date = db.Column(db.Date)
    experience_level = db.Column(db.String(50))
    workout_preferences = db.Column(db.Text)  # JSON stored
    
    # Social
    friends = db.Column(db.Text)  # JSON list of friend IDs
    achievements = db.Column(db.Text)  # JSON list of badges
    
    # Settings
    dark_mode = db.Column(db.Boolean, default=False)
    email_notifications = db.Column(db.Boolean, default=True)


class WorkoutLog(db.Model):
    """Track daily workouts"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, default=datetime.utcnow().date())
    workout_name = db.Column(db.String(200))
    duration = db.Column(db.Integer)  # minutes
    calories_burned = db.Column(db.Integer)
    exercises = db.Column(db.Text)  # JSON of exercises



class NutritionLog(db.Model):
    """Track daily nutrition"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    meal_type = db.Column(db.String(50))  # breakfast, lunch, etc.
    food_items = db.Column(db.Text)  # JSON
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fats = db.Column(db.Float)
    water_intake = db.Column(db.Float)  # in liters

class FriendRequest(db.Model):
    """Friend connections"""
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    status = db.Column(db.String(20))  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ===== AFTER YOUR EXISTING MODELS (WorkoutLog, Achievement etc) =====

class MealLog(db.Model):
    """Track daily meals"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, default=datetime.utcnow().date())
    meal_type = db.Column(db.String(50))  # breakfast, lunch, dinner, snack
    food_name = db.Column(db.String(200))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fats = db.Column(db.Float)
    image_url = db.Column(db.String(500))  # Food image

class UserSettings(db.Model):
    """User preferences and settings"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notification_enabled = db.Column(db.Boolean, default=True)
    dark_mode = db.Column(db.Boolean, default=False)
    measurement_unit = db.Column(db.String(10), default='metric')  # metric/imperial
    workout_reminder_time = db.Column(db.String(5), default='08:00')
    meal_reminder_time = db.Column(db.String(5), default='12:00')
    water_goal = db.Column(db.Float, default=2.5)  # liters
    daily_calorie_goal = db.Column(db.Integer, default=2000)


class Achievement(db.Model):
    """User achievements"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    badge_name = db.Column(db.String(100))
    badge_icon = db.Column(db.String(50))
    date_earned = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)

# Create tables
with app.app_context():
    db.create_all()

# Store OTP temporarily
otp_storage = {}

# Routes
@app.route('/')
def index():
    return render_template('index.html')


import sendgrid
from sendgrid.helpers.mail import Mail

@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        email = request.json.get('email')
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp
        
        # Try Gmail SMTP first (faster, if it works)
        try:
            msg = Message('FitAI - Your Verification Code', 
                         sender=app.config['MAIL_USERNAME'], 
                         recipients=[email])
            msg.body = f'''Welcome to FitAI!

Your verification code is: {otp}

This code will expire in 10 minutes.

Thanks,
FitAI Team'''
            
            mail.send(msg)
            print(f"✅ OTP sent via Gmail to {email}: {otp}")
            return jsonify({'success': True, 'message': 'OTP sent successfully'})
            
        except Exception as gmail_error:
            print(f"Gmail failed: {gmail_error}, trying SendGrid...")
            
            # Fallback to SendGrid
            sg_api_key = os.getenv('SENDGRID_API_KEY')
            if not sg_api_key:
                return jsonify({'success': False, 'message': 'SendGrid API key not configured'})
            
            # Create email message using SendGrid
            message = Mail(
                from_email=app.config['MAIL_USERNAME'],  # Your verified sender email
                to_emails=email,
                subject='FitAI - Your Verification Code',
                plain_text_content=f'''Welcome to FitAI!

Your verification code is: {otp}

This code will expire in 10 minutes.

Thanks,
FitAI Team'''
            )
            
            # Send via SendGrid
            sg = sendgrid.SendGridAPIClient(api_key=sg_api_key)
            response = sg.send(message)
            
            if response.status_code == 202:  # 202 = accepted for delivery [citation:6]
                print(f"✅ OTP sent via SendGrid to {email}: {otp}")
                return jsonify({'success': True, 'message': 'OTP sent successfully'})
            else:
                print(f"❌ SendGrid error: {response.status_code}")
                return jsonify({'success': False, 'message': 'Failed to send OTP'})
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})




        



@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    email = request.json.get('email')
    otp = request.json.get('otp')
    
    if email in otp_storage and otp_storage[email] == otp:
        session['email'] = email
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            session['user_id'] = user.id
            return jsonify({'success': True, 'new_user': False})
        else:
            return jsonify({'success': True, 'new_user': True})
    
    return jsonify({'success': False, 'message': 'Invalid OTP'})

@app.route('/direct-signup', methods=['POST'])
def direct_signup():
    data = request.json
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'success': False, 'error': 'Email already registered'})
    
    # Create new user directly
    user = User(
        email=data['email'],
        name=data['name'],
        age=data['age'],
        weight=data['weight'],
        height=data['height'],
        fitness_level=data['fitness_level']
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Set session
    session['email'] = data['email']
    session['user_id'] = user.id
    
    return jsonify({'success': True})

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = User.query.get(session['user_id'])
    return render_template('dashboard.html', user=user)



            
import requests
import os
import json

@app.route('/generate-schedule', methods=['POST'])
def generate_schedule():
    try:
        data = request.json
        user = User.query.get(session['user_id'])
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'})
        
        # Get user inputs
        goal = data.get('goal', 'strength')
        level = data.get('level', 'beginner')
        equipment = data.get('equipment', 'bodyweight')
        
        # Get API key
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({'success': False, 'error': 'GROQ_API_KEY not found in .env file'})
        
        print(f"🔄 Calling Groq API for {user.name}...")
        
        # Updated models for 2026
        models = [
            "llama-3.3-70b-versatile",  # Current Llama model
            "llama-3.1-8b-instant",     # Fast, reliable
            "gemma2-9b-it"               # Google's Gemma 2
        ]
        
        schedule = None
        
        for model in models:
            try:
                print(f"  Trying model: {model}")
                
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": "You are a professional fitness trainer. Create unique workout plans with different exercises each day."},
                            {"role": "user", "content": f"""Create a 5-day workout schedule for a {user.age}-year-old person.

Details:
- Goal: {goal}
- Level: {level}
- Equipment: {equipment}

IMPORTANT RULES:
- Day 1,2,3,4,5 must have DIFFERENT focus areas
- Each day must have 5 DIFFERENT exercises
- No repeating exercises across days
- Make it appropriate for {level} level
- Use only {equipment} equipment

Format EXACTLY like this:

DAY 1: [Focus Area]
1. [Exercise] - [sets] sets x [reps] reps
2. [Exercise] - [sets] sets x [reps] reps
3. [Exercise] - [sets] sets x [reps] reps
4. [Exercise] - [sets] sets x [reps] reps
5. [Exercise] - [sets] sets x [reps] reps

DAY 2: [Different Focus Area]
...continue for 5 days"""}

                        ],
                        "temperature": 0.8,
                        "max_tokens": 1000
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    schedule = result['choices'][0]['message']['content']
                    print(f"  ✅ Success with {model}")
                    break
                else:
                    print(f"  ❌ {model} failed: {response.status_code}")
                    
            except Exception as e:
                print(f"  ⚠️ Error with {model}: {str(e)}")
                continue
        
        # If all models fail, use a simple fallback
        if not schedule:
            print("❌ All models failed, using fallback")
            
            # Set sets/reps based on level
            if level == 'beginner':
                sets = 3
                reps = "10-12"
            elif level == 'intermediate':
                sets = 4
                reps = "8-10"
            else:
                sets = 4
                reps = "6-8"
            
            schedule = f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5-DAY WORKOUT PLAN (Temporary)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
For: {user.name} | Goal: {goal} | Level: {level} | Equipment: {equipment}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAY 1: Upper Body
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Push-ups - {sets} x {reps}
2. Dumbbell Rows - {sets} x {reps}
3. Overhead Press - {sets} x {reps}
4. Bicep Curls - {sets} x {reps}
5. Tricep Dips - {sets} x {reps}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAY 2: Lower Body
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Squats - {sets} x {reps}
2. Lunges - {sets} x {reps}
3. Romanian Deadlifts - {sets} x {reps}
4. Calf Raises - {sets} x 15
5. Glute Bridges - {sets} x {reps}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAY 3: Core & Cardio
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Planks - 3 x 45 sec
2. Mountain Climbers - 3 x 30 sec
3. Bicycle Crunches - 3 x 20
4. Leg Raises - 3 x 15
5. Jumping Jacks - 3 x 30 sec

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAY 4: Full Body
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Burpees - 3 x 8
2. Dumbbell Thrusters - {sets} x {reps}
3. Renegade Rows - {sets} x {reps}
4. Dumbbell Swings - {sets} x {reps}
5. Push-ups - {sets} x {reps}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DAY 5: Active Recovery
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Light walking - 20 min
2. Full body stretching - 15 min
3. Foam rolling - 10 min
4. Deep breathing - 5 min
5. Yoga poses - 10 min

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 TIP: Stay hydrated and rest 60s between sets!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        # Save schedule
        workout_schedule = WorkoutSchedule(
            user_id=user.id,
            schedule_data=schedule
        )
        db.session.add(workout_schedule)
        db.session.commit()
        
        return jsonify({'success': True, 'schedule': schedule})
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})
        

        
        
 


        


        

    
    
        
    
    

@app.route('/update-progress', methods=['POST'])
def update_progress():
    data = request.json
    progress = UserProgress(
        user_id=session['user_id'],
        current_weight=data['current_weight'],
        date=datetime.now().date(),
        notes=data.get('notes', '')
    )
    
    db.session.add(progress)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/schedule')
def schedule():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('schedule.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = User.query.get(session['user_id'])
    print(f"Loading profile for user: {user.name if user else 'None'}")
    return render_template('profile.html', user=user)

@app.route('/upload-profile-pic', methods=['POST'])
def upload_profile_pic():
    if 'user_id' not in session:
        return jsonify({'success': False})
    
    file = request.files['profile_pic']
    if file:
        filename = f"user_{session['user_id']}_{file.filename}"
        file.save(f'static/uploads/{filename}')
        
        # Update user profile
        user = User.query.get(session['user_id'])
        # You'd need to add profile_pic field to User model
        db.session.commit()
        
        return jsonify({'success': True})
    
    return jsonify({'success': False})

@app.route('/api/quote')
def get_quote():
    quotes = [
        "The only bad workout is the one that didn't happen.",
        "Your body can stand almost anything. It's your mind you need to convince.",
        "Strength doesn't come from what you can do. It comes from overcoming the things you once thought you couldn't.",
        "The difference between try and triumph is a little umph!",
        "Success starts with self-discipline."
    ]
    return jsonify({
        'quote': random.choice(quotes),
        'author': 'FitAI'
    })



@app.route('/nutrition')
def nutrition():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('nutrition.html')

@app.route('/analytics')
def analytics():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('analytics.html')

@app.route('/community')
def community():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('community.html')

@app.route('/log-workout', methods=['POST'])
def log_workout():
    data = request.json
    workout = WorkoutLog(
        user_id=session['user_id'],
        date=datetime.now().date(),
        workout_type=data['type'],
        duration=data['duration'],
        calories_burned=data['calories'],
        notes=data.get('notes', '')
    )
    db.session.add(workout)
    db.session.commit()
    return jsonify({'success': True})




@app.route('/log-meal', methods=['POST'])
def log_meal():
    data = request.json
    meal = MealLog(
        user_id=session['user_id'],
        meal_type=data['meal_type'],
        food_name=data['food_name'],
        calories=data['calories'],
        protein=data.get('protein', 0),
        carbs=data.get('carbs', 0),
        fats=data.get('fats', 0),
        image_url=data.get('image_url', '')
    )
    db.session.add(meal)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/get-recent-meals')
def get_recent_meals():
    meals = MealLog.query.filter_by(user_id=session['user_id'])\
        .order_by(MealLog.date.desc()).limit(5).all()
    return jsonify([{
        'meal_type': m.meal_type,
        'food_name': m.food_name,
        'calories': m.calories,
        'image_url': m.image_url
    } for m in meals])

@app.route('/get-recent-workouts')
def get_recent_workouts():
    workouts = WorkoutLog.query.filter_by(user_id=session['user_id'])\
        .order_by(WorkoutLog.date.desc()).limit(5).all()
    return jsonify([{
        'workout_name': w.workout_name,
        'duration': w.duration,
        'calories_burned': w.calories_burned,
        'date': w.date.strftime('%Y-%m-%d')
    } for w in workouts])

@app.route('/save-settings', methods=['POST'])
def save_settings():
    data = request.json
    settings = UserSettings.query.filter_by(user_id=session['user_id']).first()
    if not settings:
        settings = UserSettings(user_id=session['user_id'])
    
    settings.notification_enabled = data.get('notification_enabled', True)
    settings.dark_mode = data.get('dark_mode', False)
    settings.measurement_unit = data.get('measurement_unit', 'metric')
    settings.workout_reminder_time = data.get('workout_reminder_time', '08:00')
    settings.meal_reminder_time = data.get('meal_reminder_time', '12:00')
    settings.water_goal = data.get('water_goal', 2.5)
    settings.daily_calorie_goal = data.get('daily_calorie_goal', 2000)
    
    db.session.add(settings)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/get-weather')
def get_weather():
    # Use free OpenWeatherMap API
    import requests
    city = request.args.get('city', 'Chennai')
    api_key = os.getenv('WEATHER_API_KEY')  # Get free key from openweathermap.org
    
    if not api_key:
        # Mock weather for demo
        return jsonify({
            'temp': 32,
            'condition': 'Sunny',
            'humidity': 65,
            'icon': '☀️'
        })
    
    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    )
    return jsonify(response.json())

@app.route('/get-nutrition-tip')
def get_nutrition_tip():
    tips = [
        {"tip": "Drink 2-3 liters of water daily for optimal metabolism", "icon": "💧"},
        {"tip": "Include protein in every meal to support muscle growth", "icon": "🥩"},
        {"tip": "Eat colorful vegetables for essential vitamins", "icon": "🥗"},
        {"tip": "Don't skip breakfast - it kickstarts your metabolism", "icon": "🍳"},
        {"tip": "Healthy fats like avocado and nuts are essential", "icon": "🥑"},
        {"tip": "Complex carbs provide sustained energy for workouts", "icon": "🍠"},
        {"tip": "Meal prep on Sundays to stay on track", "icon": "📅"},
        {"tip": "Listen to your body's hunger cues", "icon": "👂"},
    ]
    import random
    return jsonify(random.choice(tips))

@app.route('/get-achievements')
def get_achievements():
    user_id = session['user_id']
    
    # Calculate achievements based on user data
    workout_count = WorkoutLog.query.filter_by(user_id=user_id).count()
    meal_count = MealLog.query.filter_by(user_id=user_id).count()
    
    # Get streak
    from datetime import datetime, timedelta
    today = datetime.now().date()
    streak = 0
    for i in range(30):  # Check last 30 days
        day = today - timedelta(days=i)
        workout = WorkoutLog.query.filter_by(user_id=user_id, date=day).first()
        if workout:
            streak += 1
        else:
            break
    
    achievements = []
    
    if workout_count >= 1:
        achievements.append({
            'name': 'First Workout',
            'icon': '🎯',
            'description': 'Completed your first workout',
            'date': 'Today'
        })
    if workout_count >= 10:
        achievements.append({
            'name': 'Getting Stronger',
            'icon': '💪',
            'description': 'Completed 10 workouts',
            'date': 'Recent'
        })
    if streak >= 7:
        achievements.append({
            'name': 'Week Warrior',
            'icon': '🔥',
            'description': f'{streak} day streak',
            'date': 'Current'
        })
    if meal_count >= 5:
        achievements.append({
            'name': 'Healthy Eater',
            'icon': '🥗',
            'description': 'Logged 5 meals',
            'date': 'Recent'
        })
    
    return jsonify(achievements)



@app.route('/log-workout-page')
def log_workout_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('log_workout.html', now=datetime.now())

@app.route('/log-meal-page')
def log_meal_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('log_meal.html', now=datetime.now())

@app.route('/progress')
def progress_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('progress.html')

@app.route('/get-progress-data')
def get_progress_data():
    user_id = session['user_id']
    
    # Get all workouts
    workouts = WorkoutLog.query.filter_by(user_id=user_id).order_by(WorkoutLog.date).all()
    
    # Calculate stats
    totalWorkouts = len(workouts)
    totalCalories = sum(w.calories_burned for w in workouts)
    totalMinutes = sum(w.duration for w in workouts)
    
    # Calculate streak
    from datetime import datetime, timedelta
    today = datetime.now().date()
    streak = 0
    for i in range(30):
        day = today - timedelta(days=i)
        if any(w.date == day for w in workouts):
            streak += 1
        else:
            break
    
    # Weekly data (last 7 days)
    weekLabels = []
    weeklyWorkouts = []
    weeklyCalories = []
    
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        weekLabels.append(day.strftime('%a'))
        day_workouts = [w for w in workouts if w.date == day]
        weeklyWorkouts.append(len(day_workouts))
        weeklyCalories.append(sum(w.calories_burned for w in day_workouts))
    
    # Workout types for pie chart
    workout_types = {}
    for w in workouts:
        workout_types[w.workout_type] = workout_types.get(w.workout_type, 0) + 1
    
    # Recent activity for timeline
    recent = sorted(workouts, key=lambda x: x.date, reverse=True)[:5]
    recentActivity = []
    for w in recent:
        recentActivity.append({
            'icon': 'fa-dumbbell',
            'date': w.date.strftime('%b %d'),
            'title': w.workout_type,
            'calories': w.calories_burned,
            'duration': w.duration
        })
    
    return jsonify({
        'totalWorkouts': totalWorkouts,
        'totalCalories': totalCalories,
        'totalMinutes': totalMinutes,
        'streak': streak,
        'weekLabels': weekLabels,
        'weeklyWorkouts': weeklyWorkouts,
        'weeklyCalories': weeklyCalories,
        'workoutTypes': list(workout_types.keys()),
        'workoutCounts': list(workout_types.values()),
        'recentActivity': recentActivity
    })

@app.route('/get-daily-totals')
def get_daily_totals():
    user_id = session['user_id']
    today = datetime.now().date()
    
    meals = MealLog.query.filter_by(user_id=user_id, date=today).all()
    total_calories = sum(m.calories for m in meals)
    total_protein = sum(m.protein for m in meals)
    
    return jsonify({
        'calories': total_calories,
        'protein': total_protein
    })





# ===== ADD THIS AT THE VERY BOTTOM, BEFORE if __name__ =====

# Add this function to initialize database
def init_db():
    with app.app_context():
        db.create_all()
        print("✅ Database tables created/verified!")

# Your existing code at the bottom should look like this:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


    



if __name__ == '__main__':
    app.run(debug=True)