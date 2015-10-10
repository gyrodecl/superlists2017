from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest
import sys

class ItemValidationTest(FunctionalTest):
    
    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')
    
    
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
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")
        
        # She tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')
        
        # She tries to submit a second blank list item
        self.get_item_input_box().send_keys('\n')
        
        # She receives a similar warning on the list page
        self.check_for_row_in_list_table('1: Buy milk')
        error = self.get_error_element()
        self.assertEqual(error.text, "You can't have an empty list item")
        
        #And she can correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
        
        
    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        self.browser.get(self.server_url + '/lists/')
        self.get_item_input_box().send_keys("Buy wellies\n")
        self.check_for_row_in_list_table('1: Buy wellies')
        
        #she accidentally tries to enter a duplicate item
        self.get_item_input_box().send_keys("Buy wellies\n")
        
        #she sees a helpful error message
        self.check_for_row_in_list_table('1: Buy wellies')
        error = self.get_error_element()
        self.assertEqual(error.text, "You've already got this in your list")
    
    
    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.server_url + '/lists/')
        self.get_item_input_box().send_keys('\n')
        error = self.get_error_element()
        self.assertTrue(error.is_displayed())
        
        #she starts typing in the input box to clear the error
        self.get_item_input_box().send_keys('a')
        
        # She is pleased to see the error message disappears
        error = self.get_error_element()
        self.assertFalse(error.is_displayed())
    
    