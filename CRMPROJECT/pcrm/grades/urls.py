from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'grades'

urlpatterns = [
    path('', lambda request: redirect('grades:student_list'), name='index'),

    # Students
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='add_student'),
    path('student/<int:student_id>/grades/', views.StudentGradesView.as_view(), name='student_grades'),

    # Grades
    path('grade/add/', views.GradeCreateView.as_view(), name='add_grade'),

    # Courses & Exams
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='add_course'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='edit_course'),
    path('exams/add/', views.ExamCreateView.as_view(), name='add_exam'),

    # Transcripts
    path('student/<int:student_id>/create-transcript/', views.create_transcript, name='create_transcript'),
    path('transcript/<int:pk>/', views.TranscriptDetailView.as_view(), name='transcript_detail'),
    path('transcript/<int:transcript_id>/pdf/', views.generate_pdf_transcript, name='transcript_pdf'),
]
