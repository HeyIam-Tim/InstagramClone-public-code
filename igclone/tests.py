from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import InstagramUser


# # Create your tests here.
# class FollowingPageViewTests(TestCase):
#   def test_user_gets_back_to_the_current_page(self):
#     """
#     The logged-in user go back to the FollowingPage after they unfollows a certain user(user whom the logged-in user follows to).
#     """
#     # john = User.objects.get(id=43)
#     # brad = User.objects.get(id=36)
#     # user1 = User.objects.create(pk=11, username='John')
#     user1 = User.objects.create(id=2, username='John', first_name='John Smith', email='cat@gmail.com', password='woll1111')
#     # user2 = User.objects.create(username='Will')
#     # response = self.client.get(reverse('follocwing' '1'))
#     # print('RESPONSE', response.user)
#     # ig_user = InstagramUser.objects.create(user=user1)
#     ig_user1 = InstagramUser(user=user1)
#     ig_user1.save()
#     # ig_user2 = InstagramUser.objects.create(user=user2)
#     # self.assertQuerysetEqual(user1.username, 'john')
#     # self.assertEqual(user1.username, 'john')
#     self.assertEqual(ig_user1.user.username, 'john')
#     # self.assertIs(user1, True)
#     # ig_user1.following.add(ig_user2)
#     # ig_user2.follower.add(ig_user1)
#     # request = self.client.get(reverse('following'))
#     # request.method = "POST"
#     response = self.client.get(reverse('login_register:login'))
#     self.assertEqual(response.status_code, 200)




# class 
