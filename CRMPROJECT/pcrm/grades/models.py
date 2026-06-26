from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    enrollment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

    class Meta:
        ordering = ['student_id']


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    credits = models.PositiveIntegerField(default=3)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Exam(models.Model):
    EXAM_TYPES = [
        ('midterm', 'Examen Mi-Semestre'),
        ('final', 'Examen Final'),
        ('quiz', 'Quiz'),
        ('assignment', 'Devoir'),
        ('other', 'Autre'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES, default='final')
    date = models.DateField(default=timezone.now)
    max_score = models.FloatField(default=100.0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.name} ({self.course.code})"

    class Meta:
        ordering = ['-date']


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades')
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    date_submitted = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'exam')
        ordering = ['-date_submitted']

    def __str__(self):
        return f"{self.student} - {self.exam}: {self.score}"

    def letter_grade(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'


class Transcript(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='transcripts')
    semester = models.CharField(max_length=50)
    issue_date = models.DateField(default=timezone.now)
    gpa = models.FloatField(null=True, blank=True)
    total_credits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Transcript - {self.student} ({self.semester})"

    class Meta:
        unique_together = ('student', 'semester')
