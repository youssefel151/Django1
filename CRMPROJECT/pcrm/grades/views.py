from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.generic import DetailView, CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Student, Grade, Transcript, Course, Exam
from .utils import calculate_average, calculate_gpa, generate_transcript_data
from .forms import GradeForm, CourseForm, ExamForm, StudentForm
from siteweb.authz import RoleRequiredMixin, role_required
from siteweb.models import Profile


class GradeManagerMixin(RoleRequiredMixin):
    allowed_roles = (
        Profile.ROLE_ADMIN,
        Profile.ROLE_ENSEIGNANT,
    )


class StudentListView(GradeManagerMixin, ListView):
    model = Student
    template_name = 'grades/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(student_id__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_students'] = Student.objects.count()
        return context


class StudentCreateView(GradeManagerMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'grades/add_student.html'
    success_url = reverse_lazy('grades:student_list')


class StudentGradesView(GradeManagerMixin, DetailView):
    model = Student
    template_name = 'grades/student_grades.html'
    context_object_name = 'student'
    pk_url_kwarg = 'student_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.object
        grades = Grade.objects.filter(student=student).select_related('exam__course')

        query = self.request.GET.get('q', '').strip()
        course_filter = self.request.GET.get('course', '').strip()

        if query:
            grades = grades.filter(
                Q(exam__name__icontains=query)
                | Q(exam__course__name__icontains=query)
                | Q(exam__course__code__icontains=query)
            )

        if course_filter:
            grades = grades.filter(exam__course__id=course_filter)

        context['grades'] = grades
        context['overall_average'] = round(calculate_average(student), 2)
        context['gpa'] = calculate_gpa(student)
        context['query'] = query
        context['course_filter'] = course_filter
        context['courses'] = Course.objects.all()
        context['transcripts'] = Transcript.objects.filter(student=student)
        return context


class GradeCreateView(GradeManagerMixin, CreateView):
    model = Grade
    form_class = GradeForm
    template_name = 'grades/add_grade.html'

    def get_initial(self):
        initial = super().get_initial()
        student_id = self.request.GET.get('student')
        if student_id:
            initial['student'] = student_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.request.GET.get('student')
        if student_id:
            context['back_student_id'] = student_id
        return context

    def get_success_url(self):
        return reverse_lazy('grades:student_grades', kwargs={'student_id': self.object.student.id})


class CourseListView(GradeManagerMixin, ListView):
    model = Course
    template_name = 'grades/course_list.html'
    context_object_name = 'courses'


class CourseCreateView(GradeManagerMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'grades/add_course.html'
    success_url = reverse_lazy('grades:course_list')


class CourseUpdateView(GradeManagerMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'grades/add_course.html'
    success_url = reverse_lazy('grades:course_list')


class ExamCreateView(GradeManagerMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'grades/add_exam.html'
    success_url = reverse_lazy('grades:course_list')


class TranscriptDetailView(GradeManagerMixin, DetailView):
    model = Transcript
    template_name = 'grades/transcript_detail.html'
    context_object_name = 'transcript'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = generate_transcript_data(self.object.student, self.object.semester)
        return context


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def create_transcript(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    semester = request.GET.get('semester', 'Semestre 1')
    transcript, created = Transcript.objects.get_or_create(
        student=student,
        semester=semester,
        defaults={'gpa': calculate_gpa(student)}
    )

    data = generate_transcript_data(student, semester)
    transcript.gpa = calculate_gpa(student)
    transcript.total_credits = data['total_credits']
    transcript.save()

    if created:
        messages.success(request, f'Relevé de notes pour {semester} créé avec succès !')
    else:
        messages.success(request, f'Relevé de notes pour {semester} mis à jour !')
    return redirect('grades:transcript_detail', pk=transcript.id)


@role_required(Profile.ROLE_ADMIN, Profile.ROLE_ENSEIGNANT)
def generate_pdf_transcript(request, transcript_id):
    import os
    from django.conf import settings
    from xhtml2pdf import pisa

    transcript = get_object_or_404(Transcript, pk=transcript_id)
    data = generate_transcript_data(transcript.student, transcript.semester)

    # Calculate total note ponderee
    total_note_ponderee = sum(course['note_ponderee'] for course in data['courses'])

    # Get absolute paths for images
    header_image_path = os.path.join(
        settings.BASE_DIR, 'grades', 'static', 'grades', 'images', 'header.png'
    )
    stamp_image_path = os.path.join(
        settings.BASE_DIR, 'grades', 'static', 'grades', 'images', 'signature_stamp.png'
    )

    # Only pass header path if file exists
    if not os.path.exists(header_image_path):
        header_image_path = None
    if not os.path.exists(stamp_image_path):
        stamp_image_path = None

    html_string = render_to_string('grades/transcript_pdf.html', {
        'transcript': transcript,
        'data': data,
        'header_image_path': header_image_path,
        'stamp_image_path': stamp_image_path,
        'total_note_ponderee': total_note_ponderee,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="releve_notes_{transcript.student.student_id}_{transcript.semester}.pdf"'
    )

    pisa_status = pisa.CreatePDF(
        src=html_string,
        dest=response,
        base_url=os.path.join(settings.BASE_DIR, 'grades', 'static')
    )

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response
