window.onload = function() {
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
            thumbnail.style.opacity = 0; // Defina a opacidade inicial para 0
            thumbnail.style.display = 'block';
            thumbnail.setAttribute('data-url', url); // Defina o atributo data-url com a URL do vídeo
            thumbnail.style.transition = 'opacity 1s'; // Adicione a transição de opacidade
            setTimeout(function() {
                thumbnail.style.opacity = 1; // Defina a opacidade para 1 para iniciar a transição
            }, 1000); // Pequeno delay para garantir a transição
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