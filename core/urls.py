from django.urls import path

from .views import StudentView, ExamList, QuestionList, AnswerList, StudentExamView


urlpatterns = [
	path('students/', StudentView.as_view({'get': 'list', 'post': 'create'}), name='students'),
	path('students/<pk>/', StudentView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='student-operation'),

	# path('make-available-again/<exam-id>/', MakeAvailable),

	## the student who take a specific exam
	#path('exam-taken/<pk>/', StudentExamView.as_view({'get':'retrieve'}), name='exam-student-list'),
	path('exam/<pk>/student-list/', StudentExamView.as_view({'get':'retrieve'}), name="exam-student-list"),


	path('exams/', ExamList.as_view({'get':'list', 'post':'create'}), name='exam-list'),
	path('exams/<pk>/', ExamList.as_view({'put':'update', 'get':'retrieve', 'delete':'destroy'}), name='exam-operations'),

	path('question-list/', QuestionList.as_view(), name='question-list'),

	path('answer-list/', AnswerList.as_view(), name='answer-list'),


]