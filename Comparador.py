#Autor: Pedro Vitor
#Lê número inteiro positivo e maior que 0 e repete até ser válido
def ler_int_positivo(mensagem): 
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            print('Entrada inválida! Digite um número inteiro')
            continue

        if valor <= 0:
            print('O valor deve ser maior que zero')
        else:
            return valor


#[IA] Lê número decimal positivo e repete até ser válido
def ler_float_positivo(mensagem, permitir_zero=False):
    while True:
        try:
            valor = float(input (mensagem).replace(',','.'))
        except ValueError:
            print('Entrada inválida! Digite apenas números')
            continue

        if valor < 0:
            print('O valor não pode ser negativo')
        elif valor == 0 and not permitir_zero:
            print('O valor não pode ser zero')
        else:
            return valor                           


#Cadastra ofertas e adiciona na lista
def cadastrar_oferta(ofertas): 
    loja = input('Informe o nome da loja:')
    produto = input('Informe o produto:')
    valor_vista = ler_float_positivo('Preço à vista: R$')

#Entrada tem que ser menor que o valor à vista
    while True:
        entrada = ler_float_positivo('Valor da entrada (0 se não tiver): R$', permitir_zero=True)

        if entrada >= valor_vista:
            print('A entrada deve ser menor que o preço à vista.')
        else:
            break
    
    parcelas = ler_int_positivo('Número de parcelas:')

#Total a prazo não pode ser menor que o valor à vista
    margem = parcelas * 0.01
    while True:
        valor_parcela = ler_float_positivo('Valor de cada parcela: R$')
        total_prazo = entrada + parcelas * valor_parcela
        if total_prazo + margem < valor_vista:
            minimo = (valor_vista - entrada) / parcelas
            print(f'Total a prazo (R$ {total_prazo:.2f}) menor que o preço à vista')
            print(f'Cada parcela deve ser de pelo menos R$ {minimo:.2f}')
        else:
            break

    oferta = {
        'loja': loja,
        'produto': produto,
        'valor_vista': valor_vista,
        'entrada': entrada,
        'parcelas': parcelas,
        'valor_parcela': valor_parcela,
    }
    ofertas.append(oferta)
    print('Oferta cadastrada!')


def menu():
    oferta = []

    while True:
        print('\n--- MENU ---')
        print('1. Cadastrar oferta')
        print('2. Consultar informações')
        print('0. Sair')

        opcao = input('Escolha uma opção:')

        if opcao == '1':
            cadastrar_oferta(oferta)

        elif opcao == '2':                            
            if not oferta:
                print('Nenhuma oferta cadastrada ainda')
            else: #[IA]            
                for i, o in enumerate(oferta, start=1):
                    print(f"{i}. {o['loja']} - {o['produto']} |"
                          f"À vista R$ {o['valor_vista']:.2f} |"
                          f"Entrada R$ {o['entrada']:.2f} + "
                          f"{o['parcelas']} x R$ {o['valor_parcela']:.2f}") #[IA]

        elif opcao == '0':
            print('Saindo...')
            break

        else:
            print('Opção inválida')


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


"""Projeto 15 - Parte do Integrante 3.

Responsabilidades: juros compostos, testes, integração e apoio ao relatório.

INTEGRACAO:
- Este trecho deve ser copiado para o arquivo principal do grupo.
- Mantenha apenas uma variável global K no programa.
- A funcao executar_projecao_k reutiliza ler_texto, ler_float,
  formatar_moeda e formatar_percentual, ja existentes no programa principal.
- executar_testes_integracao depende das funcoes das tres partes e deve ser
  executada depois que todas estiverem definidas.

Restricoes atendidas: simulacao com for; sem bibliotecas financeiras,
sem operador de potencia e sem pow().
"""

# Use o valor calculado pelo grupo. No momento, o valor informado e K = 10.
K = 10


