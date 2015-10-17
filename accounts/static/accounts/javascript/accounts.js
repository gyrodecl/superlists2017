var initialize = function(navigator, user, token, urls) {
    console.log(navigator);
    $('#id_login').click(function(event) {
            navigator.id.request(); 
    });
    
    navigator.id.watch({
        loggedInUser: user,
        onlogin: function(assertion) {
            $.post(urls.login, {'assertion': assertion, 'csrfmiddlewaretoken': token})
             .done(function(){window.location.reload();})
             .fail(function() {navigator.id.logout();});
        },
        onlogout: function() {
            $.post(urls.logout)
        }
    });
};
    
window.Superlists = {
    'Accounts': {
        'initialize': initialize
    }
};