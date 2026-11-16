"""Projeto 15 - Comparador de Compras Parceladas.

Versao integrada das tres partes do grupo.

Menu principal:
1. Comparar ofertas reais (inclui cadastro e consulta de ofertas).
2. Simular parcelamento usando taxa de referencia do banco e desconto Pix.
3. Projetar juros compostos a partir do parametro K.
0. Sair.

Padrao unico de oferta:
{
    "codigo_modelo": str,
    "loja": str,
    "produto": str,
    "valor_a_vista": float,
    "entrada": float,
    "num_parcelas": int,
    "valor_parcela": float
}

Restricoes preservadas: sem bibliotecas financeiras, sem operador de potencia ou funcao de potencia pronta.
A simulacao de juros compostos e realizada com laco for.
"""

# =====================================================================
# CONFIGURACOES E DADOS DO PROJETO
# =====================================================================

K = 51  # K atualizado.

PLATAFORMAS = ["Amazon", "Magazine Luiza", "Mercado Livre"]

BANCOS_CARTAO = [
    "Itaú",
    "Nubank",
    "Bradesco",
    "Santander",
    "Caixa Econômica Federal",
]

# Taxas de referencia transcritas do BCB no codigo anterior do grupo.
# Modalidade: Cartao de credito - parcelado - Prefixado (Pessoa Fisica).
# Periodo informado pelo grupo: 09/10/2026 a 16/10/2026.
# A taxa media nao corresponde necessariamente a taxa contratual individual.
PERIODO_TAXAS_BCB = "09/10/2026 a 16/10/2026"
MODALIDADE_TAXAS_BCB = "Cartao de credito - parcelado - Prefixado (Pessoa Fisica)"
FONTE_TAXAS_BCB = (
    "https://www.bcb.gov.br/estatisticas/reporttxjuroshistorico?"
    "InicioPeriodo=2024-01-&codigoModalidade=215101&codigoSegmento=1&"
    "historicotaxajurosdiario_page=1&tipoModalidade=D"
)

AMOSTRAS_TAXAS_MENSAIS = {
    "Itaú": [9.91],
    "Nubank": [9.06],
    "Bradesco": [9.02],
    "Santander": [10.16],
    "Caixa Econômica Federal": [8.62],
}

# Valores provisoriamente mantidos do codigo anterior do grupo.
# Confirmar cada amostra com print/link, data, preco Pix e preco-base da mesma oferta.
AMOSTRAS_DESCONTOS_PIX = {
    "Amazon": [19.0, 9.0, 24.0],
    "Magazine Luiza": [21.0, 15.0, 10.0],
    "Mercado Livre": [22.0, 20.0, 15.0],
}


# =====================================================================
# INTEGRANTE 1 - ENTRADA DE DADOS, VALIDACAO E CADASTRO (PEDRO VITOR
# =====================================================================