def _i3_numero_finito(valor):
    """Informa se valor e numerico, real e finito, sem usar bibliotecas."""
    return (
        isinstance(valor, (int, float))
        and not isinstance(valor, bool)
        and valor == valor
        and valor != float("inf")
        and valor != float("-inf")
    )


def calcular_parametros_k(k):
    """Calcula a taxa mensal (%) e o prazo (meses) a partir do K."""
    if isinstance(k, bool) or not isinstance(k, int) or k < 0:
        raise ValueError("K deve ser um numero inteiro nao negativo.")

    taxa_mensal = (k % 5) + 1
    prazo_meses = (k % 6) + 6
    return taxa_mensal, prazo_meses


def simular_juros_compostos(capital, taxa_mensal, meses):
    """Gera o historico mensal de juros compostos usando repeticao for."""
    if not _i3_numero_finito(capital) or capital <= 0:
        raise ValueError("O capital deve ser um numero finito maior que zero.")

    if not _i3_numero_finito(taxa_mensal) or taxa_mensal < 0:
        raise ValueError("A taxa deve ser um numero finito nao negativo.")

    if isinstance(meses, bool) or not isinstance(meses, int) or meses <= 0:
        raise ValueError("O prazo deve ser um inteiro positivo.")

    saldo = float(capital)
    historico = []

    for mes in range(1, meses + 1):
        saldo_anterior = saldo
        saldo = saldo * (1 + taxa_mensal / 100)
        juros_mes = saldo - saldo_anterior
        juros_acumulados = saldo - capital

        historico.append({
            "mes": mes,
            "saldo": round(saldo, 2),
            "juros_mes": round(juros_mes, 2),
            "juros_acumulados": round(juros_acumulados, 2)
        })

    return historico


def executar_projecao_k():
    """Executa a opcao 3 usando as funcoes de entrada e formatacao do grupo."""
    print("\nPROJECAO HIPOTETICA COM K")
    modelo = ler_texto("Nome/modelo do smartphone: ")
    capital = ler_float("Preco-base no cartao (R$): ", 0.0, False)

    taxa, meses = calcular_parametros_k(K)
    historico = simular_juros_compostos(capital, taxa, meses)

    print("\nProduto:", modelo)
    print("Capital inicial:", formatar_moeda(capital))
    print("K:", K)
    print("Taxa mensal determinada pelo K:", formatar_percentual(taxa))
    print("Prazo determinado pelo K:", meses, "meses")
    print("\nEvolucao mensal:")
    print(
        f"{'Mes':>5} {'Saldo':>18} "
        f"{'Juros do mes':>18} {'Juros acumulados':>21}"
    )
    print("-" * 68)

    for item in historico:
        print(
            f"{item['mes']:>5} {formatar_moeda(item['saldo']):>18} "
            f"{formatar_moeda(item['juros_mes']):>18} "
            f"{formatar_moeda(item['juros_acumulados']):>21}"
        )

    print("Montante final:", formatar_moeda(historico[-1]["saldo"]))
    print(
        "Juros hipoteticos acumulados:",
        formatar_moeda(historico[-1]["juros_acumulados"])
    )
    print("Esta projecao e academica; nao representa uma oferta real de credito.")


def _i3_esperar_value_error(funcao, *argumentos):
    """Retorna True quando a chamada testada gera ValueError."""
    try:
        funcao(*argumentos)
    except ValueError:
        return True
    return False


