from django.contrib import admin

from .models import Student, Question, Exam, Answer, StudentAnswer, StudentExam


admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(StudentAnswer)
admin.site.register(StudentExam)

