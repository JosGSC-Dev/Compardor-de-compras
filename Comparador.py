#Código principal
"""
Projeto 15 - Comparador de Compras Parceladas
Eduardo Soares Portela - Calculos financeiros e comparacao de ofertas

Cada oferta e um dicionario:
    {
        "loja": str,
        "produto": str,
        "valor_a_vista": float,
        "entrada": float,
        "num_parcelas": int,
        "valor_parcela": float,
    }

Formulas:
    Total a prazo = entrada + (num_parcelas * valor_parcela)
    Juros (R$)    = total a prazo - valor a vista
    Juros (%)     = (juros em R$ / valor a vista) * 100
"""
#Autor: Eduardo Soares Portela

# ---------------------------------------------------------------------------
# Funcoes auxiliares
# ---------------------------------------------------------------------------
def formatar_reais(valor):
    """Formata como moeda brasileira: 10599.0 -> 'R$ 10.599,00'."""
    texto = f"{valor:,.2f}"                       # 10,599.00
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def validar_oferta(oferta):
    """Levanta ValueError se a oferta tiver dados invalidos."""
    if oferta["num_parcelas"] <= 0:
        raise ValueError(
            f"Numero de parcelas invalido ({oferta['num_parcelas']}) "
            f"na oferta de {oferta['loja']}."
        )
    if oferta["valor_parcela"] < 0 or oferta["entrada"] < 0:
        raise ValueError(f"Valor negativo na oferta de {oferta['loja']}.")
    if oferta["valor_a_vista"] <= 0:
        raise ValueError(f"Valor a vista invalido na oferta de {oferta['loja']}.")


# ---------------------------------------------------------------------------
# Funcoes principais
# ---------------------------------------------------------------------------
def calcular_total_prazo(oferta):
    """Retorna entrada + (parcelas * valor da parcela), arredondado a 2 casas."""
    validar_oferta(oferta)
    entrada = oferta["entrada"]
    parcelas = oferta["num_parcelas"]
    valor_parcela = oferta["valor_parcela"]
    total = entrada + (parcelas * valor_parcela)
    return round(total, 2)


def calcular_juros(oferta):
    """Retorna (juros em R$, juros em %) sobre o valor a vista."""
    total = calcular_total_prazo(oferta)
    a_vista = oferta["valor_a_vista"]
    juros_reais = round(total - a_vista, 2)
    juros_percentual = (juros_reais / a_vista) * 100
    return juros_reais, juros_percentual


def achar_mais_barata(ofertas):
    """Retorna a LISTA de ofertas com menor total a prazo (varias se houver empate)."""
    if len(ofertas) == 0:
        return []
    menor_total = calcular_total_prazo(ofertas[0])
    vencedoras = [ofertas[0]]
    for oferta in ofertas[1:]:
        total = calcular_total_prazo(oferta)
        if total < menor_total:
            menor_total = total
            vencedoras = [oferta]
        elif total == menor_total:
            vencedoras.append(oferta)
    return vencedoras


def achar_mais_cara(ofertas):
    """Retorna a LISTA de ofertas com maior total a prazo (varias se houver empate)."""
    if len(ofertas) == 0:
        return []
    maior_total = calcular_total_prazo(ofertas[0])
    vencedoras = [ofertas[0]]
    for oferta in ofertas[1:]:
        total = calcular_total_prazo(oferta)
        if total > maior_total:
            maior_total = total
            vencedoras = [oferta]
        elif total == maior_total:
            vencedoras.append(oferta)
    return vencedoras


def exibir_tabela(ofertas):
    """Imprime a tabela comparativa das ofertas, alinhada com f-strings."""
    cab = (f"{'Loja':<16}{'A vista':>14}{'Entrada':>12}{'Parcelas':>18}"
           f"{'Total a prazo':>16}{'Juros R$':>13}{'Juros %':>10}")
    linha = "-" * len(cab)
    print(linha)
    print(cab)
    print(linha)
    for oferta in ofertas:
        total = calcular_total_prazo(oferta)
        juros_r, juros_p = calcular_juros(oferta)
        parcelas = f"{oferta['num_parcelas']}x {formatar_reais(oferta['valor_parcela'])}"
        print(f"{oferta['loja']:<16}"
              f"{formatar_reais(oferta['valor_a_vista']):>14}"
              f"{formatar_reais(oferta['entrada']):>12}"
              f"{parcelas:>18}"
              f"{formatar_reais(total):>16}"
              f"{formatar_reais(juros_r):>13}"
              f"{juros_p:>9.2f}%")
    print(linha)


def _nomes(lista):
    return ", ".join(o["loja"] for o in lista)


