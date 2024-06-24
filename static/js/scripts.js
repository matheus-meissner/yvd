window.onload = function() {
    document.getElementById('download-form').addEventListener('submit', async function (e) {
        e.preventDefault();
        const url = document.getElementById('url').value.trim();

        if (!isValidURL(url)) {
            alert("Invalid URL");
            return;
        }

        const requestBody = JSON.stringify({ url: url });
        if (!isJSON(requestBody)) {
            alert("Invalid JSON format");
            return;
        }

        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: requestBody
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Error response:', errorData);
                throw new Error(errorData.error);
            }

            const blob = await response.blob();
            console.log('Download blob:', blob);
            const downloadUrl = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = 'video.mp4';
            document.body.appendChild(a);
            a.click();
            a.remove();

            const message = document.getElementById('message');
            message.innerHTML = 'Video downloaded successfully';
            setTimeout(function() {
                message.style.opacity = 1; // Defina a opacidade para 1 para iniciar a transição
            }, 10); // Pequeno delay para garantir a transição
        } catch (error) {
            console.error('Error fetching download:', error);
            const message = document.getElementById('message');
            message.innerHTML = `Error: ${error.message}`;
            message.style.opacity = 1;
        }
    });

    document.getElementById('url').addEventListener('input', async function () {
        const url = this.value.trim(); // Remove espaços extras da URL
        const thumbnail = document.getElementById('thumbnail');
        if (url) {
            try {
                const response = await fetch('/get_thumbnail', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ url: url })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    console.error('Error response:', errorData);
                    throw new Error(errorData.error);
                }

                const data = await response.json();
                console.log('Thumbnail response:', data);
                thumbnail.src = data.thumbnail_url;
                thumbnail.style.opacity = 0; // Defina a opacidade inicial para 0
                thumbnail.style.display = 'block';
                thumbnail.setAttribute('data-url', url); // Defina o atributo data-url com a URL do vídeo
                thumbnail.style.transition = 'opacity 1s, box-shadow 1s'; // Adicione a transição de opacidade e box-shadow
                setTimeout(function() {
                    thumbnail.style.opacity = 1; // Defina a opacidade para 1 para iniciar a transição
                }, 100); // Pequeno delay para garantir a transição
            } catch (error) {
                console.error('Error fetching thumbnail:', error);
            }
        } else {
            thumbnail.style.opacity = 0; // Defina a opacidade para 0 para iniciar o fade out
            setTimeout(function() {
                thumbnail.style.display = 'none'; // Ocultar a thumbnail após a transição de opacidade
            }, 1000); // Aguarde a duração da transição antes de ocultar
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
        }, 10); // Pequeno delay para garantir a transição
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
        }, 1000); // Tempo de espera para a transição completar antes de esconder a tooltip
    });
}