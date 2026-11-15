# Comparador de compras parceladas

Programa acadêmico em Python para consultar os dados coletados de ofertas de
smartphones e projetar juros compostos hipotéticos. O código não usa
importações nem bibliotecas externas.

## Como executar

Execute `parte 3.py` em um terminal. O menu permite:

1. Comparar preços e planos registrados na coleta.
2. Projetar juros compostos usando o K do grupo.
3. Exibir as duas análises.

Escolha o modelo na lista e informe a quantidade de parcelas. A comparação
real só considera como plano solicitado uma oferta com essa quantidade exata
de parcelas registrada; o programa não inventa parcelas ou taxas para planos
que não foram coletados.

## Como interpretar os valores

- **Diferença entre parcelado e Pix**: total das parcelas menos o preço
  promocional à vista. Essa diferença pode refletir o desconto de Pix, e não
  necessariamente juros cobrados.
- **Acréscimo sobre o preço-base**: total calculado das parcelas menos o total
  anunciado como referência, quando esse dado foi coletado.
- **Projeção com K**: aplica mensalmente a taxa definida por `K` ao menor
  preço-base coletado do modelo. Se a coleta não tiver preço-base, usa o menor
  valor Pix e identifica essa origem. O prazo é a quantidade de parcelas
  informada. É uma simulação acadêmica, não uma taxa real da loja.

Os modelos e planos disponíveis dependem dos registros existentes na lista
`ofertas` de `parte 3.py`. Produtos ausentes da coleta, como o Galaxy S23+,
não podem ser comparados até que seus dados sejam adicionados.