def executar_testes_integracao():
    """Executa 12 grupos de testes sobre as tres partes ja integradas."""
    # 01 - O K atual deve produzir taxa de 1% e prazo de 10 meses.
    assert calcular_parametros_k(K) == (1, 10)
    print("Teste 01/12 aprovado: parametros do K atual.")

    # 02 - Verifica outros valores e os limites das formulas.
    assert calcular_parametros_k(0) == (1, 6)
    assert calcular_parametros_k(5) == (1, 11)
    print("Teste 02/12 aprovado: outros valores de K.")

    # 03 - K negativo, decimal ou booleano deve ser rejeitado.
    assert _i3_esperar_value_error(calcular_parametros_k, -1)
    assert _i3_esperar_value_error(calcular_parametros_k, 2.5)
    assert _i3_esperar_value_error(calcular_parametros_k, True)
    print("Teste 03/12 aprovado: validacao do K.")

    # 04 - A simulacao deve gerar exatamente uma linha por mes.
    historico = simular_juros_compostos(1000.00, 1.0, 10)
    assert len(historico) == 10
    assert historico[0]["mes"] == 1 and historico[-1]["mes"] == 10
    print("Teste 04/12 aprovado: quantidade de meses gerados.")

    # 05 - Primeiro mes: R$ 1.000,00 passa a R$ 1.010,00.
    assert historico[0]["saldo"] == 1010.00
    assert historico[0]["juros_mes"] == 10.00
    print("Teste 05/12 aprovado: saldo do primeiro mes.")

    # 06 - Segundo mes: os juros incidem sobre R$ 1.010,00.
    assert historico[1]["saldo"] == 1020.10
    assert historico[1]["juros_mes"] == 10.10
    print("Teste 06/12 aprovado: juros sobre saldo atualizado.")

    # 07 - Terceiro mes e juros acumulados.
    assert historico[2]["saldo"] == 1030.30
    assert historico[2]["juros_mes"] == 10.20
    assert historico[2]["juros_acumulados"] == 30.30
    print("Teste 07/12 aprovado: saldo e juros acumulados no terceiro mes.")

    # 08 - Montante final esperado para 10 meses a 1% ao mes.
    assert historico[-1]["saldo"] == 1104.62
    assert historico[-1]["juros_acumulados"] == 104.62
    print("Teste 08/12 aprovado: montante e juros acumulados finais.")

    # 09 - Taxa zero nao pode alterar o capital.
    sem_juros = simular_juros_compostos(750.00, 0.0, 4)
    assert len(sem_juros) == 4
    assert all(item["saldo"] == 750.00 for item in sem_juros)
    print("Teste 09/12 aprovado: simulacao com taxa zero.")

    # 10 - Entradas invalidas da simulacao devem ser rejeitadas.
    assert _i3_esperar_value_error(simular_juros_compostos, 0, 1, 10)
    assert _i3_esperar_value_error(simular_juros_compostos, 1000, -1, 10)
    assert _i3_esperar_value_error(simular_juros_compostos, 1000, 1, 0)
    assert _i3_esperar_value_error(simular_juros_compostos, float("nan"), 1, 10)
    assert _i3_esperar_value_error(simular_juros_compostos, 1000, float("inf"), 10)
    print("Teste 10/12 aprovado: validacao dos dados da simulacao.")

    # 11 - Integracao com leitura numerica e consulta de taxa bancaria.
    assert converter_valor_numerico("R$ 6.767,50") == 6767.50
    assert obter_media_taxa_banco("Itaú") == 9.91
    print("Teste 11/12 aprovado: leitura monetaria e consulta de taxa.")

    # 12 - Integracao com calculos do Integrante 2 e dados do Integrante 1.
    oferta_sem_juros = OFERTAS_REAIS[0]
    assert calcular_juros_reais(oferta_sem_juros) == 0.00
    assert calcular_juros_percentual(oferta_sem_juros) == 0.00
    assert calcular_parcela_simulada(1200.00, 0.00, 0.0, 12) == 100.00
    assert calcular_parcela_simulada(1200.00, 0.00, 2.0, 12) > 100.00

    simulacao = simular_condicao_plataforma(
        "Amazon", "Itaú", 3000.00, 300.00, 12
    )
    assert simulacao is not None
    assert simulacao["taxa_banco"] == 9.91
    assert round(simulacao["desconto_medio"], 2) == 17.33
    print("Teste 12/12 aprovado: integracao das tres partes.")

    print("\nResultado: 12 de 12 grupos de testes aprovados.")
