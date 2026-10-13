# Último Trem para Lugar Nenhum

Abra `index.html` por um servidor (não direto do arquivo): `python3 -m http.server` e acesse `localhost:8000`.

## Estrutura
```
index.html              jogo (HTML+CSS+JS)
assets/
  tiles/vagao0..4.png         chão dos 5 vagões   (256x64: 2 variações de 128x64 lado a lado)
  tiles/plataforma0..6.png    chão das 7 estações (idem). 0 Inundada,1 Selva,2 Deserto,3 Caverna,4 Relógio,5 Neve,6 Laboratório
  walls/vagao0..4.png         parede do fundo de cada vagão (512x192)
tools/gerar_assets.py   regenera as texturas procedurais
```
Para usar arte própria, substitua o PNG mantendo nome e tamanho. Se um arquivo faltar, o jogo desenha o padrão por código.
Personagens, móveis e puzzles continuam desenhados por código.

## GitHub Pages
Settings → Pages → Deploy from a branch → `main` / `(root)`. Use maiúsculas/minúsculas exatamente como nos nomes.
