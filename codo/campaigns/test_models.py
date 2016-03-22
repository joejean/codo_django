from datetime import date
import tempfile
from django.test import TestCase
from .models import Organizer, Campaign, Reward
from django.contrib.auth.models import User


# Test Models
class Test_Organizer(TestCase):

    def setUp(self):
        self.user = User.objects.get_or_create(first_name="Joe", last_name="Jean", \
            email="joeclef@hotmail.com", password="pol123456")
        Organizer.objects.get_or_create(\
                    user=self.user[0], country="HT",\
                    phone_number="+9710500000000",\
                    short_bio="Cool Software",\
                    profile_picture=tempfile.NamedTemporaryFile(suffix=".jpg").name,\
                    facebook_url ="http://www.facebook.com/joe3.jean",\
                    twitter_url ="http://www.twitter.com/joe",\
                    website_url ="http://www.joejean.net",\
                    dob = date(1988,4,21)
                    )

    def test_one_organizer_exists_in_db(self):
        organizers = Organizer.objects.all()
        self.assertEqual(len(organizers), 1)

    def test_organizer_has_first_name_of_linked_user(self):
        organizer = Organizer.objects.filter(user__first_name="Joe")
        self.assertEqual(organizer[0].user.first_name, "Joe" )

    def test_organizer_str(self):
        organizer = Organizer.objects.all()
        self.assertEqual(str(organizer[0]), "<Organizer: Joe>")

    def test_orginazer_get_wepay_access_token(self):
        organizer = Organizer.objects.all()
        self.assertIsNone(organizer[0].get_wepay_access_token())
    
    def test_orginazer_get_wepay_user_id(self):
        organizer = Organizer.objects.all()
        self.assertIsNone(organizer[0].get_wepay_user_id())
    
    def test_orginazer_get_wepay_account_id(self):
        organizer = Organizer.objects.all()
        self.assertIsNone(organizer[0].get_wepay_account_id())
    
    def test_orginazer_get_wepay_account_uri(self):
        organizer = Organizer.objects.all()
        self.assertIsNone(organizer[0].get_wepay_account_uri())


class TestReward(TestCase):
    pass

class TestCampaign(TestCase):
    pass



   






