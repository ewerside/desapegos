"""Gera a página de desapegos a partir de itens.json.

Uso: python gerar.py PASTA_DAS_FOTOS_ORIGINAIS
As fotos de itens.json são caminhos relativos a essa pasta (a pasta
Produtos do Motor de Preços). Cada foto vira duas: uma grande (1280 px)
para a janela de detalhes e uma média (720 px) para o cartão.
"""
import html
import json
import os
import shutil
import sys

from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.abspath(__file__))
ORIGEM = sys.argv[1]
TAMANHOS = {"g": 1280, "m": 720}


def reduzir(rel, destino, lado):
    im = ImageOps.exif_transpose(Image.open(os.path.join(ORIGEM, rel))).convert("RGB")
    im.thumbnail((lado, lado))
    im.save(destino, quality=80, optimize=True, progressive=True)


itens = json.load(open(os.path.join(RAIZ, "itens.json"), encoding="utf-8"))
pasta = os.path.join(RAIZ, "fotos")
shutil.rmtree(pasta, ignore_errors=True)
os.makedirs(pasta)
for it in itens:
    it["arquivos"] = []
    for i, rel in enumerate(it["fotos"], 1):
        base = f"{it['id']}-{i}"
        for suf, lado in TAMANHOS.items():
            reduzir(rel, os.path.join(pasta, f"{base}-{suf}.jpg"), lado)
        it["arquivos"].append(base)

e = html.escape


def carrossel(it, tam):
    total = len(it["arquivos"])
    partes = []
    for n, b in enumerate(it["arquivos"], 1):
        lazy = ' loading="lazy"' if n > 1 else ""
        partes.append(f'<img src="fotos/{b}-{tam}.jpg" alt="{e(it["nome"])}, foto {n} de {total}"{lazy} draggable="false">')
    return '<div class="trilho">' + "".join(partes) + "</div>"


cards = []
dados = {}
for n, it in enumerate(itens):
    cards.append(
        f'<article class="nota" style="--giro:{[-1.2, .9, -.4, 1.3, -.8, .5][n % 6]}deg" data-id="{e(it["id"])}">'
        f'<div class="carrossel" data-total="{len(it["arquivos"])}">{carrossel(it, "m")}'
        '<button class="seta ant" aria-label="Foto anterior"></button>'
        '<button class="seta prox" aria-label="Próxima foto"></button>'
        '<div class="pontos"></div></div>'
        f'<div class="texto"><h2>{e(it["nome"])}</h2><p>{e(it["resumo"])}</p>'
        f'<span class="preco">{e(it["preco"])}</span>'
        '<div class="acoes"><button class="ver">Ver detalhes</button>'
        '<a class="zap" data-local="cartao" target="_blank" rel="noopener">Quero este</a></div></div></article>'
    )
    dados[it["id"]] = {"nome": it["nome"], "preco": it["preco"], "descricao": it["descricao"],
                       "html": carrossel(it, "g"), "total": len(it["arquivos"])}

pagina = open(os.path.join(RAIZ, "modelo.html"), encoding="utf-8").read()
pagina = pagina.replace("{{CARDS}}", "\n".join(cards))
pagina = pagina.replace("{{DADOS}}", json.dumps(dados, ensure_ascii=False).replace("</", "<\\/"))
pagina = pagina.replace("{{CAPA}}", f"fotos/{itens[0]['arquivos'][0]}-m.jpg")
open(os.path.join(RAIZ, "index.html"), "w", encoding="utf-8").write(pagina)
print(f"{len(itens)} itens, index.html gerado")
