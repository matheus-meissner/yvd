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
    }
});
