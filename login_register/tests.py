from django.test import TestCase
from django.contrib.auth.models import User


class RegisterPageViewTest(TestCase):

  def test_user_gets_created(self):
    """
    Check if a user gets created or not on the register page.
    """
    register_url = '/register/'
    login_url = '/login/'
    data = {'username': 'tim', 'first_name': 'tim wd', 'email': 'tim@gmail.com', 'password1': 'django11', 'password2': 'django11'}
    response = self.client.post(register_url, data, follow=True)
    status_code = response.status_code
    user_count = User.objects.all().count()
    print('PATH_INFO_REGISTER: ', response.request)
    redirect_path = response.request.get('PATH_INFO')
    print('REDIRECT_REGISTER: ', redirect_path)
    user1 = User.objects.get(username="tim")    
    print('INSTAGRAM_USER: ', user1.instagramuser)

    self.assertEqual(status_code, 200) # page is found
    self.assertEqual(user_count, 1) # user exists
    self.assertEqual(redirect_path, login_url) # redirect to the login page


class LoginPageViewTest(TestCase):

  def setUp(self):
    # user3 = User.objects.create(username='timpy', email='timpy@gmail.com', password='python22')
    # self.user3 = user3

    register_url = '/register/'
    data = {'username': 'tim', 'first_name': 'tim wd', 'email': 'tim@gmail.com', 'password1': 'django11', 'password2': 'django11'}
    response = self.client.post(register_url, data, follow=True)
    user4 = User.objects.get(username="tim")
    self.user4 = user4


  def test_user_logsin_to_site(self):
    """
    Check if a user logs in into the site or not.
    """
    user_page_url = f'/user_page/{self.user4.id}/'
    login_url = '/login/'
    data = {'username': 'tim', 'password': 'django11'}
    response = self.client.post(login_url, data, follow=True)
    status_code = response.status_code
    self.assertEqual(status_code, 200) # page is found

    user_count = User.objects.all().count()
    print('COUNT: ', user_count)
    self.assertEqual(user_count, 1) # user exists

    print('RESPONSE_LOGIN: ', response.request)
    redirect_path = response.request.get('PATH_INFO')
    print('REDIRECT_LOGIN: ', redirect_path)
    self.assertEqual(redirect_path, user_page_url) # redirect to the user page