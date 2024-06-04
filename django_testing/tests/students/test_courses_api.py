import pytest
from django.contrib.auth.models import User

from model_bakery import baker

from students.models import Student, Course

from rest_framework.test import APIClient

@pytest.fixture
def api_client():
	return APIClient()

@pytest.fixture
def user():
	return User.objects.create_user('admin')

@pytest.fixture
def student_factory():
	def factory(*args, **kwargs):
		return baker.make(Student, *args, **kwargs)
	return factory


@pytest.fixture
def course_factory():
	def factory(*args, **kwargs):
		return baker.make(Course, *args, **kwargs)
	return factory

# def test_something():
# 	assert True

@pytest.mark.django_db
def test_course(api_client, course_factory):
	#Arrange
	courses = course_factory(_quantity=1)

	#Act
	response = api_client.get('/courses/')

	#Assert
	assert response.status_code == 200
	data = response.json()
	assert len(data) == len(courses)
	assert data[0]['name'] == courses[0].name

@pytest.mark.django_db
def test_course_list(api_client, course_factory):
	#Arrange
	courses = course_factory(_quantity=10)

	#Act
	response = api_client.get('/courses/')

	#Assert
	data = response.json()
	assert len(data) == len(courses)
	for i, m in enumerate(data):
		assert m['name'] == courses[i].name


@pytest.mark.django_db
def test_course_filter_id(api_client, course_factory):
	#Arrange
	courses = course_factory(_quantity=10)

	#Act
	response = api_client.get(f'/courses/?id={courses[0].id}')

	#Assert
	data = response.json()
	assert data[0]['id'] == courses[0].id


@pytest.mark.django_db
def test_course_filter_name(api_client, course_factory):
	#Arrange
	courses = course_factory(_quantity=10)

	#Act
	response = api_client.get(f'/courses/?name={courses[0].name}')

	#Assert
	data = response.json()
	assert data[0]['name'] == courses[0].name

@pytest.mark.django_db
def test_create_course(api_client, user):
	#Arrange
    count = Course.objects.count()

	#Act
    response = api_client.post('/courses/', data={'name': 'test course'})

	#Assert
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
	#Arrange
	courses = course_factory(_quantity=10)

	#Act
	response = api_client.patch(f'/courses/{courses[0].id}/', data={'name': 'updated course'})

	#Assert
	data = response.json()
	assert data['name'] == 'updated course'

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
	#Arrange
	courses = course_factory(_quantity=10)

	#Act
	response = api_client.delete(f'/courses/{courses[0].id}/')

	#Assert
	assert response.status_code == 204