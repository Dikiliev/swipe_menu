function get_text(filename, id){
    fetch(filename)
        .then(response => response.text())
        .then(text => {
            document.getElementById(id).innerHTML = text;
        })
        .catch(error => {
            console.error('Ошибка при загрузке текста:', error);
            document.getElementById(id).innerHTML = 'Ошибка при загрузке текста.'
        });
}