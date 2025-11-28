# 🦍 KongLeague - Tournament Manager

**Muestra Tu Fuerza** - A Django-based tournament management system for League of Legends ARAM tournaments.

![Theme](https://img.shields.io/badge/Theme-Banana%20%F0%9F%8D%8C%20Kong-FFD700)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)

## Features

### Public Views
- 🏆 **Real-time Standings** - Live tournament rankings with win rates
- 📅 **Match Schedule** - Organized by match days/rounds
- 🦍 **Team Profiles** - Detailed team information and statistics
- 🎉 **Champion Celebration** - Animated winner display when tournament completes

### Admin Dashboard
- ✏️ **Team Management** - Add, edit, and delete teams
- ⚔️ **Match Management** - Create match days and record results
- 🎮 **Tournament Controls** - Manage tournament status and declare champions
- 📊 **Quick Stats** - Overview of teams, matches, and progress

### Design
- 🌙 **Dark Mode** - Gaming-optimized dark theme
- 🍌 **Banana/Gorilla Branding** - Fun, competitive aesthetic
- 📱 **Mobile Responsive** - Works on all devices
- 🎨 **Tailwind CSS** - Modern, utility-first styling

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd kongLeague
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load demo data (optional)**
   ```bash
   python manage.py setup_demo_data
   ```
   This creates:
   - Admin user (username: `admin`, password: `admin123`)
   - 9 sample teams with fun names
   - 3 match days
   - Sample matches

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Visit the application**
   - Public view: http://localhost:8000
   - Admin login: http://localhost:8000/admin-login/
   - Django admin: http://localhost:8000/admin/

### Manual Admin Setup (if not using demo data)

```bash
python manage.py createsuperuser
```

## Project Structure

```
kongLeague/
├── kongleague/           # Project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI configuration
├── tournament/           # Main app
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── templates/       # HTML templates
│   └── management/      # Custom commands
├── static/              # Static files
├── requirements.txt     # Python dependencies
├── Procfile            # Deployment configuration
└── README.md           # This file
```

## Database Models

- **Team** - Tournament teams with optional logos and captains
- **MatchDay** - Tournament rounds/days
- **Match** - Individual matches between teams
- **Tournament** - Overall tournament settings and status

## Usage Guide

### For Administrators

1. **Add Teams**
   - Go to Dashboard → Manage Teams
   - Fill in team name (required), captain, and logo URL

2. **Create Match Days**
   - Go to Dashboard → Manage Matches
   - Create a new match day (e.g., "Jornada 1")

3. **Add Matches**
   - Select the match day
   - Choose Team A and Team B
   - Add the match

4. **Record Results**
   - After a match is played, select the winner
   - The standings will update automatically

5. **Declare Champion**
   - Go to Dashboard → Settings
   - Select the champion team
   - This marks the tournament as completed

### For Viewers

- Visit the home page to see current standings
- Check the Schedule page for upcoming and completed matches
- Browse Teams page to see all competitors and their stats

## Environment Variables

Create a `.env` file in the project root (see `.env.example`):

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,*.railway.app
```

## Deployment

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions for:
- Railway.app
- Render.com

## Tech Stack

- **Backend**: Django 5.0
- **Database**: SQLite (default) / PostgreSQL (production)
- **Frontend**: Django Templates + Tailwind CSS
- **Deployment**: Gunicorn + Whitenoise

## Sample Team Names

The demo data includes these fun team names:
1. Los Monos Furiosos 🦍
2. Banana Diff 🍌
3. Kong's Disciples ⚡
4. Plátano Gaming 🎮
5. Gorilla Warfare ⚔️
6. La Manada 🐺
7. Simios Supremos 👑
8. Jungle Gap 🌴
9. El Último Banano 🥇

## Easter Eggs

Look for these hidden references in the UI:
- "Muestra Tu Fuerza" (Show Your Strength) - Main tagline
- "Former coach, forever champion" - Footer tribute
- Floating banana animation in navbar
- Crown icon for first place team
- Confetti effect on champion celebration

## Contributing

Feel free to fork this project and adapt it for your own tournaments!

## License

MIT License - Feel free to use this for your own tournaments

---

**Built with 💪 for the competitive ARAM community**

🦍 Muestra Tu Fuerza 🍌
