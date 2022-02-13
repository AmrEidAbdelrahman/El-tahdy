from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt 
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import filters
from rest_framework.decorators import action

from rest_framework import status

from .serializers import StudentSerializer, ExamSerializer, StudentExamSerializer, StudentExamAnswerSerializer

from .models import Student, Exam, Question, Answer, StudentExam

# Create your views here.




class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    #authenticationclasses = [SessionAuthentication, BasicAuthentication]
    permissionclasses = (IsAuthenticated, )
    #permissionclasses = [IsAdminUser]
    filterset_fields = ['user__username', 'year']
    search_fields = ['user__username']
    ordering_fields = '__all__'

    def get_serializer_context(self):
        context = super().get_serializer_context()

        depth = 0
        try:
            depth = int(self.request.query_params.get('depth', 0))
        except ValueError:
            pass # Ignore non-numeric parameters and keep default 0 depth
        context['depth'] = depth

        if self.action == "list":
            context['exclude'] = ['create_time','studentexam_set','year']
        elif self.action == "retrieve":
            context['exclude'] = ['create_time','year', 'studentanswer_set']
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExamView(ModelViewSet):
    serializer_class = ExamSerializer
    #authenticationclasses = [SessionAuthentication, BasicAuthentication]


    def get_queryset(self):
        published = self.request.GET.get("published")
        if published:
            return Exam.objects.all().filter(published=published)
        return Exam.objects.all().filter()

    @action(detail=True, methods=['put', 'get'])
    def take_again_all(self, request, pk=None):
        print("#####$$$$")
        exam = self.get_object()
        exam.studentexam_set.all().update(take_again=True)
        print(exam)
        return Response({"response":"take again all function"}, status=200)


class StudentExamView(ModelViewSet):
    serializer_class = StudentExamSerializer
    queryset = StudentExam.objects.all()
    #authenticationclasses = [SessionAuthentication, BasicAuthentication]

    def create(self, request, *args, **kwargs):
        student = request.user.student
        exam_id = request.POST.get("exam_id")
        exam = Exam.objects.get(pk=exam_id)
        # check the existance of an instance of the same (student, exam)
        # check the exam exist 
        student_exam = StudentExam(student=student, exam=exam)
        student_exam.save()
        return Response({"exam_id":exam_id}, status=201)

    def update(self, request, *args, **kwargs):
        exam_id = request.POST.get("exam_id")
        exam = Exam.objects.get(pk=exam_id)
        student_id = request.POST.get("student_id")
        student = Student.objects.get(pk=student_id)
        student_exam = StudentExam.objects.get(student=student, exam=exam)
        student_exam.take_again = True
        student_exam.save()
        print(student_exam)
        return Response({"response":"the exam is now available"}, status=200)

    
class StudentExamAnswer(ModelViewSet):
    serializer_class = StudentExamAnswerSerializer
    queryset = StudentExam.objects.all()


'''
{
    student_exam_id:1,
    student_answer_set: [
        {
            question_id:2,
            asnwer_id:3,
        },
        {
            question_id:2,
            asnwer_id:3,
        },
        {
            question_id:2,
            asnwer_id:3,
        },
    ]
}

'''