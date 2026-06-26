from django import forms
from .models import Grade, Exam, Student, Course


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'exam', 'score', 'comments']
        labels = {
            'student': 'Étudiant',
            'exam': 'Examen',
            'score': 'Note (/100)',
            'comments': 'Commentaires',
        }
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3}),
            'score': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '100'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['course', 'name', 'exam_type', 'date', 'max_score']
        labels = {
            'course': 'Cours',
            'name': "Nom de l'examen",
            'exam_type': "Type d'examen",
            'date': 'Date',
            'max_score': 'Note maximale',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'max_score': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'first_name', 'last_name', 'email', 'date_of_birth']
        labels = {
            'student_id': 'ID Étudiant',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Email',
            'date_of_birth': 'Date de naissance',
        }
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'credits', 'description']
        labels = {
            'code': 'Code du cours',
            'name': 'Nom du cours',
            'credits': 'Crédits',
            'description': 'Description',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
