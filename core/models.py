from django.db import models


from rest_framework.authentication import SessionAuthentication, BasicAuthentication , TokenAuthentication


from django.contrib.auth.models import User

# Create your models here.


CLASS_CHOICES = (
		('اولي', "اولي"),
		('ثانيه علمي', "ثانيه علمي"),
		('ثانيه ادبي', "ثانيه ادبي"),
		('ثالثه', "ثالثه")
	)


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	#profile_pic = models.ImageField(upload_to="profile_pics", default="default_pp.jpg")
	phone = models.CharField(max_length=15)
	parent_phone = models.CharField(max_length=15)
	year = models.CharField(max_length=15, choices=CLASS_CHOICES)
	#create_time = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f'{self.user.username} _ {self.id}'




class Exam(models.Model):
	#teacher = models.ForeignKey(User, on_delete=models.CASCADE)
	subject = models.CharField(max_length=100)
	title = models.CharField(max_length=150, null=True)
	duration = models.IntegerField(default=10)
	published = models.BooleanField(default=False)
	published_time = models.DateTimeField(null=True, blank=True)
	ended = models.BooleanField(default= False)
	create_time = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f'{self.subject}'


	def total_degree(self):
		#return self.question_set.all().aggregate(Sum('degree'))
		questions = self.question_set.all()
		res = 0
		for q in questions:
			res += q.degree
		return res



class Question(models.Model):
	exam = models.ForeignKey("Exam" , on_delete=models.CASCADE)
	question = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	# TODO: INSTALL PILLOW
	# img_url = models.ImageField(default='default.png', upload_to='profile_images')
	degree = models.IntegerField()


	def __str__(self):
		return f'{self.question}'



class Answer(models.Model):
	question = models.ForeignKey("Question", on_delete=models.CASCADE)
	answer = models.TextField()
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	the_correct_answer = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.answer}'


class StudentExam(models.Model):
	student = models.ForeignKey("Student", on_delete=models.CASCADE)
	exam = models.ForeignKey("Exam", on_delete=models.CASCADE)
	start_time = models.DateTimeField(auto_now_add=True)
	end_time = models.DateTimeField(auto_now=True)
	take_again = models.BooleanField(default=False)
	# degree = models.FloatField(null=True, blank=True)	

	class Meta:
		unique_together = ['student', 'exam']


	def __str__(self):
		return f'{self.student.user.username} exam({self.exam.subject}) _ {self.id}'

	def get_total_degree(self):
		return self.exam.total_degree()

	def get_total_earn(self):
		res = 0
		answers = self.studentanswer_set.all()
		for ans in answers:
			res += ans.question.degree if ans.answer.the_correct_answer else 0
		return res


class StudentAnswer(models.Model):

	studentexam = models.ForeignKey("StudentExam", on_delete=models.CASCADE)
	question = models.ForeignKey("Question", on_delete=models.CASCADE)
	answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
	degree = models.FloatField(null=True, blank=True)

	class Meta:
		unique_together = ['studentexam', 'question']

		#constraints = [
		#	models.CheckConstraint(check=models.Q(answer__in=question.answer_set.all()), name='the answer from the question answers set'),
		#]

	def __str__(self):
		return f'{self.studentexam.student.user.username} select {self.answer}'

	# TODO: function to check weither or not the answer is the true one for the question




class BearerAuthentication(TokenAuthentication):
    '''
    Simple token based authentication using utvsapitoken.

    Clients should authenticate by passing the token key in the 'Authorization'
    HTTP header, prepended with the string 'Bearer '.  For example:

    Authorization: Bearer 956e252a-513c-48c5-92dd-bfddc364e812
    '''
    keyword = 'Bearer'


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening