import datetime
import json
import os
import random
from shutil import rmtree
from timeit import default_timer as timer

import numpy as np
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.authtoken.models import Token

from Api.models import Message
from Data.models import Profile, UserData, Version

User = get_user_model()


class ApiDataDeleteTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='username1', password='password')
        rmtree(os.path.join(settings.BASE_DIR, 'media_temp'), ignore_errors=True)

    def tearDown(self):
        rmtree(os.path.join(settings.BASE_DIR, 'media_temp'), ignore_errors=True)

    @override_settings(MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'media_temp/'))
    def test_data_delete_correct_user(self):
        """
        Tests if a logged in user can delete its own data with a POST request to the API
        """

        # Generating mock file
        rand_score = random.randint(1, 999)
        mock_file = np.ndarray(shape=[rand_score, 2])
        score = mock_file.shape[0]

        self.assertEqual(rand_score, mock_file.shape[0])

        # Adding some data to the user
        user_data = UserData(user=self.user1, score=score, processed=False, version=None)
        user_data.file = SimpleUploadedFile('training_data.npy', bytes(mock_file))
        user_data.save()

        # Testing if data was added successfully
        self.assertEqual(Profile.objects.get(user=self.user1).score, rand_score)

        # Logging the user in
        self.client.login(username='username1', password='password')

        # Preparing data to send
        data = {'data_id': UserData.objects.get(user=self.user1).pk}

        # Requesting data deletion
        response = self.client.post(reverse('api data delete'), data=data)

        # Data should be deleted, so score must have gone to 0 (as it was the only data for that user)
        self.assertEqual(response.content, b'{"success": true}')
        self.assertEqual(Profile.objects.get(user=self.user1).score, 0)

    @override_settings(MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'media_temp/'))
    def test_data_delete_wrong_user(self):
        """
        Tests if a logged in user can delete data of another user with a POST request to the API
        """

        # Generating mock file
        rand_score = random.randint(1, 999)
        mock_file = np.ndarray(shape=[rand_score, 2])
        score = mock_file.shape[0]

        self.assertEqual(rand_score, mock_file.shape[0])

        # Adding some data to the user
        user_data = UserData(user=self.user1, score=score, processed=False, version=None)
        user_data.file = SimpleUploadedFile('training_data.npy', bytes(mock_file))
        user_data.save()

        # Testing if data was added successfully
        self.assertEqual(Profile.objects.get(user=self.user1).score, rand_score)

        # Creating other user
        self.user2 = User.objects.create_user(username='username2', password='password')

        # Logging the other user in
        self.client.login(username='username2', password='password')

        # Preparing data to send
        data = {'data_id': UserData.objects.get(user=self.user1).pk}

        # Requesting data deletion
        response = self.client.post(reverse('api data delete'), data=data)

        # Data from the other user should not be deleted, so score must remain the same
        self.assertEqual(response.content, b'{"success": false, "error": "Not authorized"}')
        self.assertEqual(Profile.objects.get(user=self.user1).score, rand_score)

    @override_settings(MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'media_temp/'))
    def test_data_delete_invalid_id(self):
        """
        Tests if a invalid id error message is being returned
        """

        # Generating mock file
        rand_score = random.randint(1, 999)
        mock_file = np.ndarray(shape=[rand_score, 2])
        score = mock_file.shape[0]

        self.assertEqual(rand_score, mock_file.shape[0])

        # Adding some data to the user
        user_data = UserData(user=self.user1, score=score, processed=False, version=None)
        user_data.file = SimpleUploadedFile('training_data.npy', bytes(mock_file))
        user_data.save()

        # Testing if data was added successfully
        self.assertEqual(Profile.objects.get(user=self.user1).score, rand_score)

        # Logging the user in
        self.client.login(username='username1', password='password')

        # Requesting data deletion
        data = {'data_id': 'invalid-id'}
        response = self.client.post(reverse('api data delete'), data=data)

        # Data should have been deleted
        self.assertEqual(response.content, b'{"success": false, "error": "Invalid id"}')
        self.assertEqual(Profile.objects.get(user=self.user1).score, rand_score)

    def test_data_delete_GET(self):
        """
        Tests if GET request returns a 404 page
        """

        response = self.client.get(reverse('api data delete'))
        self.assertEqual(response.status_code, 404)


class ApiTokenResetTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='username1', password='password')

    def test_token_reset_correct_user(self):
        """
        Tests if a logged in user can reset its own token with a POST request to the API
        """

        # Getting user token
        token = Token.objects.get(user=self.user1).key

        # Logging the user in
        self.client.login(username='username1', password='password')

        # Calling the API
        data = {'token': token}
        response = self.client.post(reverse('api reset token'), data=data)

        response_dict = json.loads(response.content)
        new_token = Token.objects.get(user=self.user1).key

        # Making sure token was changed
        self.assertTrue(response_dict['success'])
        self.assertTrue(token != new_token)
        self.assertEqual(response_dict['token'], new_token)

    def test_token_reset_wrong_user(self):
        """
        Tests if a logged in user can reset token of another user with a POST request to the API
        """

        self.user2 = User.objects.create_user(username='username2', password='password')

        # Getting user tokens
        token1 = Token.objects.get(user=self.user1).key
        token2 = Token.objects.get(user=self.user2).key

        # Logging the user in
        self.client.login(username='username1', password='password')

        # Calling the API with the token of another user
        data = {'token': token2}
        response = self.client.post(reverse('api reset token'), data=data)

        response_dict = json.loads(response.content)

        # Making sure token was NOT changed
        self.assertFalse(response_dict['success'])
        self.assertEqual(Token.objects.get(user=self.user1).key, token1)
        self.assertEqual(Token.objects.get(user=self.user2).key, token2)

    def test_token_reset_invalid_key(self):
        """
        Tests if a logged in user can reset its own token with a POST request to the API
        """

        # Getting user token
        token = 'invalid-token'
        orig_token = Token.objects.get(user=self.user1).key

        # Logging the user in
        self.client.login(username='username1', password='password')

        # Calling the API
        data = {'token': token}
        response = self.client.post(reverse('api reset token'), data=data)

        new_token = Token.objects.get(user=self.user1).key

        # Making sure token was changed
        self.assertEqual(response.content, b'{"success": false}')
        self.assertTrue(orig_token == new_token)

    def test_token_reset_GET(self):
        """
        Tests if GET request returns a 404 page
        """

        response = self.client.get(reverse('api reset token'))
        self.assertEqual(response.status_code, 404)


class ApiValidateTokenTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='username1', password='password')

    def test_validate_token_valid(self):
        """
        Tests if token validation for correct token is invalid
        """
        token = Token.objects.get(user=self.user1).key

        header = {"HTTP_AUTHORIZATION": f"Token {token}"}

        response = self.client.post(reverse('api validate token'), **header)
        response_dict = json.loads(response.content)

        self.assertTrue(response_dict['valid-token'])
        self.assertEqual(response_dict['username'], self.user1.username)

    def test_validate_token_invalid(self):
        """
        Tests if token validation for incorrect token is invalid
        """

        header = {"HTTP_AUTHORIZATION": "Token invalid-token"}
        data = {'username': f'{self.user1.username}'}

        response = self.client.post(reverse('api validate token'), data=data, **header)

        self.assertEqual(response.content, b'{"valid-token": false}')


    def test_validate_token_invalid_missing_info(self):
        """
        Tests if token returns error for missing info
        """
        data = {'username': f'{self.user1.username}'}

        response = self.client.post(reverse('api validate token'), data=data)

        self.assertEqual(response.content,
                         b'{"valid-token": false, "error": "No auth token or username in POST request"}')

    def test_validate_token_GET(self):
        """
        Tests if GET request returns a 404 page
        """

        response = self.client.get(reverse('api validate token'))
        self.assertEqual(response.status_code, 404)


class ApiScoreCheckTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='username1', password='password')

    def test_score_check_token_valid(self):
        """
        Tests score is being checked correctly when valid credentials are given
        """
        token = Token.objects.get(user=self.user1).key

        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {'username': f'{self.user1.username}'}

        response = self.client.post(reverse('api score'), data=data, **header)

        self.assertEqual(response.content, b'{"score": 0}')

        user1_profile = Profile.objects.get(user=self.user1)
        user1_profile.score = 1000
        user1_profile.save()

        response = self.client.post(reverse('api score'), data=data, **header)

        self.assertEqual(response.content, b'{"score": 1000}')

    def test_score_check_token_invalid(self):
        """
        Tests if score is 0 with invalid credentials.

        To test this, first the user's score is changed and then we make a POST
        request to check if it is still 0, which means invalid credentials were
        used
        """

        arbitrary_score = 1000

        header = {"HTTP_AUTHORIZATION": f"Token invalid-token"}
        data = {'username': f'{self.user1.username}'}

        user1_profile = Profile.objects.get(user=self.user1)
        user1_profile.score = arbitrary_score
        user1_profile.save()

        self.assertEqual(user1_profile.score, arbitrary_score)

        response = self.client.post(reverse('api score'), data=data, **header)

        self.assertEqual(response.content, b'{"score": 0}')

    def test_score_check_token_wrong_user(self):
        """
        Tests if score is 0 using token from another user

        To test this, first the user's score is changed and then we make a POST
        request to check if it is still 0, which means wrong token was used
        """

        arbitrary_score = 1000

        self.user2 = User.objects.create_user(username='username2', password='password')

        token = Token.objects.get(user=self.user1).key

        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {'username': f'{self.user2.username}'}

        user1_profile = Profile.objects.get(user=self.user1)
        user1_profile.score = arbitrary_score
        user1_profile.save()

        self.assertEqual(user1_profile.score, arbitrary_score)

        response = self.client.post(reverse('api score'), data=data, **header)

        self.assertEqual(response.content, b'{"score": 0}')


