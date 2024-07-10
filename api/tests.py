from django.test import TestCase

from ttwo.api.models import Organisation
from ttwo.myauth.models import User

# Create your tests here.
class OrganisationTestCase(TestCase):
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.organisation = Organisation.objects.create(name='Test Org')
        self.organisation.users.add(self.user1)
    
    def test_user_access_to_organisation(self):
        self.assertIn(self.user1, self.organisation.users.all())
        self.assertNotIn(self.user2, self.organisation.users.all())
