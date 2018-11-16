$(document).ready(function() {
    $('#confirmar').click(function() {
        console.log("test");
        $.get("/reconhecer", function(data, status) {
            alert("DAta: " + data + "\nstatus: " + status)
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