def exibir_resumo(ofertas):
    """Mostra a(s) oferta(s) mais barata(s) e mais cara(s)."""
    barata = achar_mais_barata(ofertas)
    cara = achar_mais_cara(ofertas)
    print(f"Mais barata: {_nomes(barata)} "
          f"({formatar_reais(calcular_total_prazo(barata[0]))})"
          + ("  [EMPATE]" if len(barata) > 1 else ""))
    print(f"Mais cara:   {_nomes(cara)} "
          f"({formatar_reais(calcular_total_prazo(cara[0]))})"
          + ("  [EMPATE]" if len(cara) > 1 else ""))


# ---------------------------------------------------------------------------
# Dados reais coletados (prints do grupo). Entrada = 0 em todas.
# valor_a_vista = preco no Pix / a vista exibido na loja.
# ---------------------------------------------------------------------------
def _oferta(loja, produto, a_vista, parcelas, valor_parcela, entrada=0.0):
    return {"loja": loja, "produto": produto, "valor_a_vista": a_vista,
            "entrada": entrada, "num_parcelas": parcelas,
            "valor_parcela": valor_parcela}


# Atencao: a oferta do Mercado Livre e de 512 GB (as outras sao 256 GB).
OFERTAS_IPHONE = [
    _oferta("Amazon", "iPhone 17 Pro Max 256 GB", 9998.99, 12, 883.25),
    _oferta("Magazine Luiza", "iPhone 17 Pro Max 256 GB", 11494.05, 10, 1209.90),
    _oferta("Mercado Livre", "iPhone 17 Pro Max 512 GB", 10799.00, 10, 1199.90),
]

# Mesmo produto (POCO C85 256 GB / 8 GB) em duas lojas.
OFERTAS_POCO_C85 = [
    _oferta("Amazon", "POCO C85 256 GB", 1182.09, 12, 108.25),
    _oferta("Mercado Livre", "POCO C85 256 GB", 1278.99, 10, 139.56),
]


# Galaxy Z Flip 8 (Samsung). ATENCAO: capacidades diferentes (256 GB x 512 GB).
# A Magazine Luiza tem duas opcoes de parcelamento para o mesmo aparelho.
OFERTAS_Z_FLIP8 = [
    _oferta("Magalu 10x", "Galaxy Z Flip 8 256 GB", 7739.10, 10, 859.90),
    _oferta("Magalu 21x", "Galaxy Z Flip 8 256 GB", 7739.10, 21, 409.48),
    _oferta("Mercado Livre", "Galaxy Z Flip 8 512 GB", 6699.00, 12, 643.89),
]


# ---------------------------------------------------------------------------
# Testes (valores conferidos manualmente - veja os comentarios)
#parte feita pela IA
# ---------------------------------------------------------------------------
def aproximado(a, b, tol=0.005):
    return abs(a - b) <= tol


