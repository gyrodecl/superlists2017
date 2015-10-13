var initialize = function(navigator) {
    console.log(navigator);
    $('#id_login').click(function(event) {
            navigator.id.request(); 
    });
};
    
window.Superlists = {
    'Accounts': {
        'initialize': initialize
    }
};