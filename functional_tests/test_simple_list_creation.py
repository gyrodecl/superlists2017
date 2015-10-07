from .base import FunctionalTest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):
 
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Edith goes to our site
        #'lists/'
        print(self.server_url + '/lists/')
        self.browser.get(self.server_url + '/lists/')

        #sees the title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #invited to enter a to-do item straight away
        #she types "Buy peacock feathers" into text box
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #when she hits enter, the page updates, and now the page lists
        #"1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        #since this is the home page, she has created a new list
        #with its own URL;
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        
        #import time
        #time.sleep(10)       
        #now look at the table of results
        self.check_for_row_in_list_table("1: Buy peacock feathers")
    
        #there's still a text box inviting her to add another item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        
        #page updates again and shows both items on her list
        self.check_for_row_in_list_table("1: Buy peacock feathers")
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        
        #Now a new user, Francis, comes along to the site.
        ##We use a new browser session to make sure no info
        #of Edith's is coming through from cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        #Francis visits the home page. no sign of edit's list
        self.browser.get(self.server_url + '/lists/')
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        
        #Francis starts a new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        
        #Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        
        #Again, no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        
        #satisfied they go back to sleep     
        self.fail('Finish the test!')