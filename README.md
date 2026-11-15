# Projeto 15 — Comparador de ofertas e simulador de parcelamento

Este trabalho foi desenvolvido para a disciplina de Programação I em Python. A
ideia é usar ofertas de smartphones pesquisadas em diferentes lojas para
entender melhor o que muda entre pagar à vista e parcelar. Além de comparar os
valores coletados, o programa permite fazer simulações e observar como os juros
compostos alteram um preço ao longo do tempo.

Como o objetivo também é praticar os conteúdos vistos na disciplina, o código
foi organizado em funções e não utiliza bibliotecas ou importações. Os cálculos
de juros compostos são feitos com laços, sem o operador `**` e sem `pow()`.

## O que o programa faz

Ao iniciar `parte 3.py`, o usuário encontra três opções:

1. **Comparar ofertas reais cadastradas.** O programa mostra os planos
   registrados para o modelo escolhido, calcula o total das parcelas e compara
   esse total com o preço à vista. Também apresenta a menor e a maior oferta a
   prazo. A comparação só faz sentido quando as ofertas são do mesmo modelo e
   configuração.
2. **Simular um parcelamento.** O usuário informa o modelo, o preço-base, a
   entrada, o número máximo de parcelas e, se quiser, um limite para o valor
   mensal. O programa calcula cenários usando as médias de taxas e descontos
   pesquisadas para cada plataforma.
3. **Fazer a projeção acadêmica com K.** O usuário informa o produto e o preço
   inicial. A partir do K do grupo, o programa define uma taxa mensal e um
   prazo e mostra a evolução do saldo e dos juros acumulados.

Para executar, abra um terminal na pasta do projeto e rode:

```text
python "parte 3.py"
```

## Como os valores são interpretados

No comparativo real, o total a prazo é calculado pela fórmula:

```text
total = entrada + (número de parcelas x valor de cada parcela)
```

O programa também mostra a diferença entre esse total e o preço à vista. Essa
diferença é um acréscimo observado na oferta, mas não deve ser chamada
automaticamente de juros: em alguns anúncios, o preço à vista já inclui um
desconto no Pix. Quando o preço-base do cartão foi confirmado na coleta, ele é
apresentado separadamente para ajudar a interpretar o resultado.

Na projeção com K, o saldo é atualizado mês a mês:

```text
saldo novo = saldo anterior x (1 + taxa mensal / 100)
```

Essa projeção serve para o exercício acadêmico. Ela não representa uma taxa
cobrada por Amazon, Magazine Luiza ou Mercado Livre.

## De onde vêm os dados e quais são os limites

As ofertas reais são registros transcritos manualmente de pesquisas e capturas
de tela e ficam na lista `OFERTAS_REAIS`, em `parte 3.py`. O programa não lê uma
planilha ou um arquivo CSV automaticamente. Antes de comparar dois anúncios,
é importante conferir se correspondem ao mesmo aparelho, armazenamento,
versão, vendedor e condição de pagamento. Se a coleta não tiver ofertas
equivalentes nas três plataformas, o programa avisa; nesse caso, o resultado
não deve ser apresentado como uma comparação completa entre as lojas.

A simulação da opção 2 depende das listas `AMOSTRAS_TAXAS_MENSAIS` e
`AMOSTRAS_DESCONTOS_PIX`, que devem ser preenchidas com resultados calculados
a partir de pesquisas reais do grupo. Elas estão vazias no código atual, então
é necessário inserir esses dados antes de usar essa opção. Os valores de
exemplo nos comentários são apenas ilustrativos e não devem ser tratados como
taxas oficiais.

O valor de K também precisa ser confirmado pelo grupo conforme as orientações
do professor. No código, K está definido como 10; com esse valor, a função de
parâmetros determina taxa de 1% ao mês e prazo de 10 meses.

## Antes da entrega

- Confirmar o cálculo de K com as matrículas e com o professor.
- Preencher os nomes do grupo e dos integrantes no cabeçalho do código.
- Completar as amostras de taxas e descontos com dados pesquisados e
  documentar suas fontes.
- Conferir preços, vendedores e condições nas capturas originais.
- Testar o menu e revisar se os resultados fazem sentido para cada caso.

O programa é um recurso para organizar e estudar os dados coletados. Os
resultados dependem da qualidade dessas informações e não substituem a
conferência do anúncio original.
