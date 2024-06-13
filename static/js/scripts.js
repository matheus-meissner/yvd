document.getElementById('download-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const url = document.getElementById('url').value;
    const response = await fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    });
    const data = await response.json();
    const message = document.getElementById('message');
    message.innerHTML = data.message;
});

document.getElementById('url').addEventListener('input', async function () {
    const url = this.value;
    if (url) {
        const response = await fetch('/get_thumbnail', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        });
        const data = await response.json();
        const thumbnail = document.getElementById('thumbnail');
        thumbnail.src = data.thumbnail_url;
        thumbnail.style.display = 'block';
        thumbnail.setAttribute('data-url', url); // Defina o atributo data-url com a URL do vídeo
    }
});

document.getElementById('thumbnail').addEventListener('click', function () {
    const videoUrl = this.getAttribute('data-url');
    if (videoUrl) {
        window.open(videoUrl, '_blank'); // Abre a URL do vídeo em uma nova aba
    }
});

document.getElementById('logo').addEventListener('click', function () {
    window.location.reload();
});