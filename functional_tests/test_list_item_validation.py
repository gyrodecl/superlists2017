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
        self.browser.get(self.server_url + '/lists/')
        inputbox = self.get_item_input_box()
        inputbox.send_keys(Keys.ENTER)
    
        # The home page refreshes, and there is error message saying
        # that list items cannot be blank
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        
        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')
        
        # She tries to submit a second blank list item
        self.get_item_input_box().send_keys('\n')
        
        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "You can't have an empty list item")
        
        #And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')