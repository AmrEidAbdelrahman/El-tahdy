from django.urls import path
from rest_framework.authtoken import views

from .views import StudentView, ExamView, StudentExamView, StudentExamAnswer


urlpatterns = [
	path('students/', StudentView.as_view({'get': 'list', 'post': 'create'}), name='students'),
	path('students/<pk>/', StudentView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='student-operation'),


	path('exams/', ExamView.as_view({'get':'list', 'post':'create'}), name='exam-list'),
	path('exams/<pk>/', ExamView.as_view({'put':'update', 'get':'retrieve', 'delete':'destroy'}), name='exam-operations'),
	path('exams/<pk>/take-again-all/', ExamView.as_view({'put':'take_again_all'}), name="take-again-all"),
	path('exams/<pk>/student-list/', StudentExamView.as_view({'get':'retrieve'}), name="exam-student-list"),


	# create a StudentExam object for the student to use it in saving the student answer
	path('start-exam/', StudentExamView.as_view({'post':'create'}), name="start-exam"),
	
	# make the exam available again for specific student
	path('take-again/', StudentExamView.as_view({'put':'update'}), name="take-again"),
	
	path('student-exam-answer/', StudentExamAnswer.as_view({"post":"create"})),
	path('student-exam-answer/<pk>/', StudentExamAnswer.as_view({'get':'retrieve'}), name="student-exam-answer"),

	path('api-token-auth/', views.obtain_auth_token),

]