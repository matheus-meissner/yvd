const backendUrl = "https://ytvideodownloader-production.up.railway.app";

window.onload = function() {
    document.getElementById('download-form').addEventListener('submit', async function (e) {
        e.preventDefault();
        const url = document.getElementById('url').value;

        try {
            const response = await fetch(`${backendUrl}/download`, {  // Usando backendUrl para obter a URL do vídeo
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            });
            const data = await response.json();
            const message = document.getElementById('message');
            message.innerHTML = data.message;

            // Link de download direto no navegador
            const downloadLink = document.createElement('a');
            downloadLink.href = data.download_url;
            downloadLink.target = "_blank"; // Abre em uma nova aba
            downloadLink.download = ""; // Permite o download direto no navegador
            downloadLink.textContent = "Clique aqui para baixar o vídeo";
            message.appendChild(downloadLink);

            setTimeout(function() {
                message.style.opacity = 1;
            }, 10);

        } catch (error) {
            console.error("Erro ao tentar baixar:", error);
            document.getElementById('message').textContent = "Erro ao tentar baixar o vídeo.";
        }
    });

    document.getElementById('url').addEventListener('input', async function () {
        const url = this.value;
        const thumbnail = document.getElementById('thumbnail');
        if (url) {
            const response = await fetch(`${backendUrl}/get_thumbnail`, {  // Usando backendUrl para obter a thumbnail
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            });
            const data = await response.json();
            thumbnail.src = data.thumbnail_url;
            thumbnail.style.opacity = 0;
            thumbnail.style.display = 'block';
            thumbnail.setAttribute('data-url', url);
            thumbnail.style.transition = 'opacity 1s, box-shadow 1s';
            setTimeout(function() {
                thumbnail.style.opacity = 1;
            }, 100);
        } else {
            thumbnail.style.opacity = 0;
            setTimeout(function() {
                thumbnail.style.display = 'none';
            }, 1000);
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

    const thumbnail = document.getElementById('thumbnail');
    const tooltip = document.getElementById('tooltip');
    let tooltipVisible = false;

    thumbnail.addEventListener('mouseover', function () {
        tooltipVisible = true;
        tooltip.style.display = 'block';
        tooltip.style.opacity = 0;
        tooltip.style.transition = 'opacity 1s';
        setTimeout(function() {
            if (tooltipVisible) {
                tooltip.style.opacity = 1;
            }
        }, 10);
    });

    thumbnail.addEventListener('mousemove', function (e) {
        tooltip.style.left = e.pageX + 10 + 'px';
        tooltip.style.top = e.pageY + 10 + 'px';
    });

    thumbnail.addEventListener('mouseout', function () {
        tooltipVisible = false;
        tooltip.style.opacity = 0;
        tooltip.style.transition = 'opacity 1s';
        setTimeout(function() {
            if (!tooltipVisible) {
                tooltip.style.display = 'none';
            }
        }, 1000);
    });
};
