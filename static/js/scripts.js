window.onload = function() {
    document.getElementById('download-form').addEventListener('submit', async function (e) {
        e.preventDefault();
        const url = document.getElementById('url').value;
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            const data = await response.json();
            const message = document.getElementById('message');
            message.innerHTML = data.message;

            // Download do vídeo
            const downloadLink = document.createElement('a');
            downloadLink.href = data.download_url;
            downloadLink.download = true;
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);

            setTimeout(function() {
                message.style.opacity = 1; // Defina a opacidade para 1 para iniciar a transição
            }, 10); // Pequeno delay para garantir a transição
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
            const message = document.getElementById('message');
            message.innerHTML = 'Ocorreu um erro ao tentar baixar o vídeo. Por favor, tente novamente.';
        }
    });

    document.getElementById('url').addEventListener('input', async function () {
        const url = this.value;
        const thumbnail = document.getElementById('thumbnail');
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
            thumbnail.style.opacity = 0; // Defina a opacidade inicial para 0
            thumbnail.style.display = 'block';
            thumbnail.setAttribute('data-url', url); // Defina o atributo data-url com a URL do vídeo
            thumbnail.style.transition = 'opacity 1s, box-shadow 1s'; // Adicione a transição de opacidade e box-shadow
            setTimeout(function() {
                thumbnail.style.opacity = 1; // Defina a opacidade para 1 para iniciar a transição
            }, 100); // Pequeno delay para garantir a transição
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