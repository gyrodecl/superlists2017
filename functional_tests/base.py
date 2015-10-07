from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
import sys

#ch.10 Refactor Functional Tests into Many Files
class FunctionalTest(StaticLiveServerTestCase):
    
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:  
            if 'liveserver' in arg:  
                cls.server_url = 'http://' + arg.split('=')[1]  
                return  
        super().setUpClass()  
        cls.server_url = cls.live_server_url
    
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
        
    #helper method
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        

'''
#don't need this anymore since using django test runner
if __name__ == '__main__':
    unittest.main(warnings='ignore')
'''