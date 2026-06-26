from django.test import TestCase
from django.urls import reverse
from .models import Student, Course, Exam, Grade, Transcript
from .utils import calculate_average, calculate_gpa, generate_transcript_data


class GradesModelTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id='STU100', first_name='Test', last_name='Student'
        )
        self.course = Course.objects.create(code='TST101', name='Test Course', credits=4)
        self.exam = Exam.objects.create(course=self.course, name='Final', exam_type='final', max_score=100)

    def test_letter_grade(self):
        grade = Grade.objects.create(student=self.student, exam=self.exam, score=85)
        self.assertEqual(grade.letter_grade(), 'B')

    def test_calculate_average(self):
        Grade.objects.create(student=self.student, exam=self.exam, score=80)
        self.assertEqual(calculate_average(self.student), 80.0)

    def test_calculate_gpa(self):
        Grade.objects.create(student=self.student, exam=self.exam, score=95)
        self.assertEqual(calculate_gpa(self.student), 4.0)

    def test_transcript_data_includes_score_20(self):
        Grade.objects.create(student=self.student, exam=self.exam, score=80)
        data = generate_transcript_data(self.student, 'Semestre 1')
        self.assertEqual(data['courses'][0]['score_20'], 16.0)
        self.assertEqual(data['total_credits'], 4)


class GradesViewTests(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id='STU200', first_name='View', last_name='Tester'
        )
        self.course = Course.objects.create(code='VT101', name='View Test Course', credits=3)
        self.exam = Exam.objects.create(course=self.course, name='Midterm', exam_type='midterm', max_score=100)
        Grade.objects.create(student=self.student, exam=self.exam, score=72)

    def test_student_list_view(self):
        response = self.client.get(reverse('grades:student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'STU200')

    def test_student_grades_view(self):
        response = self.client.get(reverse('grades:student_grades', kwargs={'student_id': self.student.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'View')

    def test_create_and_view_transcript(self):
        response = self.client.get(
            reverse('grades:create_transcript', kwargs={'student_id': self.student.id}),
            {'semester': 'Semestre 1'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Transcript.objects.filter(student=self.student, semester='Semestre 1').exists())

    def test_transcript_pdf_download(self):
        transcript = Transcript.objects.create(student=self.student, semester='Semestre 1')
        response = self.client.get(reverse('grades:transcript_pdf', kwargs={'transcript_id': transcript.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_add_grade_view(self):
        response = self.client.get(reverse('grades:add_grade'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Étudiant')
