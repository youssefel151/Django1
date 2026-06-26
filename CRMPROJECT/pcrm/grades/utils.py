from django.db.models import Avg
from .models import Grade


def calculate_average(student, course=None):
    grades = Grade.objects.filter(student=student)
    if course:
        grades = grades.filter(exam__course=course)
    return grades.aggregate(Avg('score'))['score__avg'] or 0.0


def calculate_gpa(student, semester=None):
    grades_qs = Grade.objects.filter(student=student).select_related('exam__course')
    total_points = 0
    total_credits = 0

    for grade in grades_qs:
        course = grade.exam.course
        gpa_scale = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
        letter = grade.letter_grade()
        points = gpa_scale.get(letter, 0.0)
        total_points += points * course.credits
        total_credits += course.credits

    if total_credits == 0:
        return 0.0
    return round(total_points / total_credits, 2)


def generate_transcript_data(student, semester):
    grades = Grade.objects.filter(student=student).select_related('exam__course')
    courses_data = []

    for grade in grades:
        score_20 = round((grade.score / 100) * 20, 2)
        courses_data.append({
            'course_code': grade.exam.course.code,
            'course_name': grade.exam.course.name,
            'credits': grade.exam.course.credits,
            'score': grade.score,
            'score_20': score_20,
            'letter_grade': grade.letter_grade(),
            'note_ponderee': round(score_20 * grade.exam.course.credits, 2),
        })

    gpa = calculate_gpa(student, semester)
    total_credits = sum(item['credits'] for item in courses_data)

    if courses_data:
        weighted_sum = sum(item['score_20'] * item['credits'] for item in courses_data)
        moyenne_20 = round(weighted_sum / total_credits, 2) if total_credits else 0.0
    else:
        moyenne_20 = 0.0

    return {
        'student': student,
        'semester': semester,
        'courses': courses_data,
        'gpa': gpa,
        'moyenne_20': moyenne_20,
        'total_credits': total_credits,
    }
