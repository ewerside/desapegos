"""Gera compartilhar.jpg (1200 x 630), a imagem que aparece quando o link é colado no WhatsApp.

Uso: python gerar_compartilhar.py PASTA_DAS_FOTOS_ORIGINAIS PASTA_DA_FONTE_SHANTELL
"""
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ORIGEM, FONTE = sys.argv[1], sys.argv[2]
W, H = 1200, 630
TINTA = (34, 50, 77)
fb = ImageFont.truetype(FONTE + "/Shantell_Sans-Normal-ExtraBold.otf", 78)
fm = ImageFont.truetype(FONTE + "/Shantell_Sans-Normal-SemiBold.otf", 31)

bg = Image.new("RGBA", (W, H), "#d6e2d1")
camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dl = ImageDraw.Draw(camada)
fraco = (34, 50, 77, 22)
for x in range(0, W, 120):
    for y in range(0, H, 120):
        dl.rectangle([x + 12, y + 22, x + 30, y + 50], outline=fraco, width=2)
        dl.ellipse([x + 45, y + 33, x + 59, y + 47], outline=fraco, width=2)
        dl.line([x + 52, y + 47, x + 52, y + 55], fill=fraco, width=2)
        dl.polygon([(x + 70, y + 108), (x + 70, y + 88), (x + 81, y + 79), (x + 92, y + 88), (x + 92, y + 108)], outline=fraco)
bg = Image.alpha_composite(bg, camada)


def colar(img, pos):
    sombra = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sombra.paste((0, 0, 0, 65), (0, 0), img.split()[3])
    sombra = sombra.filter(ImageFilter.GaussianBlur(8))
    bg.alpha_composite(sombra, (pos[0] + 4, pos[1] + 10))
    bg.alpha_composite(img, pos)


FOTOS = [
    ("Samsung Galaxy smartwatch4/20261121_032349_703_foto.jpg", -7, (560, 40)),
    ("máquina de lavar Samsung/20261117_171900_37_foto.jpg", 5, (800, 30)),
    ("carrinho controle remoto Traxxas/20261117_193509_169_foto.jpg", -3, (640, 300)),
    ("panela elétrica morphy richards e acessórios/20261117_201024_229_foto.jpg", 6, (890, 310)),
]
FITAS = [(240, 205, 96, 210), (160, 200, 220, 210)]
for i, (f, giro, pos) in enumerate(FOTOS):
    im = ImageOps.exif_transpose(Image.open(f"{ORIGEM}/{f}")).convert("RGB")
    s = min(im.size)
    im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((230, 230))
    nota = Image.new("RGBA", (254, 280), (255, 254, 248, 255))
    nota.paste(im, (12, 12))
    nota.alpha_composite(Image.new("RGBA", (90, 26), FITAS[i % 2]), (82, 0))
    colar(nota.rotate(giro, expand=True, resample=Image.BICUBIC), pos)

d = ImageDraw.Draw(bg)
ox, oy = 70, 95
for r in [(0, 40, 26, 80), (30, 8, 56, 80), (60, 48, 86, 80)]:
    d.rectangle([ox + r[0], oy + r[1], ox + r[2], oy + r[3]], outline=TINTA, width=4)
d.line([ox - 6, oy + 80, ox + 92, oy + 80], fill=TINTA, width=4)
for wx, wy, c in [(6, 48, TINTA), (15, 48, TINTA), (36, 16, TINTA), (45, 16, (242, 201, 76)), (36, 30, TINTA),
                  (45, 30, TINTA), (66, 56, TINTA), (75, 56, (242, 201, 76))]:
    d.rectangle([ox + wx, oy + wy, ox + wx + 6, oy + wy + 7], fill=c)
d.text((70, 200), "Desapegos", font=fb, fill=TINTA)
d.text((70, 285), "do Ewer", font=fb, fill=TINTA)

linhas = ["Coisas à venda de um", "vizinho, com preço", "de vizinho."]
larg = max(int(db_w) for db_w in [ImageDraw.Draw(bg).textlength(t, font=fm) for t in linhas]) + 44
bilhete = Image.new("RGBA", (larg, 22 + 44 * len(linhas)), (255, 254, 248, 255))
db = ImageDraw.Draw(bilhete)
for k, t in enumerate(linhas):
    db.text((22, 14 + 44 * k), t, font=fm, fill=TINTA)
colar(bilhete.rotate(-1.5, expand=True, resample=Image.BICUBIC), (70, 392))
bg.convert("RGB").save("compartilhar.jpg", quality=88)
print("compartilhar.jpg gerado")
