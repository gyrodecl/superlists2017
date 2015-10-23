from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session


class MyListsTest(FunctionalTest):
    
    def create_pre_authenticated_session(self, email):
        #user = User.objects.create(email=email)
        #session = SessionStore()
        #session[SESSION_KEY] = user.pk
        #session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        #session.save()
        if self.against_staging:
            #session_key = create_session_on_server(self.server_host, email)
            session_key = create_sesion_on_server('tdd-lists-staging',email)
        else:
            session_key = create_pre_authenticated_session(email)
        
        #to set a cookie we need to first visit the domain
        # 404 pages load the quickest!
        self.browser.get(self.server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))
    
    #see if our pre-authentication function works
    #will it see our user's cookie
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        
        self.browser.get(self.server_url + '/lists/')
        self.wait_to_be_logged_out(email)
        
        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        
        self.browser.get(self.server_url + '/lists/')
        self.wait_to_be_logged_in(email)
    
    
