from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from users.models import University, Faculty, Department, UserProfile
from cms.models import UserPost, UserComment, Topic
from cms.forms import UserPostForm


class UsersAPITest(APITestCase):
    def test_return_list_of_users(self):
        # Setup test
        url = reverse('api_users_list')

        # Exercise test
        response = self.client.get(url)

        # Assert test
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_new_user(self):
        # Setup test
        url = reverse('api_user_create')
        data = {'username': 'waelll', 'email': 'teststest@hhhh.com', 'password': '22222222255555hhem',
                'password_confirmation': '22222222255555hhem'}

        # Exercise test
        response = self.client.post(url, data)

        # Assert test
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.last().username, 'waelll')
        self.assertIsNotNone(User.objects.last().auth_token)

    def test_add_new_user_with_invalid_username(self):
        # Setup test
        url = reverse('api_user_create')
        data = {'username': '123wael', 'email': 'teststest@hhhh.com', 'password': '22222222255555hhem',
                'password_confirmation': '22222222255555hhem'}

        # Exercise test
        response = self.client.post(url, data)

        # Assert test
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'اسم المستخدم مش مناسب.'})
        self.assertEqual(User.objects.count(), 0)

    def test_add_new_user_with_invalid_email(self):
        # Setup test
        url = reverse('api_user_create')
        data = {'username': 'wwwweee', 'email': 'teststest@hcom', 'password': '22222222255555hhem',
                'password_confirmation': '22222222255555hhem'}

        # Exercise test
        response = self.client.post(url, data)

        # Assert test
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'البريد الالكتروني مش صح.'})
        self.assertEqual(User.objects.count(), 0)

    def test_get_specific_user(self):
        # Setup test
        user = User.objects.create_user(username="teeest", password="sdfsd56f4sd8fs8df4sd")
        url = reverse('api_user', kwargs={'pk': user.id})

        # Exercise test
        response = self.client.get(url)

        # Assert test
        self.assertEqual(response.data['username'], user.username)

    def test_check_user_successfully(self):
        """Assert that API will authenticate the user and return the token."""
        # Test setup
        user = User.objects.create_user(username="teeest", password="sdfsd56f4sd8fs8df4sd")
        data = {'username': user.username, 'password': 'sdfsd56f4sd8fs8df4sd'}
        url = reverse('api_user_check')

        # Test body
        response = self.client.post(url, data=data)

        # Test assertion
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['token'])
        self.assertEqual(response.data['token'], user.auth_token.key)

    def test_check_non_existing_user(self):
        """Assert that API will handle the case of non-existing user."""
        # Test setup
        data = {'username': 'dfdfff', 'password': 'sdfsd56f4sd8fs8df4sd'}
        url = reverse('api_user_check')

        # Test body
        response = self.client.post(url, data=data)

        # Test assertion
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'الاسم أو الباسورد مش صح!')

    def test_check_missing_user_details(self):
        """Assert that API will handle the case of missing parameter in request."""
        # Test setup
        data = {'username': 'dfdfff'}
        url = reverse('api_user_check')

        # Test body
        response = self.client.post(url, data=data)

        # Test assertion
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'الاسم أو الباسورد مش صح!')

    def test_get_list_of_univs(self):
        # Setup test
        url = reverse('api_univs_list')

        # Exercise test
        response = self.client.get(url)

        # Assert test
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_univ_linked(self):
        # Setup test
        u = University.objects.create()
        url = reverse('api_univ', kwargs={'pk': u.pk})

        # Exercise test
        response = self.client.get(url)

        # Assert test
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DiscussionAPITest(APITestCase):
    def setUp(self):
        self.uni = University.objects.create(name='Test university')
        self.fac = Faculty.objects.create(name='Test faculty')
        self.dep = Department.objects.create(name='Test dep')
        self.topic = Topic.objects.create(pk=1, name='test topic with spaces', desc='ddddd', term=1, weeks=5)
        self.topic.department.add(self.dep)
        self.topic2 = Topic.objects.create(pk=2, name='test topic2 with spaces', desc='ddddd', term=2, weeks=5)
        self.topic2.department.add(self.dep)
        self.user = User.objects.create_user(username='ibrahemmmmm', email='test_@test.com',
                                             password='000000555555ddd5f5f')
        self.user2 = User.objects.create_user(username='ssssssss', email='test_@test.com',
                                              password='000000555555ddd5f5f')
        self.profile = UserProfile.objects.create(user=self.user, department=self.dep, faculty=self.fac)
        self.profile2 = UserProfile.objects.create(user=self.user2, department=self.dep, faculty=self.fac)
        self.post = UserPost.objects.create(title='dddd', topic=self.topic, user=self.user)
        self.comment = UserComment.objects.create(post=self.post, user=self.user, content='sdadadsrftsdgd')
        self.post2 = UserPost.objects.create(title='dddd', topic=self.topic2, user=self.user)
        self.comment2 = UserComment.objects.create(post=self.post2, user=self.user, content='fsdddasdasdasdasdasdas')
        self.profile.topics.add(self.topic)
        self.profile.topics.add(self.topic2)

    def test_insert_new_post(self):
        # Setup test
        data = {
            'user': self.user,
            'topic': self.topic,
            'title': 'new poooost',
            'content': 'sbsdfl;sdlkfjslkfjsdklfsjdlfkjsdflsjpasfack34o34=-pgd  -wo0=39  dfs ',
        }

        # Exercise test
        url = reverse('api_add_post')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.get(url, data=data)
        posts_in_db = UserPost.objects.all().count()

        # Assert test
        self.assertTrue(posts_in_db > 0)

    def test_insert_new_comment(self):
        # Setup test
        data = {
            'user': self.user,
            'post': self.post,
            'content': 'sbsdfl;sdlkfjslkfjsdklfsjdlfkjsdflsjpasfack34o34=-pgd  -wo0=39  dfs ',
        }

        # Exercise test
        url = reverse('api_add_comment')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.post(url, data=data)
        posts_in_db = UserComment.objects.all()

        # Assert test
        self.assertTrue(posts_in_db.count() > 0)
        self.assertIn(posts_in_db.first(), self.post.comments.all())

    def test_delete_comment(self):
        # Setup test
        staff_user = User.objects.create_superuser(username='staff', password='asdlasjdla239uas-38',
                                                   email='sdasd@sds.com')
        staff_profile = UserProfile.objects.create(user=staff_user, department=self.dep, faculty=self.fac)
        staff_profile.topics.add(self.topic)
        data = {'comment_id': self.comment.id}

        # Exercise test
        url = reverse('api_delete_comment')
        request = self.client.login(username="staff", password="asdlasjdla239uas-38")
        request = self.client.post(url, data=data)
        posts_in_db = UserComment.objects.filter(status=1)

        # Assert test
        self.assertTrue(posts_in_db.count() == 1)
        self.assertIn(self.comment, self.post.comments.all())

    def test_get_post_comments(self):
        # Setup test
        data = {'post_id': self.post.id}

        # Exercise test
        url = reverse('api_get_post_comments')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.get(url, data=data)

        # Assert test
        self.assertTrue(request.data)

    def test_get_post_comments_without_data(self):
        # Setup test
        data = {}

        # Exercise test
        url = reverse('api_get_post_comments')
        request = self.client.login(username="ibrahemmmmm", password="000000555555ddd5f5f")
        request = self.client.get(url, data=data)

        # Assert test
        self.assertFalse(request.data)
