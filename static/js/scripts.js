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
    document.getElementById('message').innerText = data.message;
});
