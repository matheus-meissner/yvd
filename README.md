Para rodar o codigo em tempo real, abra 3 terminais;

Execute os codigos abaixo na pasta do projeto!

conda activate teste_flask (yvd caso ja esteja renomeado);

Terminal 1 {
  execute app.py
}

Terminal 2 {
  execute sass --watch static/css/main.scss:static/css/styles.css
}

Terminal 3 {
  execute browser-sync start --proxy "localhost:5000" --files "static/css/*.css, templates/*.html"
}
