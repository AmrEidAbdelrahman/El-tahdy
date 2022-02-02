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

from rest_framework import status

from .serializers import StudentSerializer, ExamSerializer, StudentExamSerializer

from .models import Student, Exam, Question, Answer, StudentExam

# Create your views here.




class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated, )
    #permission_classes = [IsAdminUser]
    filterset_fields = ['user__username', '_class']
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
            context['exclude'] = ['create_time','studentexam_set','_class']
        elif self.action == "retrieve":
            context['exclude'] = ['create_time','_class', 'studentanswer_set']
        return context

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExamView(ModelViewSet):
    serializer_class = ExamSerializer
    #authentication_classes = [SessionAuthentication, BasicAuthentication]


    def get_queryset(self):
        published = self.request.GET.get("published")
        if published:
            return Exam.objects.all().filter(published=published)
        return Exam.objects.all().filter()


    def start_exam(self):
        print(self)
        print("#######")

        return Response({"test":"test start exam"})

class StudentExamView(ModelViewSet):
    serializer_class = StudentExamSerializer
    queryset = StudentExam.objects.all()
    #authentication_classes = [SessionAuthentication, BasicAuthentication]

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




''' 
@require_http_methods(["POST"])
@csrf_exempt
def start_exam(request, exam_id):
    print("#######################")
    print(request.auth)
    print(request.user)
    student = request.user.student
    exam = Exam.objects.get(pk=exam_id)
    # check the existance of an instance of the same (student, exam)
    # check the exam exist 
    student_exam = StudentExam(student=student, exam=exam)
    student_exam.save()
    print(student_exam)
    return Response({"student_exam":student_exam}, status=status.HTTP_204_NO_CONTENT)
    
    #Response({"error":"There is some thing wrong"})
'''



'''
class ExamView(APIView):
    def get(self, request, *args, **kwargs):
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    class StudentExamView(ModelViewSet):
    serializer_class = StudentExamSerializer

    def get_queryset(self):
        return StudentExam.objects.all()
'''   

'''
    def get_queryset(self):
        queryset = Student.objects.all()
        name = self.request.query_params.get("name")
        _class = self.request.query_params.get("class")
        print(_class)
        if name :
            #TODO: add the filter on the class too
            return queryset.filter(name__icontains=name)
        return queryset
'''
    



'''
    class StudentList(APIView):
        def get(self, request, *args, **kwargs):
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)

        def post(self, request, *args, **kwargs):
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    class QuestionList(APIView):
        def get(self, request, *args, **kwargs):
            questions = Question.objects.all()
            serializer = QuestionSerializer(questions, many=True)
            return Response(serializer.data)

        def post(self, request, *args, **kwargs):
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    class AnswerList(APIView):
        def get(self, request, *args, **kwargs):
            questions = Answer.objects.all()
            serializer = AnswerSerializer(questions, many=True)
            return Response(serializer.data)

        def post(self, request, *args, **kwargs):
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''