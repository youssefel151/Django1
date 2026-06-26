from django.contrib import admin
from .models import Student, Course, Exam, Grade, Transcript


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email']
    search_fields = ['student_id', 'first_name', 'last_name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credits']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'course', 'exam_type', 'date']
    list_filter = ['exam_type', 'course']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'score', 'letter_grade', 'date_submitted']
    list_filter = ['exam__course']
    search_fields = ['student__student_id']


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'issue_date', 'gpa']
