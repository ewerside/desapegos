# Desapegos

Página simples com os itens à venda, publicada pelo GitHub Pages em https://ewerside.github.io/desapegos/.

- `itens.json`: os itens na ordem em que aparecem (o que deve vender primeiro vem antes), com nome, preço de grupo, descrição e fotos.
- `modelo.html`: o layout da página.
- `gerar.py`: reduz as fotos para `fotos/` e escreve `index.html` a partir dos dois arquivos acima.

O que entra na página é decidido pela caixa "No site" do banco Produtos, no Notion do Motor de Preços. Para atualizar: mudar `itens.json`, rodar `python gerar.py <pasta Produtos>` e publicar.
