from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer

from django.contrib.auth.models import User

from .models import Student, Question, Exam, Answer, StudentAnswer, StudentExam


class DynamicDepthSerializer(serializers.ModelSerializer):
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
        fields = ['exam', 'subject', 'start_time', 'end_time', 'total_degree','total_earn', 'studentanswer_set']

    def get_subject(self,obj):
        return obj.exam.subject

class UserSerializer(DynamicDepthSerializer):
    username = serializers.CharField()
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "password"]


class StudentSerializer(DynamicDepthSerializer):
    user = UserSerializer(write_only=True)
    username = serializers.SerializerMethodField()
    studentexam_set = StudentExamSerializer(many=True, read_only=True, required=False)
    _class_display = serializers.SerializerMethodField()
    #password = serializers.SerializerMethodField(write_only=True, required=False)

    class Meta:
        model = Student
        fields = ['id', 'username', 'profile_pic', 'user', 'phone', 'parent_phone', '_class', '_class_display', 'studentexam_set']
        # depth = 2

    def get__class_display(self, obj):
        return obj.get__class_display()

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
        instance._class = validated_data["_class"]
        instance.save()
        return instance

    

# ==========================================================================================================
# ==========================================================================================================

class AnswerSerializer(DynamicDepthSerializer):
    class Meta:
        model = Answer
        fields = ['answer', 'create_time', 'update_time', 'the_correct_answer']




class QuestionSerializer(WritableNestedModelSerializer):
    answer_set = AnswerSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['question', 'create_time', 'update_time', 'degree' , 'answer_set']
        depth = 1



class ExamSerializer(WritableNestedModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['subject', 'duration', 'published', 'published_time', 'ended', 'create_time', 'question_set']

    

# ====================================================================
# ====================================================================

'''
'''
class Student1Serializer(DynamicDepthSerializer):
    """
    Helper for StudentExamSerializer
    """
    _class = serializers.CharField(source='get__class_display')
    username = serializers.CharField(source='user.username')
    
    class Meta:
        model = Student
        fields = ['username', 'phone', '_class']
    
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








   