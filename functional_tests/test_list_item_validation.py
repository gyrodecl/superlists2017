from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
import sys

class ItemValidationTest(FunctionalTest):      
    #ch10
    #@unittest.skip
    def test_cannot_add_empty_list_items(self):
        # Edith goes to home page tries to submit empty list item
        # hits enter on empty input box
    
        # The home page refreshes, and there is error message saying
        # that list items cannot be blank
        
        # She tries again with some text for the itmem, which now works
        
        # She tries to submit a second blank list item
        
        # She receives a similar warning on the list page
        
        #And she can correct it by filling some text in
        self.fail('write me!')