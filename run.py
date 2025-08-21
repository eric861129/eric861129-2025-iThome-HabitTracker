from app import create_app, db
from app.models import User, Habit, MoodLog, HabitTracking

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Habit': Habit, 
        'MoodLog': MoodLog, 
        'HabitTracking': HabitTracking
    }

if __name__ == '__main__':
    app.run(debug=True)