class ApiVersionControlTest(TestCase):

    def test_version_control_empty(self):
        """
        Tests if empty version control json response is being delivered
        """
        response = self.client.get(reverse('api version control'))
        self.assertEqual(response.content, b'{"Version Control": []}')

    def test_version_control_populated(self):
        """
        Tests if populated version control json response is being delivered
        """

        self.version = Version.objects.create(
            version=1.0,
            log="Version for testing!",
            date=datetime.datetime.today(),
            critical=False
        )

        response = self.client.get(reverse('api version control'))
        response_dict = json.loads(response.content)['Version Control'][0]

        self.assertEqual(response_dict['Version'], '1.0')
        self.assertEqual(response_dict['Changes'], 'Version for testing!')
        self.assertEqual(response_dict['Date'], str(datetime.date.today()))
        self.assertEqual(response_dict['Critical'], False)


class ApiBugReportTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='username1', password='password')
        self.version = Version.objects.create(
            version=1.0,
            log="Version for testing!",
            date=datetime.datetime.today(),
            critical=False
        )

    def test_bug_report_valid(self):
        """
        Tests if a valid bug report is being accepted
        """

        token = Token.objects.get(user=self.user1)

        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            'user': f'{self.user1.username}',
            'message': 'Testing the bug reporting utility!',
            'version': self.version.version
        }

        response = self.client.post(reverse('api bug report'), data=data, **header)

        self.assertEqual(response.content, b'{"success": true}')
        self.assertTrue(Message.objects.filter(user=self.user1).exists())

    def test_bug_report_invalid_version(self):
        """
        Tests if a invalid bug report (with wrong version)) is being rejected
        """

        token = Token.objects.get(user=self.user1)

        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            'user': f'{self.user1.username}',
            'message': 'Testing the bug reporting utility!',
            'version': 2.0
        }

        response = self.client.post(reverse('api bug report'), data=data, **header)

        self.assertEqual(response.content, b'{"success": false, "error": "User or version not found on database"}')
        self.assertFalse(Message.objects.filter(user=self.user1).exists())

    def test_bug_report_invalid_token(self):
        """
        Tests if a invalid bug report (invalid token) is being rejected
        """

        header = {"HTTP_AUTHORIZATION": f"Token invalid-token"}
        data = {
            'user': f'{self.user1.username}',
            'message': 'Testing the bug reporting utility!',
            'version': self.version.version
        }

        response = self.client.post(reverse('api bug report'), data=data, **header)

        self.assertEqual(response.content, b'{"success": false, "error": "User or version not found on database"}')
        self.assertFalse(Message.objects.filter(user=self.user1).exists())

    def test_bug_report_wrong_token(self):
        """
        Tests if a invalid bug report (using token from another user) is being rejected
        """
        self.user2 = User.objects.create_user(username='username2', password='password')

        token = Token.objects.get(user=self.user2)
        header = {"HTTP_AUTHORIZATION": f"Token {token}"}

        data = {
            'user': f'{self.user1.username}',
            'message': 'Testing the bug reporting utility!',
            'version': self.version.version
        }

        response = self.client.post(reverse('api bug report'), data=data, **header)

        self.assertEqual(response.content, b'{"success": false, "error": "Wrong formatting or missing information"}')
        self.assertFalse(Message.objects.filter(user=self.user1).exists())
        self.assertFalse(Message.objects.filter(user=self.user2).exists())

    def test_bug_report_missing_info(self):
        """
        Tests if a invalid bug report (with missing message) is being rejected
        """

        token = Token.objects.get(user=self.user1)

        header = {"HTTP_AUTHORIZATION": f"Token {token}"}
        data = {
            'user': f'{self.user1.username}',
            'version': self.version.version
        }

        response = self.client.post(reverse('api bug report'), data=data, **header)

        self.assertEqual(response.content, b'{"success": false, "error": "Wrong formatting or missing information"}')
        self.assertFalse(Message.objects.filter(user=self.user1).exists())

    def test_bug_report_GET(self):
        """
        Tests if GET request returns a 404 page
        """

        response = self.client.get(reverse('api bug report'))
        self.assertEqual(response.status_code, 404)
