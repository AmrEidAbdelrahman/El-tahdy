from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from django.contrib.auth.models import User

from .models import Student, Question, Exam, Answer, StudentAnswer, StudentExam


class DynamicDepthSerializer(WritableNestedModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        exclude = self.context.get('exclude')
        depth = self.context.get('depth')
        if exclude:
            self.Meta.fields = list(self.Meta.fields)
            for ex in exclude:
                if ex in self.Meta.fields:
                    self.fields.pop(ex)
        if depth:
            self.Meta.depth = depth


class StudentAnswerSerializer(DynamicDepthSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['question', 'answer', 'degree']


class StudentExamSerializer(DynamicDepthSerializer):
    #studentanswer_set = StudentAnswerSerializer(many=True, read_only=True, required=False)
    total_degree = serializers.CharField(source="get_total_degree", read_only=True)
    total_earn = serializers.CharField(source="get_total_earn", read_only=True)
    subject = serializers.SerializerMethodField()

    class Meta:
        model = StudentExam
        fields = ['id','exam', 'subject', 'start_time', 'end_time', 'total_degree','total_earn', 'studentanswer_set']
        depth=1

    def get_subject(self,obj):
        return obj.exam.subject

class UserSerializer(DynamicDepthSerializer):
    username = serializers.CharField()
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]


class StudentSerializer(DynamicDepthSerializer):
    user = UserSerializer()
    username = serializers.SerializerMethodField()
    studentexam_set = StudentExamSerializer(many=True, read_only=True, required=False)
    #year_display = serializers.SerializerMethodField()
    #password = serializers.SerializerMethodField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = ['id', 'username', 'user', 'phone', 'parent_phone', 'year', 'studentexam_set']
        # depth = 2

    #def get_year_display(self, obj):
    #    return obj.get_year_display()

    def get_username(self, obj):
        return obj.user.username

    def create(self, validated_data):
        user = validated_data.pop('user')
        user = User(**user)
        user.save()
        student = Student(user=user, **validated_data)
        student.save()
        return student


    ## there is a beter way to do that, but i do efforts to write this funsction
    ## the better way used in ExamSerializer
    def update(self, obj, validated_data):
        instance = self.instance
        user_data = validated_data.pop('user')
        user = instance.user
        user.username = user_data['username']
        try:
            user.set_password(user_data['password'])
        except:
            pass
        user.save()
        instance.phone = validated_data["phone"]
        instance.parent_phone = validated_data["parent_phone"]
        instance.year = validated_data["year"]
        instance.save()
        return instance

    

# ==========================================================================================================
# ==========================================================================================================

class AnswerSerializer(DynamicDepthSerializer):
    class Meta:
        model = Answer
        fields = ['answer', 'the_correct_answer']




class QuestionSerializer(WritableNestedModelSerializer):
    answer_set = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['question', 'degree' , 'answer_set']
        depth = 1



class ExamSerializer(WritableNestedModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id','subject', 'duration', 'published', 'published_time', 'ended', 'create_time', 'question_set']

    

# ====================================================================
# ====================================================================
class QuestionSerializer(DynamicDepthSerializer):

    class Meta:
        model = Question
        fields = ['id', 'question', 'degree', 'answer_set']
        depth=1

class StudentAnswer1Serializer(DynamicDepthSerializer):
    question = QuestionSerializer()

    class Meta:
        model = StudentAnswer
        fields = ['question', 'answer', 'degree']

class StudentExamAnswerSerializer(WritableNestedModelSerializer):
    studentanswer_set = StudentAnswer1Serializer(many=True)

    class Meta:
        model = StudentExam
        fields = ['id', 'exam', 'studentanswer_set']
        depth = 2




# ====================================================================
# ====================================================================

'''
class Student1Serializer(DynamicDepthSerializer):
    """
    Helper for StudentExamSerializer
    """
    year = serializers.CharField(source='get_year_display')
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = Student
        fields = ['username', 'phone', 'year']
    
class StudentExam1Serializer(DynamicDepthSerializer):
    """
    Helper for ExamDetailsSerializer
    """
    student = Student1Serializer()
    total_degree = serializers.CharField(source="get_total_degree", read_only=True)
    total_earn = serializers.CharField(source="get_total_earn", read_only=True)

    class Meta:
        model = StudentExam
        #fields = ['student','exam', 'start_time', 'end_time', 'total_degree','total_earn']
        fields = ['student', 'total_degree','total_earn']


class ExamDetailsSerializer(serializers.ModelSerializer):
    """
    ExamStudent: GET request ( all the studentexams associated with the exam )
    """
    studentexam_set = StudentExam1Serializer(many=True)
    #students = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = ['subject', 'duration', 'published', 'published_time', 'ended', 'create_time', 'studentexam_set']
        depth = 2

    #def get_students(self, obj):
    #    return obj.studentexam_set.stud


'''






   