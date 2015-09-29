from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
    
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Edith goes to our site
        self.browser.get('http://localhost:8000')

        #sees the title
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        #invited to enter a to-do item straight away
        #she types "Buy peacock feathers" into text box

        #when she hits enter, the page updates, and now the page lists
        #"1: Buy peacock feathers" as an item in a to-do list

if __name__ == '__main__':
    unittest.main(warnings='ignore')