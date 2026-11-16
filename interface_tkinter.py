"""Interface grafica (tkinter) do Projeto 15 - Comparador de Compras Parceladas.

Este arquivo NAO altera o Comparador.py: ele apenas reutiliza as funcoes, as
listas e os dados que ja existem la (validacao, calculos, ofertas, taxas, K).

# [IA] Layout e codigo gerados com auxilio de IA a partir das telas do Figma;
#      o grupo deve revisar e preencher os comentarios "# Autor:" abaixo.
# Autor: (preencher com o integrante responsavel)

Como usar
---------
1) Rodar so a interface (os dois arquivos na mesma pasta):
       python interface_tkinter.py

2) Chamar a partir do Comparador.py (sem circularidade de import). Exemplo,
   como uma nova opcao do menu:

       def abrir_interface_grafica():
           import sys
           from interface_tkinter import abrir_interface
           abrir_interface(sys.modules[__name__])

   Passar o proprio modulo garante que a janela e o terminal compartilham a
   mesma lista OFERTAS_REAIS.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


# =====================================================================
# PALETA E FONTES (inspiradas nas telas do Figma)
# =====================================================================

COR_FUNDO = "#F4F6FA"
COR_CARD = "#FFFFFF"
COR_BORDA = "#DDE3EE"
COR_TEXTO = "#16233B"
COR_MUTED = "#66758C"
COR_AZUL = "#2563D8"
COR_AZUL_ESCURO = "#1D4FB0"
COR_AZUL_CLARO = "#E8EFFC"
COR_SIDEBAR = "#13233F"
COR_SIDEBAR_ATIVO = "#2A4F86"
COR_VERDE = "#17784A"
COR_VERDE_BG = "#E8F5EE"
COR_VERM = "#C0392B"
COR_VERM_BG = "#FDECEC"
COR_AVISO = "#8A5A00"
COR_AVISO_BG = "#FFF6E0"

FONTE = "Segoe UI"


def fonte(tamanho=10, peso="normal"):
    """Monta a tupla de fonte usada em todos os widgets."""
    return (FONTE, tamanho, peso)


# =====================================================================
# COMPONENTES REUTILIZAVEIS
# =====================================================================


def rotulo(pai, texto, tamanho=10, peso="normal", cor=COR_TEXTO, ancora="w", quebra=0):
    """Cria um Label ja estilizado, herdando a cor de fundo do pai."""
    return tk.Label(pai, text=texto, font=fonte(tamanho, peso), fg=cor,
                    bg=pai.cget("bg"), anchor=ancora, justify="left",
                    wraplength=quebra)


def limpar(frame):
    """Remove todos os widgets filhos de um frame."""
    for widget in frame.winfo_children():
        widget.destroy()


def distribuir(pai, widgets, espaco=14):
    """Coloca widgets lado a lado, com colunas de mesma largura."""
    for indice, widget in enumerate(widgets):
        widget.grid(row=0, column=indice, sticky="nsew",
                    padx=(0 if indice == 0 else espaco, 0))
        pai.columnconfigure(indice, weight=1, uniform="colunas")


def ler_numero(comparador, texto):
    """Converte texto em float usando a funcao do codigo principal (ou None)."""
    try:
        return comparador.converter_valor_numerico(texto)
    except ValueError:
        return None


def ler_inteiro(texto):
    """Converte texto em int (ou None se for invalido)."""
    try:
        return int(texto.strip())
    except ValueError:
        return None


def formatar_diferenca(comparador, valor):
    """Formata a diferenca em relacao ao Pix com sinal (+ ou -)."""
    sinal = "+ " if valor >= 0 else "- "
    return sinal + comparador.formatar_reais(abs(valor))


class Botao(tk.Label):
    """Botao plano feito com Label (as cores funcionam em qualquer sistema)."""

    ESTILOS = {
        "primario": (COR_AZUL, "#FFFFFF", COR_AZUL, COR_AZUL_ESCURO),
        "secundario": ("#FFFFFF", COR_TEXTO, COR_BORDA, "#EEF2F8"),
        "ativo": (COR_AZUL_CLARO, COR_AZUL, "#C5D5F4", COR_AZUL_CLARO),
    }

    def __init__(self, pai, texto, comando, estilo="primario", pady=10, padx=20):
        tk.Label.__init__(self, pai, text=texto, cursor="hand2",
                          padx=padx, pady=pady, highlightthickness=1)
        self.estilo = estilo
        self.aplicar(estilo)
        self.bind("<Button-1>", lambda evento: comando())
        self.bind("<Enter>", self._entrar)
        self.bind("<Leave>", self._sair)

    def aplicar(self, estilo):
        """Troca o estilo visual (usado nas abas)."""
        self.estilo = estilo
        fundo, texto, borda, _ = self.ESTILOS[estilo]
        peso = "normal" if estilo == "secundario" else "bold"
        self.configure(bg=fundo, fg=texto, highlightbackground=borda,
                       font=fonte(10, peso))

    def _entrar(self, evento):
        self.configure(bg=self.ESTILOS[self.estilo][3])

    def _sair(self, evento):
        self.configure(bg=self.ESTILOS[self.estilo][0])


class Card(tk.Frame):
    """Caixa com borda fina; o conteudo deve ser colocado em card.corpo."""

    def __init__(self, pai, bg=COR_CARD, borda=COR_BORDA, padx=20, pady=16):
        tk.Frame.__init__(self, pai, bg=bg, highlightthickness=1,
                          highlightbackground=borda)
        self.corpo = tk.Frame(self, bg=bg)
        self.corpo.pack(fill="both", expand=True, padx=padx, pady=pady)


def cartao_metrica(pai, titulo, valor, detalhe="", bg=COR_CARD, borda=COR_BORDA,
                   cor_titulo=COR_MUTED, cor_valor=COR_TEXTO, tamanho=15):
    """Cartao pequeno com titulo, valor grande e detalhe opcional."""
    card = Card(pai, bg=bg, borda=borda, padx=16, pady=12)
    rotulo(card.corpo, titulo, 10, cor=cor_titulo).pack(anchor="w")
    rotulo(card.corpo, valor, tamanho, "bold", cor_valor).pack(anchor="w", pady=(4, 2))
    if detalhe:
        rotulo(card.corpo, detalhe, 9, cor=cor_titulo).pack(anchor="w")
    return card


class Campo(tk.Frame):
    """Rotulo + caixa de texto (Entry)."""

    def __init__(self, pai, texto, valor=""):
        tk.Frame.__init__(self, pai, bg=pai.cget("bg"))
        rotulo(self, texto, 10).pack(anchor="w")
        self.entrada = tk.Entry(
            self, font=fonte(11), relief="flat", bd=0, fg=COR_TEXTO, bg="#FFFFFF",
            insertbackground=COR_TEXTO, highlightthickness=2,
            highlightbackground=COR_BORDA, highlightcolor=COR_AZUL)
        self.entrada.pack(fill="x", ipady=7, pady=(5, 0))
        self.entrada.insert(0, valor)

    def obter(self):
        """Retorna o texto digitado."""
        return self.entrada.get()

    def definir(self, valor):
        """Substitui o texto do campo."""
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, valor)


class CampoLista(tk.Frame):
    """Rotulo + lista suspensa (Combobox somente leitura)."""

    def __init__(self, pai, texto, valores):
        tk.Frame.__init__(self, pai, bg=pai.cget("bg"))
        rotulo(self, texto, 10).pack(anchor="w")
        self.combo = ttk.Combobox(self, values=list(valores), state="readonly",
                                  font=fonte(11), style="App.TCombobox")
        if valores:
            self.combo.current(0)
        self.combo.pack(fill="x", ipady=6, pady=(5, 0))

    def obter(self):
        """Retorna a opcao selecionada."""
        return self.combo.get()


class Aviso(tk.Frame):
    """Faixa de mensagem (sucesso, erro ou aviso) que pode ser ocultada."""

    CORES = {
        "sucesso": (COR_VERDE_BG, COR_VERDE, "✓"),
        "erro": (COR_VERM_BG, COR_VERM, "!"),
        "aviso": (COR_AVISO_BG, COR_AVISO, "!"),
    }

    def __init__(self, pai):
        tk.Frame.__init__(self, pai, bg=pai.cget("bg"))
        self.faixa = None

    def mostrar(self, tipo, texto):
        """Exibe uma mensagem do tipo informado."""
        self.ocultar()
        fundo, cor, icone = self.CORES[tipo]
        self.faixa = tk.Label(self, text=icone + "  " + texto, bg=fundo, fg=cor,
                              font=fonte(10), anchor="w", justify="left",
                              padx=14, pady=10, wraplength=760)
        self.faixa.pack(fill="x", pady=(0, 10))

    def ocultar(self):
        """Remove a mensagem atual."""
        if self.faixa is not None:
            self.faixa.destroy()
            self.faixa = None


class Tabela(tk.Frame):
    """Tabela (Treeview) estilizada, com rolagem automatica."""

    def __init__(self, pai, colunas, altura=6):
        tk.Frame.__init__(self, pai, bg="#FFFFFF", highlightthickness=1,
                          highlightbackground=COR_BORDA)
        ids = [coluna[0] for coluna in colunas]
        self.arvore = ttk.Treeview(self, columns=ids, show="headings",
                                   height=altura, style="App.Treeview",
                                   selectmode="none")
        for ident, titulo, largura in colunas:
            self.arvore.heading(ident, text=titulo, anchor="w")
            self.arvore.column(ident, anchor="w", width=largura, stretch=True)
        self.arvore.tag_configure("par", background="#F8FAFD")
        self.arvore.tag_configure("verde", background=COR_VERDE_BG, foreground=COR_VERDE)
        self.arvore.tag_configure("vermelho", background=COR_VERM_BG, foreground=COR_VERM)
        self.arvore.tag_configure("destaque", background=COR_AZUL_CLARO)
        self.arvore.tag_configure("apagado", foreground="#9AA6B8")

        self.barra = ttk.Scrollbar(self, orient="vertical", command=self.arvore.yview)
        self.arvore.configure(yscrollcommand=self._rolagem)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.arvore.grid(row=0, column=0, sticky="nsew")

    def _rolagem(self, inicio, fim):
        """Mostra a barra de rolagem so quando ela e necessaria."""
        self.barra.set(inicio, fim)
        if float(inicio) <= 0.0 and float(fim) >= 1.0:
            self.barra.grid_remove()
        else:
            self.barra.grid(row=0, column=1, sticky="ns")

    def preencher(self, linhas):
        """Recebe uma lista de (valores, tag) e redesenha a tabela."""
        self.arvore.delete(*self.arvore.get_children())
        for indice, (valores, tag) in enumerate(linhas):
            if not tag and indice % 2 == 1:
                tag = "par"
            self.arvore.insert("", "end", values=valores, tags=(tag,) if tag else ())


# =====================================================================
# PAGINA BASE
# =====================================================================


class Pagina(tk.Frame):
    """Estrutura comum: titulo, subtitulo e uma area de conteudo."""

    def __init__(self, app, pai, titulo, subtitulo):
        tk.Frame.__init__(self, pai, bg=COR_FUNDO)
        self.app = app
        self.c = app.c
        self.titulo_padrao = titulo
        self.subtitulo_padrao = subtitulo
        cabecalho = tk.Frame(self, bg=COR_FUNDO)
        cabecalho.pack(fill="x", padx=36, pady=(22, 12))
        self.lbl_titulo = rotulo(cabecalho, titulo, 24, "bold")
        self.lbl_titulo.pack(anchor="w")
        self.lbl_subtitulo = rotulo(cabecalho, subtitulo, 11, cor=COR_MUTED)
        self.lbl_subtitulo.pack(anchor="w", pady=(2, 0))
        self.corpo = tk.Frame(self, bg=COR_FUNDO)
        self.corpo.pack(fill="both", expand=True, padx=36, pady=(0, 12))

    def definir_cabecalho(self, titulo=None, subtitulo=None):
        """Troca o titulo/subtitulo (ou volta ao padrao)."""
        self.lbl_titulo.configure(text=titulo or self.titulo_padrao)
        self.lbl_subtitulo.configure(text=subtitulo or self.subtitulo_padrao)

    def ao_exibir(self):
        """Chamado toda vez que a pagina aparece (as subclasses atualizam dados)."""


# =====================================================================
# PAGINA: INICIO
# =====================================================================


class PaginaInicio(Pagina):
    """Tela de boas-vindas com atalhos para as tres funcionalidades."""

    def __init__(self, app, pai):
        Pagina.__init__(self, app, pai, "Início",
                        "Uma decisão mais clara começa com uma boa comparação.")
        faixa = Card(self.corpo, bg=COR_AZUL_CLARO, borda=COR_AZUL_CLARO, padx=26, pady=24)
        faixa.pack(fill="x")
        rotulo(faixa.corpo, "Bem-vindo ao Comparador de Compras Parceladas", 20, "bold").pack(anchor="w")
        rotulo(faixa.corpo, "Compare ofertas, analise parcelamentos e compreenda os custos "
               "financeiros antes de tomar uma decisão.", 11, cor=COR_MUTED).pack(anchor="w", pady=(10, 0))

        linha = tk.Frame(self.corpo, bg=COR_FUNDO)
        linha.pack(fill="x", pady=16)
        itens = [
            ("01", "Comparar Ofertas Reais", "Compare preços e condições de parcelamento entre lojas.",
             "Acessar comparação", "comparacao"),
            ("02", "Simular Parcelamento", "Simule diferentes prazos usando taxas de referência bancárias "
             "e descontos das plataformas.", "Simular agora", "simulacao"),
            ("03", "Projeção de Juros Compostos", "Visualize a evolução mensal de um valor conforme a taxa "
             "e o prazo determinados pelo parâmetro K.", "Fazer projeção", "projecao"),
        ]
        cartoes = []
        for numero, titulo, descricao, botao, destino in itens:
            card = Card(linha, padx=20, pady=18)
            rotulo(card.corpo, numero, 10, cor=COR_MUTED, ancora="e").pack(fill="x")
            rotulo(card.corpo, titulo, 14, "bold").pack(anchor="w", pady=(8, 6))
            rotulo(card.corpo, descricao, 10, cor=COR_MUTED, quebra=250).pack(anchor="w")
            Botao(card.corpo, botao, lambda d=destino: app.mostrar(d)).pack(fill="x", pady=(18, 0))
            cartoes.append(card)
        distribuir(linha, cartoes, 16)

        dica = Card(self.corpo, padx=20, pady=14)
        dica.pack(fill="x")
        rotulo(dica.corpo, "Compare o total. Não apenas a parcela.", 11, "bold").pack(anchor="w")
        rotulo(dica.corpo, "Prazos maiores podem reduzir o valor mensal e aumentar o custo final da compra.",
               10, cor=COR_MUTED).pack(anchor="w", pady=(4, 0))


# =====================================================================
# PAGINA: COMPARAR OFERTAS REAIS (comparar / cadastrar / todas)
# =====================================================================


class PaginaComparacao(Pagina):
    """Opcao 1 do menu: comparacao por produto, cadastro e consulta de ofertas."""

    def __init__(self, app, pai):
        Pagina.__init__(self, app, pai, "Comparação de Ofertas Reais",
                        "Compare o custo total de um mesmo smartphone em diferentes lojas.")
        self.produtos = {}
        self.ultimo_cadastro = None

        barra = tk.Frame(self.corpo, bg=COR_FUNDO)
        barra.pack(fill="x", pady=(0, 12))
        self.abas = {}
        for chave, texto in (("comparar", "Comparar por produto"),
                             ("cadastrar", "Cadastrar nova oferta"),
                             ("todas", "Todas as ofertas")):
            botao = Botao(barra, texto, lambda k=chave: self.trocar_aba(k),
                          "secundario", pady=11, padx=22)
            botao.pack(side="left", padx=(0, 12))
            self.abas[chave] = botao

        self.area = tk.Frame(self.corpo, bg=COR_FUNDO)
        self.area.pack(fill="both", expand=True)
        self.vistas = {
            "comparar": self._montar_comparar(),
            "cadastrar": self._montar_cadastro(),
            "todas": self._montar_todas(),
        }
        self.aba_atual = None
        self.trocar_aba("comparar")

    # ---------------------------------------------------------- abas

    def trocar_aba(self, chave):
        """Mostra a aba escolhida e destaca o botao correspondente."""
        for nome, vista in self.vistas.items():
            vista.pack_forget()
            self.abas[nome].aplicar("ativo" if nome == chave else "secundario")
        self.vistas[chave].pack(fill="both", expand=True)
        self.aba_atual = chave
        if chave == "todas":
            self._atualizar_todas()

    def ao_exibir(self):
        self._atualizar_produtos()
        self._atualizar_todas()

    # ---------------------------------------------------------- aba 1: comparar

    def _montar_comparar(self):
        vista = tk.Frame(self.area, bg=COR_FUNDO)
        card = Card(vista, padx=22, pady=16)
        card.pack(fill="x")
        rotulo(card.corpo, "Produto cadastrado", 10).pack(anchor="w")
        linha = tk.Frame(card.corpo, bg=COR_CARD)
        linha.pack(fill="x", pady=(6, 0))
        self.combo = ttk.Combobox(linha, state="readonly", font=fonte(11), style="App.TCombobox")
        self.combo.pack(side="left", fill="x", expand=True, ipady=6)
        Botao(linha, "Comparar ofertas", self.comparar, pady=11, padx=26).pack(side="left", padx=(24, 0))

        self.aviso_comparar = Aviso(vista)
        self.aviso_comparar.pack(fill="x", pady=(10, 0))
        self.resultado = tk.Frame(vista, bg=COR_FUNDO)
        self.resultado.pack(fill="both", expand=True, pady=(4, 0))
        self._mostrar_vazio()
        self._atualizar_produtos()
        return vista

    def _atualizar_produtos(self):
        """Recarrega a lista de produtos (usa as funcoes do codigo principal)."""
        self.produtos = {}
        for codigo in self.c.listar_codigos_modelos(self.c.OFERTAS_REAIS):
            grupo = self.c.buscar_ofertas_por_modelo(self.c.OFERTAS_REAIS, codigo)
            self.produtos[grupo[0]["produto"]] = codigo
        nomes = list(self.produtos)
        self.combo["values"] = nomes
        if nomes and self.combo.get() not in self.produtos:
            self.combo.current(0)

    def _mostrar_vazio(self):
        limpar(self.resultado)
        card = Card(self.resultado, padx=20, pady=40)
        card.pack(fill="both", expand=True)
        rotulo(card.corpo, "Pronto para comparar?", 18, "bold", ancora="center").pack(fill="x")
        rotulo(card.corpo, "Selecione um produto cadastrado e clique em “Comparar ofertas”.",
               11, cor=COR_MUTED, ancora="center").pack(fill="x", pady=(10, 2))
        rotulo(card.corpo, "Os resultados aparecerão aqui, com destaque para o menor e o maior custo total.",
               10, cor=COR_MUTED, ancora="center").pack(fill="x")

    def comparar(self):
        """Compara as ofertas do produto selecionado."""
        c = self.c
        nome = self.combo.get()
        if nome not in self.produtos:
            self.aviso_comparar.mostrar("aviso", "Selecione um produto cadastrado.")
            return
        ofertas = c.buscar_ofertas_por_modelo(c.OFERTAS_REAIS, self.produtos[nome])
        try:
            baratas = c.achar_mais_barata(ofertas)
            caras = c.achar_mais_cara(ofertas)
            linhas = []
            for oferta in ofertas:
                total = c.calcular_total_prazo(oferta)
                juros_reais, juros_pct = c.calcular_juros(oferta)
                loja, tag = oferta["loja"], ""
                if oferta in baratas:
                    loja += " · empate" if len(baratas) > 1 else " · menor custo"
                    tag = "verde"
                elif oferta in caras:
                    loja += " · empate" if len(caras) > 1 else " · maior custo"
                    tag = "vermelho"
                parcelamento = str(oferta["num_parcelas"]) + " × " + c.formatar_reais(oferta["valor_parcela"])
                linhas.append(((loja, c.formatar_reais(oferta["valor_a_vista"]),
                                c.formatar_reais(oferta["entrada"]), parcelamento,
                                c.formatar_reais(total), c.formatar_reais(juros_reais),
                                c.formatar_percentual(juros_pct)), tag))
            total_barato = c.calcular_total_prazo(baratas[0])
            total_caro = c.calcular_total_prazo(caras[0])
        except ValueError as erro:
            self.aviso_comparar.mostrar("erro", str(erro))
            return

        self.aviso_comparar.ocultar()
        limpar(self.resultado)
        rotulo(self.resultado, "Ofertas para " + nome, 15, "bold").pack(anchor="w", pady=(6, 8))
        tabela = Tabela(self.resultado, [
            ("loja", "Loja", 240), ("vista", "Preço à vista", 110), ("entrada", "Entrada", 100),
            ("parc", "Parcelamento", 140), ("total", "Total a prazo", 120),
            ("jr", "Juros em R$", 100), ("jp", "Juros em %", 90)], altura=min(len(linhas), 6))
        tabela.pack(fill="x")
        tabela.preencher(linhas)

        resumo = tk.Frame(self.resultado, bg=COR_FUNDO)
        resumo.pack(fill="x", pady=12)
        nomes_baratas = ", ".join([o["loja"] for o in baratas])
        nomes_caras = ", ".join([o["loja"] for o in caras])
        distribuir(resumo, [
            cartao_metrica(resumo, "MENOR CUSTO TOTAL" + (" · EMPATE" if len(baratas) > 1 else ""),
                           c.formatar_reais(total_barato), nomes_baratas + " · melhor condição",
                           cor_titulo=COR_VERDE, tamanho=22),
            cartao_metrica(resumo, "MAIOR CUSTO TOTAL" + (" · EMPATE" if len(caras) > 1 else ""),
                           c.formatar_reais(total_caro), nomes_caras + " · maior custo",
                           cor_titulo=COR_VERM, tamanho=22),
        ], 16)
        if len(ofertas) == 1:
            rotulo(self.resultado, "Observação: existe apenas uma oferta cadastrada para este modelo.",
                   10, cor=COR_AVISO).pack(anchor="w")
        rotulo(self.resultado, "O menor valor de parcela não significa o menor custo total. "
               "Total a prazo = entrada + soma das parcelas.", 10, cor=COR_MUTED).pack(anchor="w")

    # ---------------------------------------------------------- aba 2: cadastrar

    def _montar_cadastro(self):
        vista = tk.Frame(self.area, bg=COR_FUNDO)
        card = Card(vista, padx=26, pady=18)
        card.pack(fill="x")
        rotulo(card.corpo, "Dados da oferta", 16, "bold").pack(anchor="w")
        rotulo(card.corpo, "Todos os campos são obrigatórios. Informe os valores em reais.",
               10, cor=COR_MUTED).pack(anchor="w", pady=(2, 10))
        self.aviso_cadastro = Aviso(card.corpo)
        self.aviso_cadastro.pack(fill="x")

        grade = tk.Frame(card.corpo, bg=COR_CARD)
        grade.pack(fill="x")
        grade.columnconfigure(0, weight=1, uniform="g")
        grade.columnconfigure(1, weight=1, uniform="g")
        self.campos = {}
        definicoes = [("loja", "Nome da loja *"), ("produto", "Nome/modelo e versão do produto *"),
                      ("vista", "Preço à vista/Pix (R$) *"), ("entrada", "Valor da entrada (R$) *"),
                      ("parcelas", "Número de parcelas *"), ("valor_parcela", "Valor de cada parcela (R$) *")]
        for indice, (chave, texto) in enumerate(definicoes):
            campo = Campo(grade, texto)
            campo.grid(row=indice // 2, column=indice % 2, sticky="ew", pady=(0, 10),
                       padx=(0, 14) if indice % 2 == 0 else (14, 0))
            campo.entrada.bind("<Return>", lambda evento: self.cadastrar())
            self.campos[chave] = campo
        rotulo(card.corpo, "A entrada deve ser menor que o preço à vista e o total a prazo não "
               "pode ser inferior a ele.", 10, cor=COR_MUTED).pack(anchor="w")

        rodape = tk.Frame(vista, bg=COR_FUNDO)
        rodape.pack(fill="x", pady=(12, 0))
        rotulo(rodape, "Use 0 na entrada quando não houver. Aceita vírgula ou ponto.",
               10, cor=COR_MUTED).pack(side="left")
        Botao(rodape, "Cadastrar oferta", self.cadastrar, pady=11, padx=34).pack(side="right")
        return vista

    def cadastrar(self):
        """Valida o formulario e cadastra a oferta usando o codigo principal."""
        c = self.c
        loja = self.campos["loja"].obter().strip()
        produto = self.campos["produto"].obter().strip()
        textos = [self.campos[k].obter().strip() for k in ("vista", "entrada", "parcelas", "valor_parcela")]
        if not loja or not produto or "" in textos:
            self.aviso_cadastro.mostrar("erro", "Preencha os campos obrigatórios.")
            return

        vista = ler_numero(c, textos[0])
        entrada = ler_numero(c, textos[1])
        parcelas = ler_inteiro(textos[2])
        valor_parcela = ler_numero(c, textos[3])
        erros = []
        if vista is None or entrada is None or valor_parcela is None:
            erros.append("Use apenas números válidos nos campos de valor.")
        elif vista < 0 or entrada < 0 or valor_parcela < 0:
            erros.append("Não utilize valores negativos.")
        else:
            if vista <= 0:
                erros.append("O preço à vista deve ser maior que zero.")
            elif entrada >= vista:
                erros.append("A entrada deve ser menor que o preço à vista.")
            if valor_parcela <= 0:
                erros.append("O valor da parcela deve ser maior que zero.")
        if parcelas is None or parcelas <= 0:
            erros.append("Informe um número inteiro de parcelas maior que zero.")
        if not erros and entrada + parcelas * valor_parcela + 0.01 < vista:
            erros.append("O total parcelado não pode ser inferior ao preço à vista.")
        if erros:
            self.aviso_cadastro.mostrar("erro", "Revise os campos antes de continuar:\n• " + "\n• ".join(erros))
            return

        try:
            oferta = c.criar_oferta(loja, produto, vista, parcelas, valor_parcela, entrada)
            c.validar_oferta(oferta)
        except ValueError as erro:
            self.aviso_cadastro.mostrar("erro", str(erro))
            return
        c.OFERTAS_REAIS.append(oferta)
        self.ultimo_cadastro = len(c.OFERTAS_REAIS) - 1
        for campo in self.campos.values():
            campo.definir("")
        self.aviso_cadastro.ocultar()
        self._atualizar_produtos()
        self.trocar_aba("todas")
        self.aviso_todas.mostrar("sucesso", "Oferta cadastrada com sucesso. " + loja + " · "
                                 + produto + " já está disponível na consulta.")

    # ---------------------------------------------------------- aba 3: todas

    def _montar_todas(self):
        vista = tk.Frame(self.area, bg=COR_FUNDO)
        self.aviso_todas = Aviso(vista)
        self.aviso_todas.pack(fill="x")
        cabecalho = tk.Frame(vista, bg=COR_FUNDO)
        cabecalho.pack(fill="x", pady=(0, 8))
        rotulo(cabecalho, "Todas as ofertas registradas", 15, "bold").pack(side="left")
        self.lbl_contagem = rotulo(cabecalho, "", 10, cor=COR_MUTED)
        self.lbl_contagem.pack(side="right")
        self.tabela_todas = Tabela(vista, [
            ("loja", "Loja", 150), ("produto", "Produto", 210), ("vista", "Preço à vista", 110),
            ("entrada", "Entrada", 100), ("parcelas", "Parcelas", 70),
            ("parcela", "Valor da parcela", 120), ("total", "Total a prazo", 120)], altura=8)
        self.tabela_todas.pack(fill="both", expand=True)
        rotulo(vista, "As versões de 256 GB e 512 GB são produtos distintos e são comparadas separadamente.",
               10, cor=COR_MUTED).pack(anchor="w", pady=(10, 0))
        return vista

    def _atualizar_todas(self):
        c = self.c
        linhas = []
        for indice, oferta in enumerate(c.OFERTAS_REAIS):
            try:
                total = c.formatar_reais(c.calcular_total_prazo(oferta))
            except ValueError:
                total = "—"
            linhas.append(((oferta["loja"], oferta["produto"], c.formatar_reais(oferta["valor_a_vista"]),
                            c.formatar_reais(oferta["entrada"]), oferta["num_parcelas"],
                            c.formatar_reais(oferta["valor_parcela"]), total),
                           "verde" if indice == self.ultimo_cadastro else ""))
        self.tabela_todas.preencher(linhas)
        self.lbl_contagem.configure(text=str(len(linhas)) + " ofertas registradas")


# =====================================================================
# PAGINA: SIMULAR PARCELAMENTO
# =====================================================================


class PaginaSimulacao(Pagina):
    """Opcao 2 do menu: simulacao por banco emissor e plataforma."""

    def __init__(self, app, pai):
        Pagina.__init__(self, app, pai, "Simulador de Parcelamento",
                        "Descubra como a taxa bancária e o prazo de pagamento influenciam o custo final de uma compra.")
        self.formulario = tk.Frame(self.corpo, bg=COR_FUNDO)
        self.resultado = tk.Frame(self.corpo, bg=COR_FUNDO)
        self._montar_formulario()
        self.mostrar_formulario()

    def mostrar_formulario(self):
        """Volta para a tela de entrada de dados."""
        self.resultado.pack_forget()
        self.formulario.pack(fill="both", expand=True)
        self.definir_cabecalho()

    def _montar_formulario(self):
        c = self.c
        f = self.formulario
        linha = tk.Frame(f, bg=COR_FUNDO)
        linha.pack(fill="x")
        esquerda = Card(linha, padx=24, pady=18)
        direita = Card(linha, padx=24, pady=18)
        distribuir(linha, [esquerda, direita], 18)

        rotulo(esquerda.corpo, "01   Dados do produto", 15, "bold").pack(anchor="w", pady=(0, 12))
        self.f_modelo = Campo(esquerda.corpo, "Nome/modelo do smartphone")
        self.f_preco = Campo(esquerda.corpo, "Preço-base normal no cartão (R$)")
        self.f_entrada = Campo(esquerda.corpo, "Valor da entrada (R$)", "0,00")
        for campo in (self.f_modelo, self.f_preco, self.f_entrada):
            campo.pack(fill="x", pady=(0, 10))

        rotulo(direita.corpo, "02   Configurações financeiras", 15, "bold").pack(anchor="w", pady=(0, 12))
        self.f_banco = CampoLista(direita.corpo, "Banco/emissor do cartão", c.BANCOS_CARTAO)
        self.f_plataforma = CampoLista(direita.corpo, "Plataforma", c.PLATAFORMAS)
        self.f_banco.pack(fill="x", pady=(0, 10))
        self.f_plataforma.pack(fill="x", pady=(0, 10))
        par = tk.Frame(direita.corpo, bg=COR_CARD)
        par.pack(fill="x")
        self.f_parcelas = Campo(par, "Máximo de parcelas (1 a 48)", "12")
        self.f_limite = Campo(par, "Limite mensal (R$)", "0")
        self.f_parcelas.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.f_limite.grid(row=0, column=1, sticky="ew", padx=(8, 0))
        par.columnconfigure(0, weight=1, uniform="p")
        par.columnconfigure(1, weight=1, uniform="p")
        rotulo(direita.corpo, "Use zero no limite para não filtrar por orçamento.", 9,
               cor=COR_MUTED).pack(anchor="w", pady=(8, 0))

        info = Card(f, bg=COR_AZUL_CLARO, borda=COR_AZUL_CLARO, padx=22, pady=14)
        info.pack(fill="x", pady=(14, 8))
        rotulo(info.corpo, "Sobre esta simulação", 11, "bold").pack(anchor="w")
        rotulo(info.corpo, "As taxas bancárias são referências médias do Banco Central do Brasil (período: "
               + c.PERIODO_TAXAS_BCB + "). A taxa real depende do contrato e do CET.", 10,
               cor=COR_MUTED, quebra=800).pack(anchor="w", pady=(4, 0))
        rotulo(info.corpo, "O desconto Pix usa a média das amostras do grupo. A menor parcela não "
               "significa o menor custo total.", 10, cor=COR_MUTED, quebra=800).pack(anchor="w")

        self.aviso = Aviso(f)
        self.aviso.pack(fill="x")
        rodape = tk.Frame(f, bg=COR_FUNDO)
        rodape.pack(fill="x")
        Botao(rodape, "Calcular simulação", self.calcular, pady=11, padx=34).pack(side="right")

    def calcular(self):
        """Valida os campos e gera a comparacao de prazos."""
        c = self.c
        modelo = self.f_modelo.obter().strip()
        preco = ler_numero(c, self.f_preco.obter())
        entrada = ler_numero(c, self.f_entrada.obter())
        max_parcelas = ler_inteiro(self.f_parcelas.obter())
        limite = ler_numero(c, self.f_limite.obter())
        erros = []
        if not modelo:
            erros.append("Informe o nome/modelo do smartphone.")
        if preco is None or preco <= 0:
            erros.append("Informe um preço-base maior que zero.")
        if entrada is None or entrada < 0:
            erros.append("Informe uma entrada válida (0 se não houver).")
        elif preco is not None and preco > 0 and entrada >= preco:
            erros.append("A entrada deve ser menor que o preço-base.")
        if max_parcelas is None or not 1 <= max_parcelas <= 48:
            erros.append("O máximo de parcelas deve ser um inteiro de 1 a 48.")
        if limite is None or limite < 0:
            erros.append("Informe um limite mensal válido (0 para não filtrar).")
        if erros:
            self.aviso.mostrar("erro", "Revise os campos antes de continuar:\n• " + "\n• ".join(erros))
            return

        banco = self.f_banco.obter()
        plataforma = self.f_plataforma.obter()
        try:
            resultados = c.simular_faixa_parcelas(plataforma, banco, preco, entrada, max_parcelas, limite)
            taxa = c.obter_media_taxa_banco(banco)
            desconto = c.obter_media_desconto(plataforma)
            preco_pix = c.calcular_preco_pix(preco, desconto)
        except (ValueError, TypeError) as erro:
            self.aviso.mostrar("erro", "Não foi possível simular: " + str(erro))
            return
        if not resultados:
            self.aviso.mostrar("erro", "Não há dados de taxa/desconto para essa combinação.")
            return
        self.aviso.ocultar()
        self._montar_resultado(modelo, banco, plataforma, preco, entrada, limite,
                               resultados, taxa, desconto, preco_pix)

    def _montar_resultado(self, modelo, banco, plataforma, preco, entrada, limite,
                          resultados, taxa, desconto, preco_pix):
        c = self.c
        limpar(self.resultado)
        self.formulario.pack_forget()
        self.resultado.pack(fill="both", expand=True)
        self.definir_cabecalho("Resultado da simulação",
                               "Compare todos os prazos e encontre a condição adequada ao seu orçamento.")

        topo = tk.Frame(self.resultado, bg=COR_FUNDO)
        topo.pack(fill="x")
        textos = tk.Frame(topo, bg=COR_FUNDO)
        textos.pack(side="left")
        rotulo(textos, modelo, 16, "bold").pack(anchor="w")
        limite_txt = ("Limite " + c.formatar_reais(limite) + "/mês") if limite > 0 else "Sem limite mensal"
        rotulo(textos, "Cartão " + c.formatar_reais(preco) + "  ·  Entrada " + c.formatar_reais(entrada)
               + "  ·  " + limite_txt, 10, cor=COR_MUTED).pack(anchor="w")
        Botao(topo, "Ajustar simulação", self.mostrar_formulario, "secundario", pady=11, padx=24).pack(side="right")

        cartoes = tk.Frame(self.resultado, bg=COR_FUNDO)
        cartoes.pack(fill="x", pady=10)
        distribuir(cartoes, [
            cartao_metrica(cartoes, "BANCO", banco, tamanho=15),
            cartao_metrica(cartoes, "TAXA MENSAL", c.formatar_percentual(taxa) + " a.m.", tamanho=15),
            cartao_metrica(cartoes, "PLATAFORMA", plataforma, tamanho=15),
            cartao_metrica(cartoes, "DESCONTO PIX", c.formatar_percentual(desconto), tamanho=15),
            cartao_metrica(cartoes, "PREÇO NO PIX", c.formatar_reais(preco_pix),
                           cor_valor=COR_AZUL, tamanho=15),
        ], 12)

        menor_total = resultados[0]
        menor_parcela = resultados[0]
        compativel = None
        for registro in resultados:
            if registro["total"] < menor_total["total"]:
                menor_total = registro
            if registro["parcela"] < menor_parcela["parcela"]:
                menor_parcela = registro
            if compativel is None and registro["cabe_orcamento"]:
                compativel = registro

        # Elementos do rodape primeiro (side="bottom"), para a tabela ocupar o resto.
        rotulo(self.resultado, "Parcela fixa pelo modelo Price (1ª parcela em 1 mês). Total = entrada + parcelas. "
               "Taxa real sujeita ao contrato e ao CET · Menor parcela ≠ menor custo total.",
               9, cor=COR_MUTED, quebra=830).pack(side="bottom", anchor="w")
        if limite <= 0:
            tit_comp, val_comp, det_comp = "Compatível com orçamento", "Sem filtro", "Limite mensal não informado"
        elif compativel is None:
            tit_comp, val_comp, det_comp = "Compatível com orçamento", "Nenhum prazo", "Nenhum prazo atende ao limite mensal"
        else:
            tit_comp = "Compatível com orçamento"
            val_comp = "Primeiro prazo: " + str(compativel["parcelas"]) + " parcelas"
            det_comp = c.formatar_reais(compativel["parcela"]) + "/mês · total " + c.formatar_reais(compativel["total"])
        resumo = tk.Frame(self.resultado, bg=COR_FUNDO)
        resumo.pack(side="bottom", fill="x", pady=(10, 8))
        distribuir(resumo, [
            cartao_metrica(resumo, "Menor custo total",
                           str(menor_total["parcelas"]) + " × " + c.formatar_reais(menor_total["parcela"]),
                           "Total final: " + c.formatar_reais(menor_total["total"]), cor_titulo=COR_AZUL, tamanho=17),
            cartao_metrica(resumo, "Menor parcela mensal",
                           str(menor_parcela["parcelas"]) + " × " + c.formatar_reais(menor_parcela["parcela"]),
                           "Total final: " + c.formatar_reais(menor_parcela["total"]), tamanho=17),
            cartao_metrica(resumo, tit_comp, val_comp, det_comp, cor_titulo=COR_VERDE, tamanho=17),
        ], 12)

        rotulo(self.resultado, taxa_aviso(c), 9, cor=COR_AVISO, quebra=830).pack(side="bottom", anchor="w")

        tabela = Tabela(self.resultado, [
            ("n", "Nº de parcelas", 150), ("valor", "Valor mensal", 170),
            ("total", "Total a prazo", 170), ("dif", "Diferença em relação ao Pix", 200)], altura=5)
        tabela.pack(fill="both", expand=True)
        linhas = []
        for registro in resultados:
            if limite > 0 and registro is compativel:
                tag = "verde"
            elif limite > 0 and not registro["cabe_orcamento"]:
                tag = "apagado"
            else:
                tag = ""
            n = registro["parcelas"]
            linhas.append(((str(n) + (" parcela" if n == 1 else " parcelas"),
                            c.formatar_reais(registro["parcela"]), c.formatar_reais(registro["total"]),
                            formatar_diferenca(c, registro["diferenca_pix"])), tag))
        tabela.preencher(linhas)


def taxa_aviso(comparador):
    """Texto de aviso sobre a origem das taxas e dos descontos."""
    return ("Taxas médias de referência do BCB (período: " + comparador.PERIODO_TAXAS_BCB
            + "); descontos Pix são médias das amostras do grupo.")


# =====================================================================
# PAGINA: PROJECAO DE JUROS COMPOSTOS COM K
# =====================================================================


class PaginaProjecao(Pagina):
    """Opcao 3 do menu: projecao de juros compostos usando o parametro K."""

    def __init__(self, app, pai):
        Pagina.__init__(self, app, pai, "Projeção de Juros Compostos",
                        "Visualize como o saldo de uma compra evolui ao longo dos meses considerando uma taxa de juros composta.")
        self.formulario = tk.Frame(self.corpo, bg=COR_FUNDO)
        self.resultado = tk.Frame(self.corpo, bg=COR_FUNDO)
        self._montar_formulario()
        self.mostrar_formulario()

    def mostrar_formulario(self):
        """Volta para a tela de entrada de dados."""
        self.resultado.pack_forget()
        self.formulario.pack(fill="both", expand=True)
        self.definir_cabecalho()

    def _montar_formulario(self):
        c = self.c
        taxa, meses = c.calcular_parametros_k(c.K)
        f = self.formulario
        linha = tk.Frame(f, bg=COR_FUNDO)
        linha.pack(fill="x")
        esquerda = Card(linha, padx=26, pady=20)
        direita = Card(linha, bg=COR_AZUL_CLARO, borda="#C5D5F4", padx=26, pady=20)
        linha.columnconfigure(0, weight=3, uniform="proj")
        linha.columnconfigure(1, weight=2, uniform="proj")
        esquerda.grid(row=0, column=0, sticky="nsew", padx=(0, 18))
        direita.grid(row=0, column=1, sticky="nsew")

        rotulo(esquerda.corpo, "Dados da compra", 16, "bold").pack(anchor="w", pady=(0, 14))
        self.f_modelo = Campo(esquerda.corpo, "Nome/modelo do smartphone")
        self.f_preco = Campo(esquerda.corpo, "Preço-base no cartão (R$)")
        self.f_modelo.pack(fill="x", pady=(0, 12))
        self.f_preco.pack(fill="x")
        rotulo(esquerda.corpo, "O preço informado será o capital inicial da projeção.", 10,
               cor=COR_MUTED).pack(anchor="w", pady=(10, 0))

        rotulo(direita.corpo, "PARÂMETRO DO PROJETO", 9, "bold", COR_AZUL).pack(anchor="w")
        rotulo(direita.corpo, "K = " + str(c.K), 30, "bold").pack(anchor="w", pady=(6, 0))
        rotulo(direita.corpo, "Valor definido pelo projeto", 10, cor=COR_MUTED).pack(anchor="w", pady=(0, 14))
        rotulo(direita.corpo, "Taxa mensal = (K % 5) + 1", 11).pack(anchor="w")
        rotulo(direita.corpo, str(taxa) + "% ao mês", 16, "bold", COR_AZUL).pack(anchor="w", pady=(0, 10))
        rotulo(direita.corpo, "Prazo = (K % 6) + 6", 11).pack(anchor="w")
        rotulo(direita.corpo, str(meses) + " meses", 16, "bold", COR_AZUL).pack(anchor="w", pady=(0, 10))
        rotulo(direita.corpo, "A taxa e o prazo não podem ser alterados nesta tela.", 9,
               cor=COR_MUTED).pack(anchor="w")

        explica = Card(f, padx=26, pady=14)
        explica.pack(fill="x", pady=(14, 8))
        rotulo(explica.corpo, "Entenda o cálculo", 12, "bold").pack(anchor="w")
        rotulo(explica.corpo, "O saldo é atualizado a cada mês pela fórmula M = C × (1 + i)ⁿ, "
               "sem amortização por parcelas.", 10, cor=COR_MUTED).pack(anchor="w", pady=(4, 2))
        rotulo(explica.corpo, "Esta projeção é acadêmica e não representa uma oferta real de crédito.",
               10, cor=COR_AVISO).pack(anchor="w")

        self.aviso = Aviso(f)
        self.aviso.pack(fill="x")
        rodape = tk.Frame(f, bg=COR_FUNDO)
        rodape.pack(fill="x")
        rotulo(rodape, "Taxa e prazo calculados automaticamente a partir de K.", 10,
               cor=COR_MUTED).pack(side="left")
        Botao(rodape, "Gerar projeção", self.gerar, pady=11, padx=34).pack(side="right")

    def gerar(self):
        """Valida os campos e gera a projecao mes a mes."""
        c = self.c
        modelo = self.f_modelo.obter().strip()
        capital = ler_numero(c, self.f_preco.obter())
        erros = []
        if not modelo:
            erros.append("Informe o nome/modelo do smartphone.")
        if capital is None or capital <= 0:
            erros.append("Informe um preço-base numérico maior que zero.")
        if erros:
            self.aviso.mostrar("erro", "Revise os campos antes de continuar:\n• " + "\n• ".join(erros))
            return
        try:
            taxa, meses = c.calcular_parametros_k(c.K)
            historico = c.simular_juros_compostos(capital, taxa, meses)
        except ValueError as erro:
            self.aviso.mostrar("erro", str(erro))
            return
        self.aviso.ocultar()
        self._montar_resultado(modelo, capital, taxa, meses, historico)

    def _montar_resultado(self, modelo, capital, taxa, meses, historico):
        c = self.c
        limpar(self.resultado)
        self.formulario.pack_forget()
        self.resultado.pack(fill="both", expand=True)
        self.definir_cabecalho("Resultado da projeção", "Acompanhe a evolução mensal do saldo e dos juros acumulados.")

        topo = tk.Frame(self.resultado, bg=COR_FUNDO)
        topo.pack(fill="x")
        textos = tk.Frame(topo, bg=COR_FUNDO)
        textos.pack(side="left")
        rotulo(textos, modelo, 16, "bold").pack(anchor="w")
        rotulo(textos, "K = " + str(c.K) + "  ·  Atualização por juros compostos  ·  Sem amortização",
               10, cor=COR_MUTED).pack(anchor="w")
        Botao(topo, "Nova projeção", self.mostrar_formulario, "secundario", pady=11, padx=24).pack(side="right")

        cartoes = tk.Frame(self.resultado, bg=COR_FUNDO)
        cartoes.pack(fill="x", pady=10)
        final = historico[-1]
        distribuir(cartoes, [
            cartao_metrica(cartoes, "Capital inicial", c.formatar_reais(capital), "Valor informado"),
            cartao_metrica(cartoes, "Taxa mensal", c.formatar_percentual(taxa), "Definida pelo K"),
            cartao_metrica(cartoes, "Prazo", str(meses) + " meses", "Definido pelo K"),
            cartao_metrica(cartoes, "Montante final", c.formatar_reais(final["saldo"]), "Ao final do período",
                           bg=COR_AZUL_CLARO, borda="#C5D5F4"),
            cartao_metrica(cartoes, "Juros acumulados", c.formatar_reais(final["juros_acumulados"]),
                           "Montante − capital", bg=COR_VERM_BG, borda="#F2C9C5"),
        ], 12)

        rotulo(self.resultado, "Esta projeção é acadêmica e não representa uma oferta real de crédito.",
               10, cor=COR_AVISO).pack(side="bottom", anchor="w", pady=(6, 0))
        cab = tk.Frame(self.resultado, bg=COR_FUNDO)
        cab.pack(fill="x", pady=(2, 8))
        rotulo(cab, "Evolução mensal", 14, "bold").pack(side="left")
        rotulo(cab, "Saldo inicial: " + c.formatar_reais(capital), 10, cor=COR_MUTED).pack(side="right")

        tabela = Tabela(self.resultado, [
            ("mes", "Mês", 120), ("saldo", "Saldo atualizado", 200),
            ("juros", "Juros do mês", 200), ("acum", "Juros acumulados", 200)], altura=6)
        tabela.pack(fill="both", expand=True)
        linhas = []
        for item in historico:
            ultimo = item is final
            nome_mes = ("%02d" % item["mes"]) + (" · final" if ultimo else "")
            linhas.append(((nome_mes, c.formatar_reais(item["saldo"]), c.formatar_reais(item["juros_mes"]),
                            c.formatar_reais(item["juros_acumulados"])), "destaque" if ultimo else ""))
        tabela.preencher(linhas)


# =====================================================================
# JANELA PRINCIPAL
# =====================================================================


class App(tk.Tk):
    """Janela principal: barra lateral de navegacao + area de conteudo."""

    MENU = [
        ("inicio", "⌂", "Início"),
        ("comparacao", "▥", "Comparar Ofertas"),
        ("simulacao", "▦", "Simular Parcelamento"),
        ("projecao", "↗", "Projeção com K"),
    ]

    def __init__(self, comparador):
        tk.Tk.__init__(self)
        self.c = comparador
        self.title("Comparador de Compras Parceladas")
        largura = 1180
        altura = min(780, self.winfo_screenheight() - 90)
        x = max(0, (self.winfo_screenwidth() - largura) // 2)
        y = max(0, (self.winfo_screenheight() - altura) // 2 - 20)
        self.geometry(str(largura) + "x" + str(altura) + "+" + str(x) + "+" + str(y))
        self.minsize(1040, 640)
        self.configure(bg=COR_FUNDO)
        self._escolher_fonte()
        self._configurar_estilos()

        self.itens = {}
        self._montar_barra_lateral()
        self.conteudo = tk.Frame(self, bg=COR_FUNDO)
        self.conteudo.pack(side="right", fill="both", expand=True)
        self.paginas = {
            "inicio": PaginaInicio(self, self.conteudo),
            "comparacao": PaginaComparacao(self, self.conteudo),
            "simulacao": PaginaSimulacao(self, self.conteudo),
            "projecao": PaginaProjecao(self, self.conteudo),
        }
        self.atual = None
        self.mostrar("inicio")

    def _escolher_fonte(self):
        """Usa a primeira fonte disponivel entre as preferidas."""
        global FONTE
        instaladas = set(tkfont.families(self))
        for nome in ("Inter", "Segoe UI", "SF Pro Text", "Helvetica Neue", "Arial"):
            if nome in instaladas:
                FONTE = nome
                break

    def _configurar_estilos(self):
        """Estilos ttk para tabela e lista suspensa."""
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("App.Treeview", background="#FFFFFF", fieldbackground="#FFFFFF",
                         foreground=COR_TEXTO, rowheight=32, borderwidth=0, font=fonte(10))
        estilo.configure("App.Treeview.Heading", background="#EEF2F8", foreground=COR_MUTED,
                         font=fonte(9, "bold"), relief="flat", padding=(10, 9))
        estilo.map("App.Treeview.Heading", background=[("active", "#EEF2F8")])
        estilo.map("App.Treeview", background=[("selected", COR_AZUL_CLARO)],
                   foreground=[("selected", COR_TEXTO)])
        estilo.layout("App.Treeview", [("Treeview.treearea", {"sticky": "nswe"})])
        estilo.configure("App.TCombobox", fieldbackground="#FFFFFF", background="#FFFFFF",
                         foreground=COR_TEXTO, bordercolor=COR_BORDA, lightcolor=COR_BORDA,
                         darkcolor=COR_BORDA, arrowcolor=COR_MUTED, padding=6)
        estilo.map("App.TCombobox", fieldbackground=[("readonly", "#FFFFFF")],
                   bordercolor=[("focus", COR_AZUL)], lightcolor=[("focus", COR_AZUL)])
        self.option_add("*TCombobox*Listbox.font", fonte(11))

    def _montar_barra_lateral(self):
        lateral = tk.Frame(self, bg=COR_SIDEBAR, width=236)
        lateral.pack(side="left", fill="y")
        lateral.pack_propagate(False)

        marca = tk.Frame(lateral, bg=COR_SIDEBAR)
        marca.pack(fill="x", padx=18, pady=(22, 28))
        tk.Label(marca, text="▥", font=fonte(15, "bold"), fg="#FFFFFF", bg=COR_AZUL,
                 width=3).pack(side="left")
        textos = tk.Frame(marca, bg=COR_SIDEBAR)
        textos.pack(side="left", padx=(12, 0))
        rotulo(textos, "COMPARADOR", 10, "bold", "#FFFFFF").pack(anchor="w")
        rotulo(textos, "Compras Parceladas", 9, cor="#A9B8D1").pack(anchor="w")

        rotulo(lateral, "PRINCIPAL", 8, "bold", "#8FA3C4").pack(anchor="w", padx=22, pady=(0, 8))
        for chave, icone, texto in self.MENU:
            item = tk.Label(lateral, text=" " + icone + "   " + texto, anchor="w", font=fonte(10),
                            fg="#D7E0F0", bg=COR_SIDEBAR, padx=10, pady=11, cursor="hand2")
            item.pack(fill="x", padx=12, pady=2)
            item.bind("<Button-1>", lambda evento, k=chave: self.mostrar(k))
            item.bind("<Enter>", lambda evento, k=chave: self._hover(k, True))
            item.bind("<Leave>", lambda evento, k=chave: self._hover(k, False))
            self.itens[chave] = item

        rodape = tk.Frame(lateral, bg=COR_SIDEBAR)
        rodape.pack(side="bottom", fill="x", padx=22, pady=(0, 20))
        tk.Frame(rodape, bg="#2B3D5C", height=1).pack(fill="x", pady=(0, 14))
        rotulo(rodape, "PROJETO 15", 10, "bold", "#FFFFFF").pack(anchor="w")
        rotulo(rodape, "Análise de compras parceladas", 9, cor="#8FA3C4").pack(anchor="w")

    def _hover(self, chave, dentro):
        """Realce ao passar o mouse nos itens inativos do menu."""
        if chave != self.atual:
            self.itens[chave].configure(bg="#1B3157" if dentro else COR_SIDEBAR)

    def mostrar(self, chave):
        """Troca a pagina exibida e destaca o item do menu."""
        if self.atual is not None:
            self.paginas[self.atual].pack_forget()
        self.atual = chave
        for nome, item in self.itens.items():
            ativo = nome == chave
            item.configure(bg=COR_SIDEBAR_ATIVO if ativo else COR_SIDEBAR,
                           fg="#FFFFFF" if ativo else "#D7E0F0",
                           font=fonte(10, "bold" if ativo else "normal"))
        pagina = self.paginas[chave]
        pagina.pack(fill="both", expand=True)
        pagina.ao_exibir()


def abrir_interface(comparador=None):
    """Abre a janela. Se nenhum modulo for informado, importa o Comparador.py."""
    if comparador is None:
        import Comparador as comparador
    App(comparador).mainloop()


if __name__ == "__main__":
    abrir_interface()
