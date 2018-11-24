$(document).ready(function() {
    $('.modal').modal({
        dismissible: false, // Modal can be dismissed by clicking outside of the modal
        onOpenStart: modal => { // Callback for Modal open. Modal and trigger parameters available.
            $('#modal1 .modal-content .preloader-wrapper').addClass("active");
            $('#modal1 .modal-content h4').text("Reconhecendo");
            $('#modal1 .modal-content p').text("");
        },
      }
    );

    $('#confirmar').click(function() {
        $.get("/reconhecer", function(data, status) {
            dataJson = JSON.parse(data);
            console.log(dataJson);
            $('#modal1 .modal-content .preloader-wrapper').removeClass("active");

            if(dataJson.id != 0) {
                $('#modal1 .modal-content h4').text("Reconhecido");
            } else {
                $('#modal1 .modal-content h4').text("Desconhecido");
            }

            $('#modal1 .modal-content p').append("<b>ID:</b> " + dataJson.id);
            $('#modal1 .modal-content p').append("<br><b>Nome:</b> " + dataJson.nome);
            $('#modal1 .modal-content p').append("<br><b>E-mail:</b> " + dataJson.email);
        });
    });

    $('#pessoa-form').submit(function() {
        let formData = new FormData(this);

        $.ajax({
            url: "/cadastro",
            type: "POST",
            data: formData,
            success: function(data) {
                alert(data);
            },
            cache: false,
            contentType: false,
            processData: false,
            xhr: function() {
                let myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload) {
                    myXhr.upload.addEventListener('progress', function() {

                    }, false);
                }
                return myXhr;
            }
        });
    });
});