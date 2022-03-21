
'''
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.test import APIClient

from faker import Faker

from django.urls import reverse
from django.contrib.auth.models import User

from .models import Student
from .views import StudentView
#import pdb; pdb.set_trace()

# Create your tests here.

class StudentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin", password="password")
        self.student_data_0 = {
            "user": {
                "username": "am012",
                "password": "012345678"
                },
            "phone": "01",
            "parent_phone": "01",
            "_class": 'F'
        }
        self.student_data = {
            "user": {
                "username": "amr",
                "password": "012345678"
                },
            "phone": "01",
            "parent_phone": "01",
            "_class": 'F'
        }
        url = reverse('students')
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(url, data=self.student_data_0, format="json")
        number_of_students = Student.objects.all().count()
        self.assertEqual(number_of_students, 1)

    def test_list_student(self):
        """
        Ensure we can retrieve all students
        """
        url = reverse('students')
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.get(url)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['username'], self.student_data_0["user"]["username"])

    def test_create_student(self):
        """
        Ensure we can create a new student object.
        - send post request with the data of the student
        - check: response status is equal 201
        - check: that there is user created (count_of_user=1)
        - check: that there is student created ( count_of_students=1)
        - check: that the user exist with the same data we provide in the post request
        """
        url = reverse('students')
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(url, data=self.student_data, format="json")
        count_of_students = Student.objects.all().count()
        count_of_users = User.objects.all().count()
        student = Student.objects.get(pk=2)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(count_of_users, 3) # the admin and the one we added
        self.assertEqual(count_of_students, 2)
        self.assertEqual(student.user.username, self.student_data["user"]["username"])
        self.assertEqual(student.phone, self.student_data["phone"])
        
    def test_delete_student(self):
        """
        Ensure we can delete a student
        - add the student
        - send delete request with the id of the student added
        - check: response status code is equal 
        - check: that the user deleted and there is only one ( the admin )
        - check: that the student deleted ( number of students = 0 )
        """
        url = reverse('student-operation', kwargs={'pk': 1})
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.delete(url, )
        count_of_students = Student.objects.all().count()
        count_of_users = User.objects.all().count()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(count_of_students, 0)
        self.assertEqual(count_of_users, 1) # the admin

    def test_edit_existed_user(self):
        """
        Ensure we can update a student data
        - send put request with the edited data
        - check: response status is equal 200
        - check: that there is user updated
        - check: that the user exist with the same updated_data we provide in the put request
        """
        updated_data = {
            "user": {
                "username": "amr_updated",
                "password": "012345678_updated"
                },
            "phone": "01109765",
            "parent_phone": "01228991",
            "_class": 'F'
        }
        url = reverse('student-operation', kwargs={'pk': 1})
        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.put(url, updated_data, format="json")
        count_of_students = Student.objects.all().count()
        count_of_users = User.objects.all().count()
        student = Student.objects.get(pk=1)
        #import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(count_of_students, 1)
        self.assertEqual(count_of_users, 2) # the admin and the student added we work on
        self.assertEqual(student.user.username, updated_data["user"]["username"])
        self.assertEqual(student.phone, updated_data["phone"])

'''
    
