# backend/seeddata.py

from src import create_app
from src.models import db, Skill, Lesson, Quiz, Activity

app = create_app()

def seed_data():
    # Curriculum → Skill
    skills = [
        Skill(name="Critical Thinking", min_age=8, max_age=14),
        Skill(name="Communication Skills", min_age=8, max_age=14),
        Skill(name="Time Management", min_age=8, max_age=14),
        Skill(name="Extracurricular Activities", min_age=8, max_age=14),
        Skill(name="Financial Literacy", min_age=8, max_age=14)
    ]
    db.session.add_all(skills)
    db.session.commit()

<<<<<<< HEAD
    # # Lessons for first skill
    # lessons = [
    #     Lesson(skill_id=skills[0].skill_id, title="Lesson 1", content={"url_details": {"0": "https://www.lipsum.com/", "1": "https://drawsql.app"}}, position=1),
    #     Lesson(skill_id=skills[0].skill_id, title="Lesson 2", content={"url_details": {"0": "https://dflsjds.com", "1": "https://google.com"}}, position=2),
    #     Lesson(skill_id=skills[0].skill_id, title="Lesson 3", content={"url_details": {}}, position=3),
    #     Lesson(skill_id=skills[0].skill_id, title="Ram 4", content={"url_details": {}}, position=4),
    #     Lesson(skill_id=skills[0].skill_id, title="Ram 5", content={"url_details": {}}, position=5),
    # ]
    # db.session.add_all(lessons)
    # db.session.commit()

    # # Dummy Quiz
    # quiz = Quiz(
    #     quiz_name="Quiz 1",
    #     description="Description for Quiz 1",
    #     questions={
    #         "1": {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "marks": 10},
    #         "2": {"question": "What is the largest planet?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "marks": 10},
    #         "3": {"question": "Chemical symbol for water?", "options": ["H2O", "CO2", "O2", "NaCl"], "marks": 10},
    #     },
    #     answers={"1": "Paris", "2": "Jupiter", "3": "H2O"},
    #     time_duration=300,
    #     lesson_id=lessons[0].lesson_id,
    #     position=1
    # )
    # db.session.add(quiz)
    # db.session.commit()

    # # Dummy Activities
    # activities = [
    #     Activity(name="Activity 1", description="Description for Activity 1", answer_format="text", lesson_id=lessons[0].lesson_id),
    #     Activity(name="Activity 2", description="Description for Activity 2", answer_format="image", lesson_id=lessons[1].lesson_id),
    #     Activity(name="Activity 3", description="Description for Activity 3", answer_format="text", lesson_id=lessons[2].lesson_id),
    #     Activity(name="Activity 4", description="Description for Activity 4", answer_format="pdf", lesson_id=lessons[3].lesson_id),
    # ]
    # db.session.add_all(activities)
    # db.session.commit()
=======
    # Lessons for first skill
    lessons = [
        Lesson(skill_id=skills[0].skill_id, title="Lesson 1", content={"url_details": {"0": "https://www.lipsum.com/", "1": "https://drawsql.app"}}, position=1),
        Lesson(skill_id=skills[0].skill_id, title="Lesson 2", content={"url_details": {"0": "https://dflsjds.com", "1": "https://google.com"}}, position=2),
        Lesson(skill_id=skills[0].skill_id, title="Lesson 3", content={"url_details": {}}, position=3),
        Lesson(skill_id=skills[0].skill_id, title="Ram 4", content={"url_details": {}}, position=4),
        Lesson(skill_id=skills[0].skill_id, title="Ram 5", content={"url_details": {}}, position=5),
    ]
    db.session.add_all(lessons)
    db.session.commit()

    # Dummy Quiz
    quiz = Quiz(
        quiz_name="Quiz 1",
        description="Description for Quiz 1",
        questions={
            "1": {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "marks": 10},
            "2": {"question": "What is the largest planet?", "options": ["Earth", "Mars", "Jupiter", "Saturn"], "marks": 10},
            "3": {"question": "Chemical symbol for water?", "options": ["H2O", "CO2", "O2", "NaCl"], "marks": 10},
        },
        answers={"1": "Paris", "2": "Jupiter", "3": "H2O"},
        time_duration=300,
        lesson_id=lessons[0].lesson_id,
        position=1
    )
    db.session.add(quiz)
    db.session.commit()

    # Dummy Activities
    activities = [
        Activity(name="Activity 1", description="Description for Activity 1", answer_format="text", lesson_id=lessons[0].lesson_id),
        Activity(name="Activity 2", description="Description for Activity 2", answer_format="image", lesson_id=lessons[1].lesson_id),
        Activity(name="Activity 3", description="Description for Activity 3", answer_format="text", lesson_id=lessons[2].lesson_id),
        Activity(name="Activity 4", description="Description for Activity 4", answer_format="pdf", lesson_id=lessons[3].lesson_id),
    ]
    db.session.add_all(activities)
    db.session.commit()
>>>>>>> main

    print("✅ Seed data inserted successfully!")

if __name__ == "__main__":
    with app.app_context():
        seed_data()
