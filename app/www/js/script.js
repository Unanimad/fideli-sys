function do_login() {
  var login_form = $('#login_form').serializeArray()[0];

  if (login_form.value == "" || login_form.value == null) {
    myApp.alert('Por favor, preencha o campo do telefone.', 'Login');
  } else {

    localStorage.setItem("username", login_form.value);
    
    login($('#login_form').serialize());

  }

}

function do_logoff() {
  myApp.confirm('Tem certeza que deseja sair?', 'Sair', function () {
        logoff();
    });
}

function logoff() {
  localStorage.removeItem("username");
}
