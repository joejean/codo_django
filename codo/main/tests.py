from django.test import TestCase
from codo.models import Organizer, Campaign, BankAccount
from django.contrib.auth.models import User


# Tests Models
class Test_Models(TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
      

    def no_user_in_db_test(self):
        users = User.query.all()
        self.assertEqual(users, [])

    def add_user_to_db_test(self):
        user = models.User("Joe", "Jean", "joe@hotmail.com", "testpassword")
        db.session.add(user)
        db.session.commit()
        user = models.User.query.filter_by(first_name="Joe").first()
        self.assertEqual(user.first_name, "Joe")
        self.assertEqual(user.email, "joe@hotmail.com")
        self.assertTrue(user.verify_password("testpassword"))
        self.assertFalse(user.verify_password("Testpassword"))

    def delete_user_test(self):
        user = models.User("Joe", "Jean", "joe@hotmail.com", "testpassword")
        db.session.add(user)
        db.session.commit()
        user = models.User.query.filter_by(first_name="Joe").first()
        db.session.delete(user)
        db.session.commit()
        user = models.User.query.filter_by(first_name="Joe").first()
        self.assertIsNone(user)

    def user_string_repr_test(self):
        user = models.User("Joe", "Jean", "joe@hotmail.com", "testpassword")
        self.assertEqual(str(user), "<User: Joe Jean>")

    def organizer_add_and_fk_integrity_test(self):
        user = models.User("Joe", "Jean", "joe@hotmail.com", "testpassword")
        db.session.add(user)
        db.session.commit()
        organizer = models.Organizer(user.id, 21, 4, 1988, "ak122939393")
        db.session.add(organizer)
        db.session.commit()
        organizer_joe = models.Organizer.query.filter_by(user_id=user.id).first()
        self.assertEqual(organizer_joe.user_id, user.id)
        self.assertEqual(organizer_joe.user.first_name, "Joe")
        self.assertEqual(organizer_joe.user.last_name, "Jean")
        self.assertEqual(organizer_joe.dob_month, 4)
        self.assertEqual(organizer_joe.dob_day, 21)
        self.assertEqual(organizer_joe.dob_year, 1988)
        self.assertEqual(organizer_joe.stripe_account_id, "ak122939393")

    def campaign_add_and_fk_integrity_test(self):
        user = models.User("Joe", "Jean", "joe@hotmail.com", "testpassword")
        db.session.add(user)
        db.session.commit()
        organizer = models.Organizer(user.id, 21, 4, 1988, "ak122939393")
        db.session.add(organizer)
        db.session.commit()
        campaign = models.Campaign(organizer.id, "Test Campaign", "Really Goooood\
            campaign for the people", "https://www.youtube.com/watch?v=KEI4qSrkPAs&li",
            "http://www.wellclean.com/wp-content/themes/artgallery_3.0/images/car3.png")
        db.session.add(campaign)
        db.session.commit()
        campaign_test = models.Campaign.query.filter_by(organizer_id=organizer.id)\
            .first()
        self.assertIsNotNone(campaign_test)
        self.assertEqual(campaign_test.organizer_id, organizer.id)
        self.assertEqual((campaign_test.description).index("Really"), 0)

    def bankaccount_add_and_fk_integrity_test(self):
        user = models.User("Joe", "Jean", "joe@hotmail.com", "testpassword")
        db.session.add(user)
        db.session.commit()
        bank_account = models.BankAccount(user.id, "US", "usd", "hshsh219199sjs22")
        db.session.add(bank_account)
        db.session.commit()
        bank_accnt = models.BankAccount.query.filter_by(country="US").first()
        self.assertIsNotNone(bank_accnt)
        self.assertEqual(bank_accnt.country, "US")
        self.assertEqual(bank_accnt.currency, "usd")
        self.assertEqual(bank_accnt.account_number, "hshsh219199sjs22")
        self.assertEqual(len(user.bank_accounts), 1)

if __name__ == "__main__":
    unittest.main()


# Tests Views 


