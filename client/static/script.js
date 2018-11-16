var botaoConfirmar = document.getElementById("confirmar");

botaoConfirmar.onclick = function() {
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4 && xhr.status==200) {
            alert(xhr.responseText);
        }
    }
    xhr.open("GET", "/reconhecer");
    xhr.send();
};