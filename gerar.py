"""Gera a página de desapegos a partir de itens.json.

Uso: python gerar.py PASTA_DAS_FOTOS_ORIGINAIS
As fotos listadas em itens.json são caminhos relativos a essa pasta
(a pasta Produtos do Motor de Preços). O script reduz cada foto,
grava em fotos/ e escreve index.html.
"""
import html
import json
import os
import sys

from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.abspath(__file__))
ORIGEM = sys.argv[1]
GRANDE, MINI = 1280, 640


def reduzir(rel, destino, lado):
    im = ImageOps.exif_transpose(Image.open(os.path.join(ORIGEM, rel))).convert("RGB")
    im.thumbnail((lado, lado))
    im.save(destino, quality=80, optimize=True, progressive=True)


itens = json.load(open(os.path.join(RAIZ, "itens.json"), encoding="utf-8"))
os.makedirs(os.path.join(RAIZ, "fotos"), exist_ok=True)
for it in itens:
    nomes = []
    for i, rel in enumerate(it["fotos"], 1):
        nome = f"{it['id']}-{i}.jpg"
        reduzir(rel, os.path.join(RAIZ, "fotos", nome), GRANDE)
        nomes.append(nome)
    reduzir(it.get("capa", it["fotos"][0]), os.path.join(RAIZ, "fotos", f"{it['id']}-capa.jpg"), MINI)
    it["arquivos"] = nomes

e = html.escape
cards, dados = [], {}
for it in itens:
    cards.append(
        f'<button class="card" data-id="{e(it["id"])}">'
        f'<img src="fotos/{e(it["id"])}-capa.jpg" alt="{e(it["nome"])}" loading="lazy">'
        f'<span class="info"><span class="nome">{e(it["nome"])}</span>'
        f'<span class="resumo">{e(it["resumo"])}</span>'
        f'<span class="preco">{e(it["preco"])}</span></span></button>'
    )
    dados[it["id"]] = {k: it[k] for k in ("nome", "preco", "descricao", "arquivos")}

pagina = open(os.path.join(RAIZ, "modelo.html"), encoding="utf-8").read()
pagina = pagina.replace("{{CARDS}}", "\n".join(cards))
pagina = pagina.replace("{{DADOS}}", json.dumps(dados, ensure_ascii=False).replace("</", "<\\/"))
pagina = pagina.replace("{{TOTAL}}", str(len(itens)))
open(os.path.join(RAIZ, "index.html"), "w", encoding="utf-8").write(pagina)
print(f"{len(itens)} itens, index.html gerado")
