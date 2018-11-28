$(document).ready(function() {
    $('.modal').modal({
        dismissible: false,
        onOpenStart: modal => {
            $('#modal1 .modal-content .preloader-wrapper').addClass("active");
            $('#modal1 .modal-content h4').text("Reconhecendo");
            $('#modal1 .modal-content p').text("");
            $('#modal1 .modal-content img').css({"display": "none"});
            $('#modal1 .modal-content img').attr('src', "data:image/png;base64, ");
        },
      }
    );

    $('#confirmar').click(function() {
        $.get("/reconhecer", function(data, status) {
            dataJson = data
            console.log(dataJson);
            $('#modal1 .modal-content .preloader-wrapper').removeClass("active");

            if(dataJson.id != 0) {
                $('#modal1 .modal-content img').css({"display": "block"});
                $('#modal1 .modal-content h4').text("Reconhecido");
                $('#modal1 .modal-content img').attr('src', "data:image/png;base64, " + dataJson["foto_b64"]);
                M.toast({html: "Reconhecido.", displayLength: 5000})
            } else {
                $('#modal1 .modal-content h4').text("Desconhecido");
                M.toast({html: "Não reconhecido.", displayLength: 5000})
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
                M.toast({html: data, displayLength: 5000})
            },
            error: function(req, text, errorThrown) {
                M.toast({html: req.responseText, displayLength: 5000});
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