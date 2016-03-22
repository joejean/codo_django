import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()

    def test_can_view_home_page(self):
        # Check Home Page of Codo 
        self.browser.get('http://localhost:8000')
        # See Codo in the Title
        self.assertIn('Codo', self.browser.title)
    # User can go to the sign up page in order to create an account
    def test_can_signup(self):
        self.browser.get('http://localhost:8000/accounts/signup')
        first_name_input = self.browser.find_element_by_name('first_name')
        last_name_input = self.browser.find_element_by_name('last_name')
        email_input = self.browser.find_element_by_name('email')
        password1_input = self.browser.find_element_by_name('password1')
        password2_input = self.browser.find_element_by_name('password2')
        first_name_input.send_keys('Joe')
        last_name_input.send_keys('Jean')
        email_input.send_keys('joe@nyu.edu')
        #password1_input.send_keys("mytest1234")
        password2_input.send_keys("mytest1234")
        password2_input.submit()
        







if __name__ == "__main__":
    unittest.main()