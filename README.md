# 🛍️ Comparador de Compras Parceladas

Aplicação acadêmica em Python para analisar ofertas de smartphones, simular
parcelamentos e visualizar uma projeção de juros compostos. O projeto oferece
um menu no terminal e uma interface gráfica construída com Tkinter.

> **Objetivo:** ajudar a entender o custo total de uma compra — não apenas o
> valor de cada parcela.

---

## ✨ O que você pode fazer

| Recurso | O que faz |
| --- | --- |
| **Comparar ofertas** | Agrupa ofertas pelo produto, exibe preço à vista, entrada, parcelas, total e juros; destaca o menor e o maior custo, inclusive em caso de empate. |
| **Cadastrar ofertas** | Permite informar novas ofertas e valida os dados antes de incluí-las na comparação. |
| **Simular parcelamento** | Estima parcelas para uma combinação de banco e plataforma e compara os prazos, o total e o preço Pix. Também pode considerar um limite mensal. |
| **Projetar juros com K** | Demonstra, mês a mês, como um capital evolui com juros compostos usando os parâmetros definidos pelo projeto. |
| **Usar interface gráfica** | Reúne comparação, cadastro, simulação e projeção em telas navegáveis. |

## 🚀 Como executar

### Requisitos

- Python 3 instalado.
- Tkinter disponível na instalação do Python para usar a interface gráfica
  (normalmente incluído nas instalações padrão).
- Nenhuma biblioteca financeira de terceiros é necessária.

Deixe `Comparador.py` e `interface_tkinter.py` na mesma pasta. No terminal,
abra essa pasta e escolha uma das opções:

**Menu no terminal** — executa os testes de integração e, se forem aprovados,
abre o menu:

```bash
python Comparador.py
```

**Interface gráfica diretamente:**

```bash
python interface_tkinter.py
```

No Windows, se o comando `python` não estiver disponível, tente `py` no lugar
dele (por exemplo, `py Comparador.py`).

## 🧭 Guia rápido

### Pelo terminal

1. Escolha **1** para comparar ofertas reais, cadastrar uma oferta ou consultar
   todas as ofertas.
2. Escolha **2** para simular um parcelamento. Informe o preço-base, a entrada,
   o banco, a plataforma e o prazo máximo.
3. Escolha **3** para gerar a projeção de juros compostos com o parâmetro `K`.
4. Escolha **4** para abrir a interface gráfica.
5. Escolha **0** para sair.

### Pela interface gráfica

Use a navegação lateral para abrir **Início**, **Comparar Ofertas**,
**Simular Parcelamento** ou **Projeção com K**. Na comparação, selecione um
produto para ver as ofertas ou acesse as abas de cadastro e consulta.

## 🧮 Entenda os cálculos

### Comparação de ofertas

O custo total a prazo considera a entrada e todas as parcelas:

```text
Total a prazo = entrada + (número de parcelas × valor de cada parcela)
Juros em reais = total a prazo − preço à vista
Juros percentuais = (juros em reais ÷ preço à vista) × 100
```

As ofertas com menor e maior total são destacadas. Se houver valores iguais,
o programa informa o empate.

### Simulação de parcelamento

A simulação estima parcelas fixas pelo modelo Price, a partir de uma taxa
mensal de referência associada ao banco escolhido. Também estima o preço Pix
aplicando a média de descontos cadastrada para a plataforma. É possível
comparar vários prazos e informar um limite mensal.

**Importante:** taxas e descontos são amostras mantidas no código, não
condições garantidas por bancos ou lojas. A taxa efetiva depende do contrato e
do Custo Efetivo Total (CET); confira as condições atuais diretamente com a
instituição e o vendedor. A menor parcela mensal não significa necessariamente
o menor custo total.

### Projeção com juros compostos

O valor de `K` determina a taxa mensal e o prazo:

```text
Taxa mensal (%) = (K % 5) + 1
Prazo (meses)   = (K % 6) + 6
```

O saldo é atualizado mês a mês, com juros incidindo sobre o saldo anterior.
Essa projeção é **didática e hipotética**: não representa uma oferta real de
crédito nem inclui amortização de parcelas.

## 👥 Integrantes e responsabilidades

### 1. Pedro Vitor — entrada, validação e cadastro

Responsável pela base de entrada e tratamento dos dados. Essa parte inclui
leitura e conversão de valores, validação de campos financeiros, criação do
formato comum das ofertas e cadastro de novas ofertas.

### 2. Eduardo Soares — cálculos financeiros e comparação

Responsável pelos cálculos do total a prazo e dos juros, pela identificação
das ofertas mais baratas e mais caras e pela exibição dos resultados. Também
inclui a simulação de parcelamento considerando referências de banco e
plataforma.

### 3. Josué Gabriel — juros compostos, testes e integração

Responsável pela projeção de juros compostos com o parâmetro `K`, pelos testes
de integração e pela conexão das funcionalidades das três partes no fluxo do
programa.

## 🗂️ Arquivos principais

```text
Comparador de compras/
├── Comparador.py        # Lógica integrada, dados, testes e menu do terminal
├── interface_tkinter.py # Interface gráfica que reutiliza o módulo principal
├── Parte1.py            # Arquivo de desenvolvimento da parte 1
├── Parte2.py            # Arquivo de desenvolvimento da parte 2
├── parte 3.py           # Arquivo de desenvolvimento da parte 3
├── README.md            # Este guia
└── LICENSE              # Licença do projeto
```

O fluxo integrado e a interface gráfica usam principalmente `Comparador.py`
e `interface_tkinter.py`. Os arquivos `Parte1.py`, `Parte2.py` e `parte 3.py`
preservam versões de desenvolvimento das partes; para executar o projeto
integrado, use um dos dois comandos indicados acima.

## ✅ Testes

Ao iniciar `Comparador.py`, os testes de integração são executados antes de o
menu aparecer. Para executar somente os testes pelo terminal:

```bash
python -c "import Comparador; Comparador.executar_testes_integracao()"
```

## 📌 Observações

- As ofertas cadastradas durante a execução ficam na memória do programa e
  não são salvas em arquivo; elas são perdidas ao encerrar a aplicação.
- Os produtos de algumas ofertas iniciais podem ter capacidades diferentes.
  Confira a descrição do modelo antes de comparar os preços.
- Valores, taxas e descontos podem precisar de atualização. Consulte a fonte
  e as condições vigentes antes de tomar decisões de compra.

---

**Projeto acadêmico — Projeto 15: Comparador de Compras Parceladas**