def rodar_testes():
    # 1) Oferta SEM juros: 10 x 100 = 1000 = valor a vista
    sem_juros = _oferta("Loja Teste", "Produto", 1000.00, 10, 100.00)
    assert calcular_total_prazo(sem_juros) == 1000.00
    assert calcular_juros(sem_juros) == (0.0, 0.0)

    # 2) Oferta COM entrada (mao): 200 + 4*250 = 1200; juros = 200 (20%) sobre 1000
    com_entrada = _oferta("Loja A", "Produto", 1000.00, 4, 250.00, entrada=200.00)
    assert calcular_total_prazo(com_entrada) == 1200.00
    j_r, j_p = calcular_juros(com_entrada)
    assert j_r == 200.00 and aproximado(j_p, 20.0)

    # 3) Oferta SEM entrada (mao): 5*220 = 1100; juros = 100 (10%) sobre 1000
    sem_entrada = _oferta("Loja B", "Produto", 1000.00, 5, 220.00)
    assert calcular_total_prazo(sem_entrada) == 1100.00
    j_r, j_p = calcular_juros(sem_entrada)
    assert j_r == 100.00 and aproximado(j_p, 10.0)

    # 4) Ofertas reais - iPhone (conferido a mao)
    #    Amazon: 12*883,25 = 10.599,00 ; juros = 10.599,00 - 9.998,99 = 600,01 ; 6,00%
    amazon, magalu, ml = OFERTAS_IPHONE
    assert calcular_total_prazo(amazon) == 10599.00
    j_r, j_p = calcular_juros(amazon)
    assert j_r == 600.01 and aproximado(j_p, 6.00)
    #    Magalu: 10*1.209,90 = 12.099,00 ; juros = 604,95 ; 5,26%
    assert calcular_total_prazo(magalu) == 12099.00
    j_r, j_p = calcular_juros(magalu)
    assert j_r == 604.95 and aproximado(j_p, 5.26)
    #    Mercado Livre: 10*1.199,90 = 11.999,00 ; juros = 1.200,00 ; 11,11%
    assert calcular_total_prazo(ml) == 11999.00
    j_r, j_p = calcular_juros(ml)
    assert j_r == 1200.00 and aproximado(j_p, 11.11)

    # 5) Mais barata e mais cara (iPhone)
    assert achar_mais_barata(OFERTAS_IPHONE) == [amazon]
    assert achar_mais_cara(OFERTAS_IPHONE) == [magalu]

    # 6) POCO C85 (mao): Amazon 12*108,25 = 1.299,00 -> juros 116,91 (9,89%)
    #                    ML 10*139,56 = 1.395,60 -> juros 116,61 (9,12%)
    am, ml2 = OFERTAS_POCO_C85
    assert calcular_total_prazo(am) == 1299.00
    assert calcular_juros(am)[0] == 116.91
    assert aproximado(calcular_juros(am)[1], 9.89)
    assert calcular_total_prazo(ml2) == 1395.60
    assert calcular_juros(ml2)[0] == 116.61
    assert aproximado(calcular_juros(ml2)[1], 9.12)

    # 6b) Galaxy Z Flip 8 (conferido a mao)
    #    Magalu 10x: 10*859,90 = 8.599,00 ; juros = 8.599,00 - 7.739,10 = 859,90 ; 11,11%
    #    Magalu 21x: 21*409,48 = 8.599,08 ; juros = 859,98 ; 11,11%
    #    Mercado Livre 12x: 12*643,89 = 7.726,68 ; juros = 7.726,68 - 6.699,00 = 1.027,68 ; 15,34%
    z10, z21, zml = OFERTAS_Z_FLIP8
    assert calcular_total_prazo(z10) == 8599.00
    assert calcular_juros(z10)[0] == 859.90
    assert aproximado(calcular_juros(z10)[1], 11.11)
    assert calcular_total_prazo(z21) == 8599.08
    assert calcular_juros(z21)[0] == 859.98
    assert aproximado(calcular_juros(z21)[1], 11.11)
    assert calcular_total_prazo(zml) == 7726.68
    assert calcular_juros(zml)[0] == 1027.68
    assert aproximado(calcular_juros(zml)[1], 15.34)
    assert achar_mais_barata(OFERTAS_Z_FLIP8) == [zml]
    assert achar_mais_cara(OFERTAS_Z_FLIP8) == [z21]

    # 7) EMPATE: duas ofertas com o mesmo total a prazo (1200)
    e1 = _oferta("Loja X", "Produto", 1000.00, 4, 250.00, entrada=200.00)  # 1200
    e2 = _oferta("Loja Y", "Produto", 1000.00, 6, 200.00)                  # 1200
    e3 = _oferta("Loja Z", "Produto", 1000.00, 10, 130.00)                 # 1300
    assert calcular_total_prazo(e1) == calcular_total_prazo(e2) == 1200.00
    assert achar_mais_barata([e1, e2, e3]) == [e1, e2]
    assert achar_mais_cara([e1, e2, e3]) == [e3]
    assert achar_mais_cara([e1, e2]) == [e1, e2]   # todas empatadas

    # 8) Entradas INVALIDAS: parcelas zero / negativas / valores negativos
    invalidos = [
        _oferta("Inv1", "P", 1000.00, 0, 100.00),
        _oferta("Inv2", "P", 1000.00, -3, 100.00),
        _oferta("Inv3", "P", 1000.00, 5, -50.00),
        _oferta("Inv4", "P", 1000.00, 5, 100.00, entrada=-10.00),
        _oferta("Inv5", "P", 0.00, 5, 100.00),
    ]
    for inv in invalidos:
        try:
            calcular_total_prazo(inv)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Deveria ter recusado {inv['loja']}")

    # 9) Lista vazia
    assert achar_mais_barata([]) == [] and achar_mais_cara([]) == []

    print("Todos os testes passaram.\n")

#fim da parte feita pela IA
# ---------------------------------------------------------------------------
#Autor: Eduardo Soares Portela:
if __name__ == "__main__":
    rodar_testes()

    print("=== iPhone 17 Pro Max (atencao: Mercado Livre e 512 GB) ===")
    exibir_tabela(OFERTAS_IPHONE)
    exibir_resumo(OFERTAS_IPHONE)

    print("\n=== POCO C85 256 GB / 8 GB (mesmo produto) ===")
    exibir_tabela(OFERTAS_POCO_C85)
    exibir_resumo(OFERTAS_POCO_C85)

    print("\n=== Galaxy Z Flip 8 (atencao: Magalu 256 GB x Mercado Livre 512 GB) ===")
    exibir_tabela(OFERTAS_Z_FLIP8)
    exibir_resumo(OFERTAS_Z_FLIP8)

    print("\n=== Teste de empate ===")
    empate = [
        _oferta("Loja X", "Produto", 1000.00, 4, 250.00, entrada=200.00),
        _oferta("Loja Y", "Produto", 1000.00, 6, 200.00),
        _oferta("Loja Z", "Produto", 1000.00, 10, 130.00),
    ]
    exibir_tabela(empate)
    exibir_resumo(empate)
