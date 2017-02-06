function login(data) {

  myApp.showPreloader();

  $$.post({
    url: '',
    data: data,
    success: function (data) {

      myApp.closeModal();

      if (data.exist = 0) {
        myApp.alert('Telefone não cadastrado.', 'Login');
      } else {

        setTimeout(function () {
          myApp.closeNotification(".notifications");
        }, 3000);

        myApp.addNotification({
          title: 'Bem-vindo Fulano de Tal - ' + localStorage.getItem("username")
        });
      }

    },
    error: function (data) {
      myApp.alert('Falha ao efetuar login.', 'Login');
    }

  });

}