def ler_texto(mensagem):
    """Solicita um texto nao vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("O campo nao pode ficar vazio.")


def converter_valor_numerico(texto):
    """Converte valores como 'R$ 1.234,56', '1234,56' ou '1234.56'."""
    if isinstance(texto, (int, float)) and not isinstance(texto, bool):
        valor = float(texto)
        if not _numero_finito(valor):
            raise ValueError("O valor precisa ser finito.")
        return valor

    texto = str(texto).strip().replace("R$", "").replace(" ", "")
    if not texto:
        raise ValueError("Digite um valor numerico.")

    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif "," in texto:
        texto = texto.replace(",", ".")

    valor = float(texto)
    if not _numero_finito(valor):
        raise ValueError("O valor precisa ser finito.")
    return valor


def ler_float(mensagem, minimo=0.0, permitir_igual=True):
    """Le um numero decimal, aceitando virgula e formato monetario brasileiro."""
    while True:
        try:
            valor = converter_valor_numerico(input(mensagem))
        except ValueError:
            print("Entrada invalida. Digite um numero valido.")
            continue

        if permitir_igual and valor >= minimo:
            return valor
        if not permitir_igual and valor > minimo:
            return valor
        comparacao = "maior ou igual" if permitir_igual else "maior"
        print("O valor deve ser", comparacao, "a", minimo)


def ler_inteiro(mensagem, minimo=1, maximo=60):
    """Le um inteiro dentro do intervalo informado."""
    while True:
        texto = input(mensagem).strip()
        try:
            valor = int(texto)
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")
            continue

        if minimo <= valor <= maximo:
            return valor
        print("Digite um inteiro entre", minimo, "e", maximo, ".")


def ler_int_positivo(mensagem):
    """Compatibilidade com o nome usado no primeiro trecho do grupo."""
    return ler_inteiro(mensagem, 1, 1000)


def ler_float_positivo(mensagem, permitir_zero=False):
    """Compatibilidade com o nome usado no primeiro trecho do grupo."""
    return ler_float(mensagem, 0.0, permitir_zero)


def formatar_reais(valor):
    """Formata um numero como moeda brasileira."""
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


def formatar_moeda(valor):
    """Alias para manter compatibilidade com a parte de juros compostos."""
    return formatar_reais(valor)


def formatar_percentual(valor):
    """Formata um percentual com duas casas decimais."""
    return f"{valor:.2f}%".replace(".", ",")


def criar_codigo_modelo(produto):
    """Cria identificador simples para agrupar ofertas do mesmo produto."""
    codigo = ""
    for caractere in produto.lower():
        if caractere.isalnum():
            codigo += caractere
    return codigo


def criar_oferta(loja, produto, valor_a_vista, parcelas, valor_parcela,
                 entrada=0.0, codigo_modelo=None):
    """Cria uma oferta usando o padrao unico compartilhado pelo programa."""
    if codigo_modelo is None:
        codigo_modelo = criar_codigo_modelo(produto)
    return {
        "codigo_modelo": codigo_modelo,
        "loja": loja,
        "produto": produto,
        "valor_a_vista": float(valor_a_vista),
        "entrada": float(entrada),
        "num_parcelas": int(parcelas),
        "valor_parcela": float(valor_parcela),
    }


def validar_oferta(oferta):
    """Valida os campos financeiros de uma oferta cadastrada."""
    campos = ["loja", "produto", "valor_a_vista", "entrada",
              "num_parcelas", "valor_parcela"]
    for campo in campos:
        if campo not in oferta:
            raise ValueError("Campo ausente na oferta: " + campo)

    if not str(oferta["loja"]).strip() or not str(oferta["produto"]).strip():
        raise ValueError("Loja e produto nao podem ficar vazios.")

    vista = oferta["valor_a_vista"]
    entrada = oferta["entrada"]
    parcelas = oferta["num_parcelas"]
    valor_parcela = oferta["valor_parcela"]

    if not _numero_finito(vista) or vista <= 0:
        raise ValueError("O preco a vista deve ser finito e maior que zero.")
    if not _numero_finito(entrada) or entrada < 0 or entrada >= vista:
        raise ValueError("A entrada deve ser finita, nao negativa e menor que o preco a vista.")
    if isinstance(parcelas, bool) or not isinstance(parcelas, int) or parcelas <= 0:
        raise ValueError("O numero de parcelas deve ser um inteiro positivo.")
    if not _numero_finito(valor_parcela) or valor_parcela <= 0:
        raise ValueError("O valor da parcela deve ser finito e maior que zero.")

    total = entrada + parcelas * valor_parcela
    if total + 0.01 < vista:
        raise ValueError("O total a prazo nao pode ser menor que o preco a vista.")
    return True


def cadastrar_oferta(ofertas):
    """Solicita os dados de uma oferta e adiciona a lista compartilhada."""
    print("\nCADASTRO DE OFERTA REAL")
    loja = ler_texto("Nome da loja: ")
    produto = ler_texto("Nome/modelo do produto (inclua memoria/versao): ")
    valor_a_vista = ler_float("Preco a vista/Pix (R$): ", 0.0, False)

    while True:
        entrada = ler_float("Valor da entrada (R$; 0 se nao houver): ", 0.0, True)
        if entrada < valor_a_vista:
            break
        print("A entrada precisa ser menor que o preco a vista.")

    parcelas = ler_int_positivo("Numero de parcelas: ")
    while True:
        valor_parcela = ler_float("Valor de cada parcela (R$): ", 0.0, False)
        total = entrada + parcelas * valor_parcela
        if total + 0.01 >= valor_a_vista:
            break
        minimo = (valor_a_vista - entrada) / parcelas
        print("O total a prazo ficou abaixo do preco a vista.")
        print("Cada parcela deve ser de pelo menos", formatar_reais(minimo))

    oferta = criar_oferta(loja, produto, valor_a_vista, parcelas,
                          valor_parcela, entrada)
    validar_oferta(oferta)
    ofertas.append(oferta)
    print("Oferta cadastrada com sucesso.")


# =====================================================================
# DADOS REAIS FORNECIDOS NO CODIGO ENVIADO PELO GRUPO
# =====================================================================

OFERTAS_IPHONE = [
    criar_oferta("Amazon", "iPhone 17 Pro Max 256 GB", 9998.99, 12, 883.25,
                 codigo_modelo="iphone17promax256"),
    criar_oferta("Magazine Luiza", "iPhone 17 Pro Max 256 GB", 11494.05, 10, 1209.90,
                 codigo_modelo="iphone17promax256"),
    criar_oferta("Mercado Livre", "iPhone 17 Pro Max 512 GB", 10799.00, 10, 1199.90,
                 codigo_modelo="iphone17promax512"),
]

OFERTAS_POCO_C85 = [
    criar_oferta("Amazon", "POCO C85 256 GB", 1182.09, 12, 108.25,
                 codigo_modelo="pococ85256"),
    criar_oferta("Mercado Livre", "POCO C85 256 GB", 1278.99, 10, 139.56,
                 codigo_modelo="pococ85256"),
]

OFERTAS_Z_FLIP8 = [
    criar_oferta("Magazine Luiza 10x", "Galaxy Z Flip 8 256 GB", 7739.10, 10, 859.90,
                 codigo_modelo="galaxyzflip8256"),
    criar_oferta("Magazine Luiza 21x", "Galaxy Z Flip 8 256 GB", 7739.10, 21, 409.48,
                 codigo_modelo="galaxyzflip8256"),
    criar_oferta("Mercado Livre", "Galaxy Z Flip 8 512 GB", 6699.00, 12, 643.89,
                 codigo_modelo="galaxyzflip8512"),
]

# Uma unica lista alimenta cadastro, consulta e comparacao.
OFERTAS_REAIS = OFERTAS_IPHONE + OFERTAS_POCO_C85 + OFERTAS_Z_FLIP8


# =====================================================================
# INTEGRANTE 2 - CALCULOS FINANCEIROS E COMPARACAO DE OFERTAS (EDUARDO SOARES)
# =====================================================================


def calcular_total_prazo(oferta):
    """Calcula entrada + quantidade de parcelas * valor da parcela."""
    validar_oferta(oferta)
    total = oferta["entrada"] + oferta["num_parcelas"] * oferta["valor_parcela"]
    return round(total, 2)


def calcular_juros(oferta):
    """Retorna uma tupla com juros em reais e juros percentuais sobre o preco a vista."""
    total = calcular_total_prazo(oferta)
    a_vista = oferta["valor_a_vista"]
    juros_reais = round(total - a_vista, 2)
    juros_percentual = round((juros_reais / a_vista) * 100, 2)
    return juros_reais, juros_percentual


def calcular_juros_reais(oferta):
    """Retorna o acrescimo em reais sobre o preco a vista."""
    return calcular_juros(oferta)[0]


def calcular_juros_percentual(oferta):
    """Retorna o acrescimo percentual sobre o preco a vista."""
    return calcular_juros(oferta)[1]


def achar_mais_barata(ofertas):
    """Retorna todas as ofertas empatadas com o menor total a prazo."""
    if not ofertas:
        return []
    menor = calcular_total_prazo(ofertas[0])
    for oferta in ofertas[1:]:
        total = calcular_total_prazo(oferta)
        if total < menor:
            menor = total
    return [oferta for oferta in ofertas
            if abs(calcular_total_prazo(oferta) - menor) <= 0.01]


def achar_mais_cara(ofertas):
    """Retorna todas as ofertas empatadas com o maior total a prazo."""
    if not ofertas:
        return []
    maior = calcular_total_prazo(ofertas[0])
    for oferta in ofertas[1:]:
        total = calcular_total_prazo(oferta)
        if total > maior:
            maior = total
    return [oferta for oferta in ofertas
            if abs(calcular_total_prazo(oferta) - maior) <= 0.01]


def _nomes(ofertas):
    """Retorna os nomes das lojas de uma lista de ofertas."""
    nomes = []
    for oferta in ofertas:
        nomes.append(oferta["loja"])
    return ", ".join(nomes)


def exibir_tabela(ofertas):
    """Exibe a comparacao de parcelas, custo total e juros."""
    if not ofertas:
        print("Nenhuma oferta disponivel para comparar.")
        return

    cabecalho = (
        f"{'Loja':<22}{'A vista':>14}{'Entrada':>13}"
        f"{'Parcelamento':>23}{'Total a prazo':>17}{'Juros R$':>14}{'Juros %':>10}"
    )
    linha = "-" * len(cabecalho)
    print(linha)
    print(cabecalho)
    print(linha)

    for oferta in ofertas:
        total = calcular_total_prazo(oferta)
        juros_reais, juros_percentual = calcular_juros(oferta)
        parcelamento = (
            str(oferta["num_parcelas"]) + "x "
            + formatar_reais(oferta["valor_parcela"])
        )
        print(
            f"{oferta['loja']:<22}"
            f"{formatar_reais(oferta['valor_a_vista']):>14}"
            f"{formatar_reais(oferta['entrada']):>13}"
            f"{parcelamento:>23}"
            f"{formatar_reais(total):>17}"
            f"{formatar_reais(juros_reais):>14}"
            f"{juros_percentual:>9.2f}%"
        )
    print(linha)


def exibir_resumo(ofertas):
    """Identifica a oferta de menor e maior custo total, incluindo empates."""
    if not ofertas:
        print("Nao ha ofertas para gerar o resumo.")
        return

    baratas = achar_mais_barata(ofertas)
    caras = achar_mais_cara(ofertas)
    total_barato = calcular_total_prazo(baratas[0])
    total_caro = calcular_total_prazo(caras[0])

    print("Menor custo total:", _nomes(baratas), "-", formatar_reais(total_barato),
          "[EMPATE]" if len(baratas) > 1 else "")
    print("Maior custo total:", _nomes(caras), "-", formatar_reais(total_caro),
          "[EMPATE]" if len(caras) > 1 else "")


def calcular_media(valores):
    """Calcula a media aritmetica de uma lista de valores."""
    if not valores:
        return None
    soma = 0.0
    for valor in valores:
        soma += valor
    return soma / len(valores)


def obter_media_taxa_banco(banco):
    """Retorna a taxa mensal de referencia cadastrada para o banco."""
    if banco not in AMOSTRAS_TAXAS_MENSAIS:
        return None
    return calcular_media(AMOSTRAS_TAXAS_MENSAIS[banco])


def obter_media_desconto(plataforma):
    """Retorna o desconto Pix medio cadastrado para a plataforma."""
    if plataforma not in AMOSTRAS_DESCONTOS_PIX:
        return None
    return calcular_media(AMOSTRAS_DESCONTOS_PIX[plataforma])


def fator_presente_parcelas(taxa_percentual, quantidade_parcelas):
    """Soma fatores de valor presente usando for, sem potencia pronta."""
    if taxa_percentual < 0 or quantidade_parcelas <= 0:
        raise ValueError("Taxa ou quantidade de parcelas invalida.")
    taxa_decimal = taxa_percentual / 100
    fator = 1.0
    soma = 0.0
    for mes in range(1, quantidade_parcelas + 1):
        fator = fator / (1 + taxa_decimal)
        soma += fator
    return soma


def calcular_parcela_simulada(preco_base, entrada, taxa_percentual, parcelas):
    """Calcula parcela fixa pelo modelo Price, com primeira parcela em um mes."""
    if not _numero_finito(preco_base) or preco_base <= 0:
        raise ValueError("Preco-base deve ser finito e maior que zero.")
    if not _numero_finito(entrada) or entrada < 0 or entrada >= preco_base:
        raise ValueError("Entrada invalida.")
    if not _numero_finito(taxa_percentual) or taxa_percentual < 0:
        raise ValueError("Taxa invalida.")
    if isinstance(parcelas, bool) or not isinstance(parcelas, int) or parcelas <= 0:
        raise ValueError("Quantidade de parcelas invalida.")

    capital_financiado = preco_base - entrada
    if taxa_percentual == 0:
        return round(capital_financiado / parcelas, 2)
    fator = fator_presente_parcelas(taxa_percentual, parcelas)
    return round(capital_financiado / fator, 2)


def calcular_preco_pix(preco_base, desconto_percentual):
    """Aplica o desconto medio Pix ao preco-base informado."""
    if not _numero_finito(preco_base) or preco_base <= 0:
        raise ValueError("Preco-base invalido.")
    if not _numero_finito(desconto_percentual) or not 0 <= desconto_percentual < 100:
        raise ValueError("Desconto deve estar entre 0% e menos de 100%.")
    return round(preco_base * (1 - desconto_percentual / 100), 2)


def simular_condicao_plataforma(plataforma, banco, preco_base, entrada, parcelas):
    """Calcula parcela, total a prazo e estimativa Pix para banco e plataforma."""
    taxa_banco = obter_media_taxa_banco(banco)
    desconto_medio = obter_media_desconto(plataforma)
    if taxa_banco is None or desconto_medio is None:
        return None

    parcela = calcular_parcela_simulada(preco_base, entrada, taxa_banco, parcelas)
    total = round(entrada + parcela * parcelas, 2)
    preco_pix = calcular_preco_pix(preco_base, desconto_medio)
    return {
        "plataforma": plataforma,
        "banco": banco,
        "taxa_banco": taxa_banco,
        "desconto_medio": desconto_medio,
        "preco_pix": preco_pix,
        "valor_parcela": parcela,
        "parcelas": parcelas,
        "total_parcelado": total,
        "acrescimo_sobre_base": round(total - preco_base, 2),
        "diferenca_vs_pix": round(total - preco_pix, 2),
    }


def simular_faixa_parcelas(plataforma, banco, preco_base, entrada,
                            limite_parcelas, limite_mensal=0.0):
    """Gera resultados de 1 ate o limite de parcelas para a combinacao escolhida."""
    resultados = []
    for quantidade in range(1, limite_parcelas + 1):
        simulacao = simular_condicao_plataforma(
            plataforma, banco, preco_base, entrada, quantidade
        )
        if simulacao is None:
            return []
        registro = {
            "parcelas": quantidade,
            "parcela": simulacao["valor_parcela"],
            "total": simulacao["total_parcelado"],
            "preco_pix": simulacao["preco_pix"],
            "diferenca_pix": simulacao["diferenca_vs_pix"],
            "cabe_orcamento": limite_mensal <= 0 or simulacao["valor_parcela"] <= limite_mensal,
        }
        resultados.append(registro)
    return resultados


def selecionar_banco_cartao():
    """Mostra os emissores disponiveis e retorna o banco escolhido."""
    print("\nSELECIONE O BANCO/EMISSOR DO CARTAO")
    for indice, banco in enumerate(BANCOS_CARTAO, start=1):
        print(str(indice) + " - " + banco)
    escolha = ler_inteiro("Banco do cartao: ", 1, len(BANCOS_CARTAO))
    return BANCOS_CARTAO[escolha - 1]


def selecionar_plataforma():
    """Mostra as plataformas disponiveis e retorna a escolhida."""
    print("\nSELECIONE A PLATAFORMA DE COMPRA")
    for indice, plataforma in enumerate(PLATAFORMAS, start=1):
        print(str(indice) + " - " + plataforma)
    escolha = ler_inteiro("Plataforma: ", 1, len(PLATAFORMAS))
    return PLATAFORMAS[escolha - 1]


# =====================================================================
# INTEGRANTE 3 - JUROS COMPOSTOS, TESTES E INTEGRACAO(JOSUÉ GABRIEL)
# =====================================================================


def _numero_finito(valor):
    """Verifica se o argumento e numero finito, sem importar bibliotecas."""
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
        raise ValueError("K deve ser um inteiro nao negativo.")
    taxa_mensal = (k % 5) + 1
    prazo_meses = (k % 6) + 6
    return taxa_mensal, prazo_meses


def simular_juros_compostos(capital, taxa_mensal, meses):
    """Gera historico mensal de juros compostos com for, sem operador ou funcao de potencia pronta."""
    if not _numero_finito(capital) or capital <= 0:
        raise ValueError("O capital deve ser finito e maior que zero.")
    if not _numero_finito(taxa_mensal) or taxa_mensal < 0:
        raise ValueError("A taxa deve ser finita e nao negativa.")
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
            "juros_acumulados": round(juros_acumulados, 2),
        })
    return historico


def executar_projecao_k():
    """Executa a opcao 3 usando as funcoes de entrada compartilhadas."""
    print("\nPROJECAO HIPOTETICA COM K")
    modelo = ler_texto("Nome/modelo do smartphone: ")
    capital = ler_float("Preco-base no cartao (R$): ", 0.0, False)
    taxa, meses = calcular_parametros_k(K)
    historico = simular_juros_compostos(capital, taxa, meses)

    print("\nProduto:", modelo)
    print("Capital inicial:", formatar_reais(capital))
    print("K:", K)
    print("Taxa mensal determinada pelo K:", formatar_percentual(taxa))
    print("Prazo determinado pelo K:", meses, "meses")
    print("\nEvolucao mensal:")
    print(f"{'Mes':>5} {'Saldo':>18} {'Juros do mes':>18} {'Juros acumulados':>21}")
    print("-" * 68)
    for item in historico:
        print(
            f"{item['mes']:>5} {formatar_reais(item['saldo']):>18} "
            f"{formatar_reais(item['juros_mes']):>18} "
            f"{formatar_reais(item['juros_acumulados']):>21}"
        )
    print("Montante final:", formatar_reais(historico[-1]["saldo"]))
    print("Juros hipoteticos acumulados:", formatar_reais(historico[-1]["juros_acumulados"]))
    print("Esta projecao e academica; nao representa uma oferta real de credito.")


# =====================================================================
# OPCOES DO MENU PRINCIPAL (IA-REVISADO PELO GRUPO)
# =====================================================================


def listar_codigos_modelos(ofertas):
    """Retorna os codigos de modelos sem repeticoes, preservando a ordem."""
    codigos = []
    for oferta in ofertas:
        codigo = oferta["codigo_modelo"]
        if codigo not in codigos:
            codigos.append(codigo)
    return codigos


def buscar_ofertas_por_modelo(ofertas, codigo_modelo):
    """Seleciona as ofertas do mesmo modelo/versao cadastrada."""
    encontradas = []
    for oferta in ofertas:
        if oferta["codigo_modelo"] == codigo_modelo:
            encontradas.append(oferta)
    return encontradas


def exibir_ofertas_cadastradas(ofertas):
    """Lista todas as ofertas cadastradas."""
    if not ofertas:
        print("Nenhuma oferta cadastrada ainda.")
        return
    for indice, oferta in enumerate(ofertas, start=1):
        total = calcular_total_prazo(oferta)
        print(
            str(indice) + ". " + oferta["loja"] + " - " + oferta["produto"]
            + " | A vista: " + formatar_reais(oferta["valor_a_vista"])
            + " | Entrada: " + formatar_reais(oferta["entrada"])
            + " + " + str(oferta["num_parcelas"]) + " x "
            + formatar_reais(oferta["valor_parcela"])
            + " | Total: " + formatar_reais(total)
        )


def executar_comparacao_real():
    """Executa a opcao 1: compara ofertas reais e permite cadastro/consulta."""
    while True:
        print("\n--- OFERTAS REAIS ---")
        print("1. Comparar ofertas por produto")
        print("2. Cadastrar nova oferta")
        print("3. Consultar todas as ofertas")
        print("0. Voltar ao menu principal")
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            codigos = listar_codigos_modelos(OFERTAS_REAIS)
            if not codigos:
                print("Nenhuma oferta cadastrada.")
                continue
            print("\nPRODUTOS DISPONIVEIS")
            for indice, codigo in enumerate(codigos, start=1):
                grupo = buscar_ofertas_por_modelo(OFERTAS_REAIS, codigo)
                print(str(indice) + " - " + grupo[0]["produto"])
            escolha = ler_inteiro("Escolha o produto: ", 1, len(codigos))
            grupo = buscar_ofertas_por_modelo(OFERTAS_REAIS, codigos[escolha - 1])
            print("\nCOMPARACAO DE OFERTAS")
            exibir_tabela(grupo)
            exibir_resumo(grupo)
            if len(grupo) == 1:
                print("Observacao: existe apenas uma oferta cadastrada para este modelo.")
        elif opcao == "2":
            cadastrar_oferta(OFERTAS_REAIS)
        elif opcao == "3":
            exibir_ofertas_cadastradas(OFERTAS_REAIS)
        elif opcao == "0":
            break
        else:
            print("Opcao invalida. Digite 1, 2, 3 ou 0.")


def executar_simulacao_avulsa():
    """Executa a opcao 2: compara prazos usando banco e plataforma."""
    print("\nSIMULACAO DE PARCELAMENTO - BANCO + PLATAFORMA")
    modelo = ler_texto("Nome/modelo do smartphone: ")
    preco_base = ler_float("Preco-base normal no cartao (R$): ", 0.0, False)

    while True:
        entrada = ler_float("Entrada (R$; digite 0 se nao houver): ", 0.0, True)
        if entrada < preco_base:
            break
        print("A entrada deve ser menor que o preco-base.")

    banco = selecionar_banco_cartao()
    plataforma = selecionar_plataforma()
    limite_parcelas = ler_inteiro("Quantidade maxima de parcelas (1 a 48): ", 1, 48)
    limite_mensal = ler_float("Limite mensal (R$; 0 para nao filtrar): ", 0.0, True)

    taxa_banco = obter_media_taxa_banco(banco)
    desconto_medio = obter_media_desconto(plataforma)
    preco_pix = calcular_preco_pix(preco_base, desconto_medio)
    resultados = simular_faixa_parcelas(
        plataforma, banco, preco_base, entrada, limite_parcelas, limite_mensal
    )

    print("\nProduto:", modelo)
    print("Banco/emissor:", banco)
    print("Taxa mensal de referencia:", formatar_percentual(taxa_banco))
    print("Periodo da taxa BCB:", PERIODO_TAXAS_BCB)
    print("Plataforma:", plataforma)
    print("Desconto Pix medio cadastrado:", formatar_percentual(desconto_medio))
    print("Preco estimado no Pix:", formatar_reais(preco_pix))
    print("\nCOMPARACAO DOS PRAZOS")
    print(f"{'Parcelas':>9} {'Valor mensal':>18} {'Total a prazo':>20} {'Diferenca vs Pix':>19}")
    print("-" * 75)
    for registro in resultados:
        print(
            f"{registro['parcelas']:>9} "
            f"{formatar_reais(registro['parcela']):>18} "
            f"{formatar_reais(registro['total']):>20} "
            f"{formatar_reais(registro['diferenca_pix']):>19}"
        )

    menor_total = resultados[0]
    menor_parcela = resultados[0]
    primeiro_compativel = None
    for registro in resultados:
        if registro["total"] < menor_total["total"]:
            menor_total = registro
        if registro["parcela"] < menor_parcela["parcela"]:
            menor_parcela = registro
        if primeiro_compativel is None and registro["cabe_orcamento"]:
            primeiro_compativel = registro

    print("\nMENOR CUSTO TOTAL:", menor_total["parcelas"], "parcelas de",
          formatar_reais(menor_total["parcela"]), "- total",
          formatar_reais(menor_total["total"]))
    print("MENOR PARCELA MENSAL:", menor_parcela["parcelas"], "parcelas de",
          formatar_reais(menor_parcela["parcela"]), "- total",
          formatar_reais(menor_parcela["total"]))

    if limite_mensal > 0:
        if primeiro_compativel is None:
            print("Nenhum prazo analisado cabe no limite mensal informado.")
        else:
            print("Primeiro prazo dentro do limite:", primeiro_compativel["parcelas"],
                  "parcelas de", formatar_reais(primeiro_compativel["parcela"]))

    print("\nObservacoes metodologicas:")
    print("- A taxa do banco e uma referencia media do BCB, nao uma taxa garantida.")
    print("- A condicao real depende do contrato e do Custo Efetivo Total (CET).")
    print("- O desconto Pix e uma media das amostras cadastradas pelo grupo.")
    print("- A menor parcela mensal nao significa o menor custo total.")

#[IA]
def abrir_interface_grafica():
    """Executa a opcao 4: abre a interface grafica (tkinter)."""
    import sys
    try:
        from interface_tkinter import abrir_interface
    except ImportError:
        print("Nao foi possivel abrir a interface grafica (tkinter ou interface_tkinter.py ausente).")
        return
    abrir_interface(sys.modules[__name__])

def exibir_menu():
    """Mostra o menu principal com as tres funcionalidades do projeto."""
    print("\n" + "=" * 66)
    print("COMPARADOR DE OFERTAS DE SMARTPHONES - PROJETO 15")
    print("=" * 66)
    print("1 - Comparar ofertas reais cadastradas")
    print("2 - Simular parcelamento (banco + plataforma)")
    print("3 - Fazer projecao hipotetica com K")
    print("4 - Abrir interface grafica")
    print("0 - Sair")
    print("=" * 66)


def main():
    """Controla o menu principal ate o usuario escolher sair."""
    while True:
        exibir_menu()
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            executar_comparacao_real()
        elif opcao == "2":
            executar_simulacao_avulsa()
        elif opcao == "3":
            executar_projecao_k()
        elif opcao == "4":
            abrir_interface_grafica()
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opcao invalida. Digite 1, 2, 3 ou 0.")


# =====================================================================
# TESTES DE INTEGRACAO - 12 GRUPOS (TESTES DE VALIDAÇÃO EM GRUPO)
# =====================================================================


def _esperar_value_error(funcao, *argumentos):
    """Retorna True quando a funcao testada rejeita os argumentos."""
    try:
        funcao(*argumentos)
    except ValueError:
        return True
    return False


def aproximado(a, b, tolerancia=0.005):
    """Compara numeros considerando uma pequena tolerancia de arredondamento."""
    return abs(a - b) <= tolerancia


def executar_testes_integracao():
    """Executa 12 grupos de testes sobre entrada, calculos e simulacao."""
    # 01 - K atual.
    assert calcular_parametros_k(K) == ((K % 5) + 1, (K % 6) + 6)
    print("Teste 01/12 aprovado: parametros do K atual.")

    # 02 - Outros valores de K.
    assert calcular_parametros_k(0) == (1, 6)
    assert calcular_parametros_k(5) == (1, 11)
    print("Teste 02/12 aprovado: outros valores de K.")

    # 03 - Validacao do K.
    assert _esperar_value_error(calcular_parametros_k, -1)
    assert _esperar_value_error(calcular_parametros_k, 2.5)
    assert _esperar_value_error(calcular_parametros_k, True)
    print("Teste 03/12 aprovado: validacao do K.")

    # 04 - Quantidade e identificacao dos meses.
    historico = simular_juros_compostos(1000.00, 1.0, 10)
    assert len(historico) == 10
    assert historico[0]["mes"] == 1 and historico[-1]["mes"] == 10
    print("Teste 04/12 aprovado: quantidade de meses gerados.")

    # 05 - Primeiro mes.
    assert historico[0]["saldo"] == 1010.00
    assert historico[0]["juros_mes"] == 10.00
    print("Teste 05/12 aprovado: saldo do primeiro mes.")

    # 06 - Segundo mes.
    assert historico[1]["saldo"] == 1020.10
    assert historico[1]["juros_mes"] == 10.10
    print("Teste 06/12 aprovado: juros sobre o saldo atualizado.")

    # 07 - Terceiro mes e juros acumulados.
    assert historico[2]["saldo"] == 1030.30
    assert historico[2]["juros_mes"] == 10.20
    assert historico[2]["juros_acumulados"] == 30.30
    print("Teste 07/12 aprovado: terceiro mes e juros acumulados.")

    # 08 - Montante final.
    assert historico[-1]["saldo"] == 1104.62
    assert historico[-1]["juros_acumulados"] == 104.62
    print("Teste 08/12 aprovado: montante final em dez meses.")

    # 09 - Taxa zero.
    sem_juros = simular_juros_compostos(750.00, 0.0, 4)
    assert len(sem_juros) == 4
    assert all(item["saldo"] == 750.00 for item in sem_juros)
    print("Teste 09/12 aprovado: simulacao com taxa zero.")

    # 10 - Valores invalidos da simulacao.
    assert _esperar_value_error(simular_juros_compostos, 0, 1, 10)
    assert _esperar_value_error(simular_juros_compostos, 1000, -1, 10)
    assert _esperar_value_error(simular_juros_compostos, 1000, 1, 0)
    assert _esperar_value_error(simular_juros_compostos, float("nan"), 1, 10)
    assert _esperar_value_error(simular_juros_compostos, 1000, float("inf"), 10)
    print("Teste 10/12 aprovado: validacao dos dados da simulacao.")

    # 11 - Integracao de cadastro e comparacao (schema unico).
    oferta = OFERTAS_IPHONE[0]
    assert oferta["valor_a_vista"] == 9998.99
    assert oferta["num_parcelas"] == 12
    assert calcular_total_prazo(oferta) == 10599.00
    assert calcular_juros(oferta)[0] == 600.01
    assert achar_mais_barata(OFERTAS_IPHONE) == [OFERTAS_IPHONE[0]]
    assert achar_mais_cara(OFERTAS_IPHONE) == [OFERTAS_IPHONE[1]]
    assert achar_mais_barata([]) == [] and achar_mais_cara([]) == []
    assert converter_valor_numerico("R$ 6.767,50") == 6767.50
    print("Teste 11/12 aprovado: schema unico, leitura e comparacao de ofertas.")

    # 12 - Integracao dos calculos financeiros com bancos e plataformas.
    assert obter_media_taxa_banco("Itaú") == 9.91
    assert aproximado(obter_media_desconto("Amazon"), 17.3333333333)
    assert calcular_parcela_simulada(1200.00, 0.00, 0.0, 12) == 100.00
    assert calcular_parcela_simulada(1200.00, 0.00, 2.0, 12) > 100.00
    simulacao = simular_condicao_plataforma("Amazon", "Itaú", 3000.00, 300.00, 12)
    assert simulacao is not None
    assert simulacao["taxa_banco"] == 9.91
    assert aproximado(simulacao["desconto_medio"], 17.3333333333)
    assert len(simular_faixa_parcelas("Amazon", "Itaú", 3000.00, 300.00, 12)) == 12
    print("Teste 12/12 aprovado: integracao de juros, banco e plataforma.")

    print("\nResultado: 12 de 12 grupos de testes aprovados.")


def rodar_testes():
    """Mantem o nome de funcao usado no trecho do Integrante 2."""
    executar_testes_integracao()


if __name__ == "__main__":
    # Os testes rodam antes do menu para detectar erros de integracao.
    executar_testes_integracao()
    main()
