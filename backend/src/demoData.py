from .models import Admin, Session, Parent, Child, Skill, Lesson, LessonHistory, Activity, ActivityHistory, Quiz, QuizHistory, Badge, BadgeHistory
from . import db
from datetime import date, datetime

def createDummyData():
    # Clear and recreate tables
    db.drop_all()
    db.create_all()

    # Admin
    admin = Admin(email_id='admin@example.com', password='securepassword')

    # Parents
    parent1 = Parent(name='Alice Smith', email_id='alice@example.com', password='alicepass')
    parent2 = Parent(name='Bob Johnson', email_id='bob@example.com', password='bobpass', is_blocked=True)

    # Children
    child1 = Child(
        name='Charlie Smith', username='charlie123', password='charliepass', dob=date(2015, 5, 15),
        school='Sunrise Elementary', email_id='charlie@example.com', points=100, streak=5,
        last_login=datetime.utcnow(), parent=parent1
    )
    child2 = Child(
        name='Daisy Johnson', username='daisyj', password='daisypass', dob=date(2014, 8, 20),
        school='Greenwood School', email_id='daisy@example.com', parent=parent2
    )

    # Skills
    skill1 = Skill(name='Math', description='Basic math skills', min_age=5, max_age=12)
    skill2 = Skill(name='Science', description='Intro to science', min_age=6, max_age=12)

    # Lessons
    lesson1 = Lesson(skill=skill1, title='Addition', content={"text": "Learn to add numbers"}, position=1)
    lesson2 = Lesson(skill=skill1, title='Subtraction', content={"text": "Learn to subtract"}, position=2)
    lesson3 = Lesson(skill=skill2, title='Plants', content={"text": "Learn about plants"}, position=1)

    # Quizzes
    quiz1 = Quiz(
        quiz_name='Addition Quiz', description='Test your addition', questions=[{"q": "2+2?"}],
        answers=[{"a": "4"}], time_duration=300, lesson=lesson1, position=1
    )
    quiz2 = Quiz(
        quiz_name='Plants Quiz', description='Plant parts', questions=[{"q": "Part of plant that makes food?"}],
        answers=[{"a": "Leaf"}], time_duration=300, lesson=lesson3, position=1
    )

    # Activities
    activity1 = Activity(name='Add & Color', description='Draw and add numbers', answer_format='image', child=child1, parent=parent1, lesson=lesson1)
    activity2 = Activity(name='Plant Drawing', description='Draw a plant', answer_format='image', child=child2, parent=parent2, lesson=lesson3)

    # Lesson History
    lesson_hist1 = LessonHistory(child=child1, lesson=lesson1)

    # Quiz History
    quiz_hist1 = QuizHistory(quiz=quiz1, child=child1, score=10, responses=[{"q": "2+2?", "a": "4"}])

    # Badge
    badge1 = Badge(name='Math Whiz', description='Awarded for completing math quiz')

    # Badge History
    badge_hist1 = BadgeHistory(child=child1, badge=badge1)
    quiz_hist1.badge_history_id = 1
    quiz1.badge = badge1

    # Add and commit
    db.session.add_all([
        admin,
        parent1, parent2,
        child1, child2,
        skill1, skill2,
        lesson1, lesson2, lesson3,
        quiz1, quiz2,
        activity1, activity2,
        lesson_hist1, quiz_hist1,
        badge1, badge_hist1
    ])
    db.session.commit()
