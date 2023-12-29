
let videos = [];
let video_player;
let short;

document.addEventListener('click', function(e) {
    console.log('Кликнуто на: ', e.target);

    video_player.muted = false;
});

function init_shorts(){
    video_player = document.getElementById('video-player');

    load_new_video();
}

function load_new_video(){
    fetch(BASE_URL + "get-short/")
        .then(response => response.json())
        .then(data => {

            data.brand = JSON.parse(data.brand)[0];
            data.comments = JSON.parse(data.comments);
            short = data;

            console.log(short)
            play_video(data.short);

            refresh();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function play_video(short){
    video_player.src = short.url;
    video_player.play();
}

function refresh(){
    console.log(short.title);

    document.getElementById('title').innerHTML = short.short.title;
    document.getElementById('description').innerHTML = short.short.description;
    document.getElementById('brand-title').innerHTML = short.brand.fields.title;
    document.getElementById('avatar').src = 'http://127.0.0.1:8000/media/' + short.brand.fields.avatar;
}

function next(){
    load_new_video();
}

function getCsrfToken() {
    const csrfTokenElement = document.getElementsByName('csrfmiddlewaretoken')[0];
    return csrfTokenElement ? csrfTokenElement.value : '';
}