"""
PROJETO 15 - COMPARADOR DE OFERTAS E SIMULADOR DE PARCELAMENTO
Disciplina: Programacao I - Python
Grupo: [PREENCHER]
Integrantes: [PREENCHER]
K do grupo: 10 (confirmar calculo com as matriculas e com o professor)

OBJETIVO DO PRE-CODIGO
1. Comparar ofertas reais previamente cadastradas (opcao 1).
2. Simular um novo smartphone usando medias calculadas a partir de ofertas
   pesquisadas em cada plataforma (opcao 2).
3. Fazer a simulacao academica de juros compostos definida pelo K (opcao 3).

RESTRICOES ADOTADAS NESTE PRE-CODIGO
- Nenhum import.
- Nenhuma biblioteca financeira.
- Nenhum operador **.
- Nenhuma funcao pow().
- Juros compostos e fator de valor presente calculados com lacos for.

IMPORTANTE SOBRE A OPCAO 1
A leitura automatica de planilha ainda nao foi implementada, pois o grupo
precisa confirmar com o professor se ela sera permitida. Por enquanto, os
registros reais ficam na lista OFERTAS_REAIS. Se a planilha for autorizada,
a funcao carregar_ofertas_reais() sera o ponto de integracao.

IMPORTANTE SOBRE A OPCAO 2
As listas AMOSTRAS_TAXAS e AMOSTRAS_DESCONTOS_PIX estao vazias de proposito.
O grupo deve preencher cada lista com percentuais obtidos em pesquisas reais.
Nao use taxas inventadas como se fossem taxas oficiais das plataformas.

# [IA] Este pre-codigo foi estruturado com apoio de IA. O grupo deve revisar,
# testar, compreender e adaptar todas as funcoes antes da entrega.
"""
import csv

K = 10

PLATAFORMAS = ["Amazon", "Magazine Luiza", "Mercado Livre"]

# =====================================================================
# 1. BASE DE OFERTAS REAIS (OPCAO 1)
# =====================================================================

# Cada registro representa uma oferta coletada manualmente nas capturas.
# codigo_modelo agrupa apenas aparelhos/configuracoes considerados equivalentes.
# Revise cores, memoria, versao 4G/5G e vendedor antes de comparar.
# None significa que o dado nao foi confirmado na captura.

OFERTAS_REAIS = [
    {
        "codigo_modelo": "samsung_s26_256_combo",
        "marca": "Samsung",
        "modelo": "Galaxy S26 256GB + Buds Core",
        "cor": "Nao informada",
        "plataforma": "Magazine Luiza",
        "vendedor": "Nao confirmado na transcricao",
        "preco_a_vista": 4843.80,
        "preco_base_cartao": 5382.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 538.20,
        "total_anunciado": 5382.00,
        "condicao": "Sem juros anunciado",
        "observacao": "Combo com Galaxy Buds Core; nao e apenas o celular."
    },
    {
        "codigo_modelo": "samsung_s26_ultra_256",
        "marca": "Samsung",
        "modelo": "Galaxy S26 Ultra 256GB",
        "cor": "Nao informada",
        "plataforma": "Mercado Livre",
        "vendedor": "Nao confirmado na transcricao",
        "preco_a_vista": 6578.53,
        "preco_base_cartao": 7309.48,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 730.95,
        "total_anunciado": 7309.48,
        "condicao": "Sem juros anunciado",
        "observacao": "10 x R$ 730,95 = R$ 7.309,50; anuncio mostra R$ 7.309,48. Diferenca de R$ 0,02."
    },
    {
        "codigo_modelo": "samsung_z_flip8_512",
        "marca": "Samsung",
        "modelo": "Galaxy Z Flip 8 512GB",
        "cor": "Nao informada",
        "plataforma": "Mercado Livre",
        "vendedor": "Nao confirmado na transcricao",
        "preco_a_vista": None,
        "preco_base_cartao": None,
        "base_confirmada": False,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 643.89,
        "total_anunciado": None,
        "condicao": "Nao esclarecida",
        "observacao": "A captura mostra R$ 6.699,00 e 12 x R$ 643,89, mas a modalidade do preco exibido nao foi confirmada."
    },
    {
        "codigo_modelo": "samsung_z_flip8_256",
        "marca": "Samsung",
        "modelo": "Galaxy Z Flip 8 256GB",
        "cor": "Laranja? Confirmar",
        "plataforma": "Magazine Luiza",
        "vendedor": "Nao confirmado na transcricao",
        "preco_a_vista": 7739.10,
        "preco_base_cartao": 8599.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 859.90,
        "total_anunciado": 8599.00,
        "condicao": "Sem juros anunciado",
        "observacao": "A captura tambem apresenta plano alternativo de 21 parcelas."
    },
    {
        "codigo_modelo": "samsung_z_flip8_256",
        "marca": "Samsung",
        "modelo": "Galaxy Z Flip 8 256GB",
        "cor": "Laranja? Confirmar",
        "plataforma": "Magazine Luiza",
        "vendedor": "Nao confirmado na transcricao",
        "preco_a_vista": 7739.10,
        "preco_base_cartao": 8599.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 21,
        "valor_parcela": 409.48,
        "total_anunciado": None,
        "condicao": "Sem juros anunciado",
        "observacao": "21 x R$ 409,48 = R$ 8.599,08; diferenca de R$ 0,08 em relacao ao preco-base informado."
    },
    {
        "codigo_modelo": "iphone_17_pro_max_256",
        "marca": "Apple",
        "modelo": "iPhone 17 Pro Max 256GB",
        "cor": "Azul",
        "plataforma": "Amazon",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": 9998.99,
        "preco_base_cartao": 10599.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 883.25,
        "total_anunciado": 10599.00,
        "condicao": "Sem juros anunciado",
        "observacao": "A captura informa 12 x R$ 883,25 e menciona desconto a vista."
    },
    {
        "codigo_modelo": "iphone_17_pro_max_256",
        "marca": "Apple",
        "modelo": "iPhone 17 Pro Max 256GB",
        "cor": "Laranja",
        "plataforma": "Magazine Luiza",
        "vendedor": "iPlace",
        "preco_a_vista": 11494.05,
        "preco_base_cartao": 12099.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 1209.90,
        "total_anunciado": 12099.00,
        "condicao": "Sem juros anunciado",
        "observacao": "Mesma capacidade, mas cor diferente da oferta Amazon. Confirmar se o grupo aceita comparar cores distintas."
    },
    {
        "codigo_modelo": "iphone_17_pro_max_512",
        "marca": "Apple",
        "modelo": "iPhone 17 Pro Max 512GB",
        "cor": "Azul",
        "plataforma": "Mercado Livre",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": 10799.00,
        "preco_base_cartao": 11999.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 1199.90,
        "total_anunciado": 11999.00,
        "condicao": "Sem juros anunciado",
        "observacao": "Configuracao de 512GB; nao comparar como identica a versao de 256GB."
    },
    {
        "codigo_modelo": "poco_x8_pro_256_8gb",
        "marca": "Xiaomi",
        "modelo": "POCO X8 Pro 256GB 8GB RAM",
        "cor": "Nao informada",
        "plataforma": "Amazon",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": 2474.80,
        "preco_base_cartao": 2690.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 224.24,
        "total_anunciado": 2690.00,
        "condicao": "Sem juros anunciado",
        "observacao": "12 x R$ 224,24 = R$ 2.690,88; a captura mostra total de R$ 2.690,00. Conferir arredondamento/anuncio."
    },
    {
        "codigo_modelo": "redmi_note15_pro_512_8gb",
        "marca": "Xiaomi",
        "modelo": "Redmi Note 15 Pro 512GB 8GB RAM",
        "cor": "Nao informada",
        "plataforma": "Amazon",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": 2038.40,
        "preco_base_cartao": 2240.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 186.74,
        "total_anunciado": 2240.00,
        "condicao": "Sem juros anunciado",
        "observacao": "12 x R$ 186,74 = R$ 2.240,88; a captura mostra R$ 2.240,00."
    },
    {
        "codigo_modelo": "poco_c85_256_8gb_amazon",
        "marca": "Xiaomi",
        "modelo": "POCO C85 256GB 8GB RAM",
        "cor": "Nao informada",
        "plataforma": "Amazon",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": 1182.09,
        "preco_base_cartao": 1299.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 108.25,
        "total_anunciado": 1299.00,
        "condicao": "Sem juros anunciado",
        "observacao": "Total calculado das parcelas confere com o total anunciado."
    },
    {
        "codigo_modelo": "redmi_note15_256_8gb",
        "marca": "Xiaomi",
        "modelo": "Redmi Note 15 256GB 8GB RAM",
        "cor": "Nao informada",
        "plataforma": "Amazon",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": 1534.25,
        "preco_base_cartao": 1615.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 134.62,
        "total_anunciado": 1615.00,
        "condicao": "Sem juros anunciado",
        "observacao": "12 x R$ 134,62 = R$ 1.615,44; a captura mostra R$ 1.615,00."
    },
    {
        "codigo_modelo": "redmi_15c_256_8gb",
        "marca": "Xiaomi",
        "modelo": "Redmi 15C 256GB 8GB RAM",
        "cor": "Nao informada",
        "plataforma": "Magazine Luiza",
        "vendedor": "Atacado Import",
        "preco_a_vista": 1274.15,
        "preco_base_cartao": 1499.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 149.90,
        "total_anunciado": 1499.00,
        "condicao": "Sem juros anunciado",
        "observacao": "Vendido por Atacado Import e entregue pelo Magazine Luiza."
    },
    {
        "codigo_modelo": "redmi_note15_pro_5g_256_8gb",
        "marca": "Xiaomi",
        "modelo": "Redmi Note 15 Pro 5G 256GB 8GB RAM",
        "cor": "Nao informada",
        "plataforma": "Mercado Livre",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": None,
        "preco_base_cartao": 2625.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 262.50,
        "total_anunciado": 2625.00,
        "condicao": "Sem juros anunciado",
        "observacao": "A captura informa 10 x R$ 262,50 sem juros; preco a vista separado nao confirmado."
    },
    {
        "codigo_modelo": "poco_c85_4g_256_8gb_ml",
        "marca": "Xiaomi",
        "modelo": "POCO C85 4G 256GB 8GB RAM",
        "cor": "Nao informada",
        "plataforma": "Mercado Livre",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": None,
        "preco_base_cartao": None,
        "base_confirmada": False,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 139.56,
        "total_anunciado": 1395.55,
        "condicao": "Referencia do preco precisa de confirmacao",
        "observacao": "A tela separa menor preco de R$ 1.278,99 do plano de 10 x R$ 139,56; confirmar se e a mesma oferta/vendedor."
    },
    {
        "codigo_modelo": "redmi_note17_pro_5g_256_8gb",
        "marca": "Xiaomi",
        "modelo": "Redmi Note 17 Pro 5G 256GB 8GB RAM",
        "cor": "Nao informada",
        "plataforma": "Mercado Livre",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": 2469.00,
        "preco_base_cartao": 2610.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 261.00,
        "total_anunciado": 2610.00,
        "condicao": "Sem juros anunciado",
        "observacao": "Confirmar nome exato do aparelho no link original."
    },
    {
        "codigo_modelo": "poco_x8_pro_512_12gb",
        "marca": "Xiaomi",
        "modelo": "POCO X8 Pro 512GB 12GB RAM",
        "cor": "Nao informada",
        "plataforma": "Mercado Livre",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": 2865.00,
        "preco_base_cartao": 3255.00,
        "base_confirmada": True,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 325.50,
        "total_anunciado": 3255.00,
        "condicao": "Sem juros anunciado",
        "observacao": "Configuracao de 512GB/12GB RAM; nao comparar com a versao de 256GB/8GB."
    },
    {
        "codigo_modelo": "redmi_17_256",
        "marca": "Xiaomi",
        "modelo": "Redmi 17 256GB",
        "cor": "Nao informada",
        "plataforma": "Mercado Livre",
        "vendedor": "Confirmar no anuncio",
        "preco_a_vista": None,
        "preco_base_cartao": None,
        "base_confirmada": False,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 177.72,
        "total_anunciado": None,
        "condicao": "Nao esclarecida",
        "observacao": "A captura mostra 12 x R$ 177,72, mas nao esclarece a modalidade do preco exibido."
    }
]

# =====================================================================
# 2. PARAMETROS DA PESQUISA PARA A OPCAO 2
# =====================================================================

# [PESQUISA OBRIGATORIA]
# Depois de pesquisar ofertas reais de cada plataforma, calcule a taxa mensal
# implicita de CADA oferta. Coloque os resultados (em percentual) na lista.
# Exemplo ficticio de preenchimento: "Amazon": [1.4, 1.8, 2.0]
# NAO copie esses numeros de exemplo: use somente resultados calculados pelo grupo.

AMOSTRAS_TAXAS_MENSAIS = {
    "Amazon": [],          # TODO: pesquisar e inserir taxas mensais reais estimadas.
    "Magazine Luiza": [],  # TODO: pesquisar e inserir taxas mensais reais estimadas.
    "Mercado Livre": []    # TODO: pesquisar e inserir taxas mensais reais estimadas.
}

# [PESQUISA OBRIGATORIA]
# Para cada oferta em que o preco-base no cartao e o preco Pix sejam confirmados,
# calcule o desconto percentual: (B - preco_pix) / B * 100.
# Insira os percentuais observados na plataforma correspondente.
# Exemplo ficticio de preenchimento: "Amazon": [5.0, 4.0, 6.0]

AMOSTRAS_DESCONTOS_PIX = {
    "Amazon": [],          # TODO: pesquisar e inserir descontos Pix observados.
    "Magazine Luiza": [],  # TODO: pesquisar e inserir descontos Pix observados.
    "Mercado Livre": []    # TODO: pesquisar e inserir descontos Pix observados.
}

# =====================================================================
# 3. FUNCOES DE ENTRADA E FORMATACAO
# =====================================================================


# Autor: [Nome do integrante responsavel]
def formatar_moeda(valor):
    """Converte um numero para o formato monetario brasileiro."""
    if valor is None:
        return "Nao informado"
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


# Autor: [Nome do integrante responsavel]
def formatar_percentual(valor):
    """Formata um percentual com duas casas decimais."""
    if valor is None:
        return "Nao calculado"
    return f"{valor:.2f}%".replace(".", ",")


# Autor: [Nome do integrante responsavel]
def ler_texto(mensagem):
    """Solicita um texto nao vazio ao usuario."""
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("O campo nao pode ficar vazio.")


# Autor: [Nome do integrante responsavel]
def ler_float(mensagem, minimo=0.0, permitir_igual=True):
    """Le um numero decimal, aceitando virgula ou ponto."""
    while True:
        texto = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(texto)
            if permitir_igual and valor >= minimo:
                return valor
            if not permitir_igual and valor > minimo:
                return valor
            print("Valor fora do limite permitido.")
        except ValueError:
            print("Digite um valor numerico valido.")


# Autor: [Nome do integrante responsavel]
def ler_inteiro(mensagem, minimo=1, maximo=60):
    """Le um numero inteiro dentro do intervalo informado."""
    while True:
        texto = input(mensagem).strip()
        try:
            valor = int(texto)
            if minimo <= valor <= maximo:
                return valor
            print("Digite um inteiro entre", minimo, "e", maximo, ".")
        except ValueError:
            print("Digite um numero inteiro valido.")


# =====================================================================
# 4. FUNCOES MATEMATICAS DAS OFERTAS REAIS (OPCAO 1)
# =====================================================================


# Autor: [Nome do integrante responsavel]
def carregar_ofertas_reais():
    """Retorna os registros reais transcritos das capturas de tela."""
    # A leitura de planilha nao foi implementada enquanto aguarda autorizacao
    # do professor. Se ele permitir, esta funcao sera substituida/adaptada.
    return OFERTAS_REAIS


# Autor: [Nome do integrante responsavel]
def calcular_total_prazo(oferta):
    """Calcula entrada mais quantidade de parcelas vezes valor da parcela."""
    total = oferta["entrada"] + oferta["parcelas"] * oferta["valor_parcela"]
    return round(total, 2)


# Autor: [Nome do integrante responsavel]
def calcular_juros_reais(oferta):
    """Calcula o acrescimo em relacao ao preco a vista confirmado."""
    preco_vista = oferta["preco_a_vista"]
    if preco_vista is None or preco_vista <= 0:
        return None
    return round(calcular_total_prazo(oferta) - preco_vista, 2)


# Autor: [Nome do integrante responsavel]
def calcular_juros_percentual(oferta):
    """Calcula o acrescimo percentual sobre o preco a vista confirmado."""
    preco_vista = oferta["preco_a_vista"]
    if preco_vista is None or preco_vista <= 0:
        return None
    juros = calcular_juros_reais(oferta)
    return round((juros / preco_vista) * 100, 2)


# Autor: [Nome do integrante responsavel]
def ordenar_ofertas_por_total(ofertas_modelo):
    """Ordena ofertas do mesmo modelo pelo total calculado, sem sorted()."""
    copia = ofertas_modelo[:]
    for inicio in range(len(copia)):
        menor_indice = inicio
        for atual in range(inicio + 1, len(copia)):
            total_atual = calcular_total_prazo(copia[atual])
            total_menor = calcular_total_prazo(copia[menor_indice])
            if total_atual < total_menor:
                menor_indice = atual
        temporaria = copia[inicio]
        copia[inicio] = copia[menor_indice]
        copia[menor_indice] = temporaria
    return copia


# Autor: [Nome do integrante responsavel]
def achar_mais_barata(ofertas_modelo):
    """Retorna todas as ofertas empatadas com o menor total a prazo."""
    if len(ofertas_modelo) == 0:
        return []
    menor = calcular_total_prazo(ofertas_modelo[0])
    for oferta in ofertas_modelo[1:]:
        total = calcular_total_prazo(oferta)
        if total < menor:
            menor = total
    resultado = []
    for oferta in ofertas_modelo:
        if abs(calcular_total_prazo(oferta) - menor) <= 0.01:
            resultado.append(oferta)
    return resultado


# Autor: [Nome do integrante responsavel]
def achar_mais_cara(ofertas_modelo):
    """Retorna todas as ofertas empatadas com o maior total a prazo."""
    if len(ofertas_modelo) == 0:
        return []
    maior = calcular_total_prazo(ofertas_modelo[0])
    for oferta in ofertas_modelo[1:]:
        total = calcular_total_prazo(oferta)
        if total > maior:
            maior = total
    resultado = []
    for oferta in ofertas_modelo:
        if abs(calcular_total_prazo(oferta) - maior) <= 0.01:
            resultado.append(oferta)
    return resultado


# Autor: [Nome do integrante responsavel]
def listar_codigos_modelos(ofertas):
    """Retorna codigos de modelos sem repeticoes."""
    codigos = []
    for oferta in ofertas:
        codigo = oferta["codigo_modelo"]
        if codigo not in codigos:
            codigos.append(codigo)
    return codigos


# Autor: [Nome do integrante responsavel]
def buscar_ofertas_por_modelo(ofertas, codigo_modelo):
    """Seleciona apenas registros com o mesmo codigo de modelo/configuracao."""
    encontradas = []
    for oferta in ofertas:
        if oferta["codigo_modelo"] == codigo_modelo:
            encontradas.append(oferta)
    return encontradas


# Autor: [Nome do integrante responsavel]
def selecionar_modelo_real(ofertas):
    """Mostra o catalogo real e solicita o modelo para comparacao."""
    codigos = listar_codigos_modelos(ofertas)
    print("\nMODELOS CADASTRADOS NA BASE REAL")
    for indice in range(len(codigos)):
        grupo = buscar_ofertas_por_modelo(ofertas, codigos[indice])
        primeiro = grupo[0]
        print(str(indice + 1) + " - " + primeiro["marca"] + " | " + primeiro["modelo"])
    escolha = ler_inteiro("Escolha o numero do modelo: ", 1, len(codigos))
    return codigos[escolha - 1]


# Autor: [Nome do integrante responsavel]
def exibir_comparacao_real(ofertas_modelo):
    """Exibe ofertas reais, ranking de totais e limites da amostra."""
    if len(ofertas_modelo) == 0:
        print("Nao ha ofertas cadastradas para esse modelo.")
        return

    ordenadas = ordenar_ofertas_por_total(ofertas_modelo)
    plataformas_encontradas = []

    primeiro = ofertas_modelo[0]
    print("\nCOMPARACAO DE OFERTAS REAIS")
    print("Produto:", primeiro["marca"], primeiro["modelo"])
    print("-" * 105)
    print(f"{'Loja':<18} {'Parcelamento':<22} {'Total a prazo':>17} {'Pix/a vista':>17}")
    print("-" * 105)

    for oferta in ordenadas:
        if oferta["plataforma"] not in plataformas_encontradas:
            plataformas_encontradas.append(oferta["plataforma"])
        plano = str(oferta["parcelas"]) + " x " + formatar_moeda(oferta["valor_parcela"])
        print(
            f"{oferta['plataforma']:<18} {plano:<22} "
            f"{formatar_moeda(calcular_total_prazo(oferta)):>17} "
            f"{formatar_moeda(oferta['preco_a_vista']):>17}"
        )
        print("  Preco-base cartao:", formatar_moeda(oferta["preco_base_cartao"]))
        print("  Condicao:", oferta["condicao"])

        acrescimo = calcular_juros_reais(oferta)
        percentual = calcular_juros_percentual(oferta)
        if acrescimo is not None:
            print("  Acrescimo sobre o preco a vista (regra do projeto):", formatar_moeda(acrescimo))
            print("  Percentual sobre o preco a vista:", formatar_percentual(percentual))
        else:
            print("  Acrescimo percentual nao calculado: preco a vista nao confirmado.")

        if oferta["preco_base_cartao"] is not None and oferta["base_confirmada"]:
            diferenca_base = round(calcular_total_prazo(oferta) - oferta["preco_base_cartao"], 2)
            print("  Diferenca contra o preco-base do cartao:", formatar_moeda(diferenca_base))
        else:
            print("  Preco-base do cartao nao confirmado; nao calcular taxa a partir desta oferta.")

        if oferta["total_anunciado"] is not None:
            diferenca_anuncio = round(calcular_total_prazo(oferta) - oferta["total_anunciado"], 2)
            if abs(diferenca_anuncio) > 0.01:
                print("  ATENCAO: parcelas somadas divergem do total anunciado em", formatar_moeda(diferenca_anuncio))
        if oferta["vendedor"] != "":
            print("  Vendedor:", oferta["vendedor"])
        if oferta["observacao"]:
            print("  Observacao:", oferta["observacao"])
        print("." * 105)

    if len(plataformas_encontradas) < 3:
        print("ATENCAO: a coleta deste modelo nao possui ofertas nas tres plataformas.")
        print("Nao e correto concluir um ranking entre Amazon, Magazine Luiza e Mercado Livre sem completar a amostra.")

    melhores = achar_mais_barata(ofertas_modelo)
    piores = achar_mais_cara(ofertas_modelo)

    print("\nMENOR TOTAL A PRAZO:")
    for oferta in melhores:
        print(oferta["plataforma"], "-", formatar_moeda(calcular_total_prazo(oferta)))

    print("MAIOR TOTAL A PRAZO:")
    for oferta in piores:
        print(oferta["plataforma"], "-", formatar_moeda(calcular_total_prazo(oferta)))


# =====================================================================
# 5. FUNCOES PARA CALIBRAR TAXAS E DESCONTOS (OPCAO 2)
# =====================================================================


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]
def calcular_media(valores):
    """Calcula a media aritmetica usando acumulador e laco for."""
    if len(valores) == 0:
        return None
    soma = 0.0
    for valor in valores:
        soma = soma + valor
    return soma / len(valores)


# Autor: [Nome do integrante responsavel]
def obter_media_taxa(plataforma):
    """Retorna a taxa mensal media pesquisada para uma plataforma."""
    return calcular_media(AMOSTRAS_TAXAS_MENSAIS[plataforma])


# Autor: [Nome do integrante responsavel]
def obter_media_desconto(plataforma):
    """Retorna o desconto medio Pix pesquisado para uma plataforma."""
    return calcular_media(AMOSTRAS_DESCONTOS_PIX[plataforma])


# Autor: [Nome do integrante responsavel]
def fator_presente_parcelas(taxa_percentual, quantidade_parcelas):
    """Soma fatores de desconto para parcelas fixas, sem potencia pronta."""
    taxa_decimal = taxa_percentual / 100
    fator = 1.0
    soma = 0.0
    for mes in range(1, quantidade_parcelas + 1):
        fator = fator / (1 + taxa_decimal)
        soma = soma + fator
    return soma


# Autor: [Nome do integrante responsavel]
def calcular_taxa_implicita(preco_base, entrada, parcelas, valor_parcela):
    """Estima a taxa mensal de uma oferta real por busca binaria."""
    if preco_base is None or preco_base <= 0:
        return None
    if entrada < 0 or entrada >= preco_base or parcelas <= 0 or valor_parcela <= 0:
        return None

    capital_financiado = preco_base - entrada
    total_parcelas = parcelas * valor_parcela

    if abs(total_parcelas - capital_financiado) <= 0.02:
        return 0.0
    if total_parcelas < capital_financiado:
        return None

    limite_inferior = 0.0
    limite_superior = 1.0

    # Aumenta o limite ate o valor presente ficar abaixo do capital financiado.
    while valor_parcela * fator_presente_parcelas(limite_superior * 100, parcelas) > capital_financiado:
        limite_superior = limite_superior * 2
        if limite_superior > 1000000:
            return None

    # Busca binaria: procura a taxa que aproxima o valor presente do capital.
    for tentativa in range(100):
        taxa_teste = (limite_inferior + limite_superior) / 2
        valor_presente = valor_parcela * fator_presente_parcelas(taxa_teste * 100, parcelas)
        if valor_presente > capital_financiado:
            limite_inferior = taxa_teste
        else:
            limite_superior = taxa_teste

    taxa_final_decimal = (limite_inferior + limite_superior) / 2
    return taxa_final_decimal * 100


# Autor: [Nome do integrante responsavel]
def calcular_desconto_observado(preco_base, preco_pix):
    """Calcula o percentual de desconto Pix observado em uma oferta."""
    if preco_base is None or preco_pix is None or preco_base <= 0:
        return None
    if preco_pix < 0 or preco_pix > preco_base:
        return None
    return ((preco_base - preco_pix) / preco_base) * 100


# Autor: [Nome do integrante responsavel]
def calcular_preco_pix(preco_base, desconto_percentual):
    """Aplica o desconto medio Pix sobre o preco-base informado."""
    if desconto_percentual is None:
        return None
    if desconto_percentual < 0 or desconto_percentual >= 100:
        raise ValueError("O desconto deve ser maior ou igual a zero e menor que 100%.")
    return round(preco_base * (1 - desconto_percentual / 100), 2)


# Autor: [Nome do integrante responsavel]
def calcular_parcela_simulada(preco_base, entrada, taxa_percentual, parcelas):
    """Calcula prestacao fixa pelo modelo Price, com primeira parcela em um mes."""
    if preco_base <= 0 or entrada < 0 or entrada >= preco_base:
        raise ValueError("Preco-base e entrada invalidos.")
    if parcelas <= 0 or taxa_percentual < 0:
        raise ValueError("Parcelas ou taxa invalidas.")

    capital = preco_base - entrada
    if taxa_percentual == 0:
        return round(capital / parcelas, 2)

    fator = fator_presente_parcelas(taxa_percentual, parcelas)
    parcela = capital / fator
    return round(parcela, 2)


# Autor: [Nome do integrante responsavel]
def simular_condicao_plataforma(plataforma, preco_base, entrada, parcelas):
    """Calcula Pix e financiamento usando medias pesquisadas da plataforma."""
    taxa_media = obter_media_taxa(plataforma)
    desconto_medio = obter_media_desconto(plataforma)

    if taxa_media is None:
        return None

    valor_parcela = calcular_parcela_simulada(preco_base, entrada, taxa_media, parcelas)
    total_parcelado = round(entrada + valor_parcela * parcelas, 2)
    preco_pix = calcular_preco_pix(preco_base, desconto_medio)

    return {
        "plataforma": plataforma,
        "taxa_media": taxa_media,
        "desconto_medio": desconto_medio,
        "preco_pix": preco_pix,
        "valor_parcela": valor_parcela,
        "total_parcelado": total_parcelado,
        "acrescimo_sobre_base": round(total_parcelado - preco_base, 2),
        "diferenca_vs_pix": None if preco_pix is None else round(total_parcelado - preco_pix, 2)
    }


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]
def simular_faixa_parcelas(plataforma, preco_base, entrada, limite_parcelas, limite_mensal):
    """Mostra prazos de 1 ate o limite e identifica o primeiro que cabe no orcamento."""
    taxa_media = obter_media_taxa(plataforma)
    desconto_medio = obter_media_desconto(plataforma)
    if taxa_media is None:
        print("Sem taxa media cadastrada para", plataforma, "- preencher AMOSTRAS_TAXAS_MENSAIS.")
        return []

    resultados = []
    print("\nPLATAFORMA:", plataforma, "| Taxa media pesquisada:", formatar_percentual(taxa_media))
    print(f"{'Parcelas':>9} {'Valor mensal':>18} {'Total parcelado':>20} {'Diferenca vs Pix':>19}")
    print("-" * 75)

    for quantidade in range(1, limite_parcelas + 1):
        parcela = calcular_parcela_simulada(preco_base, entrada, taxa_media, quantidade)
        total = round(entrada + parcela * quantidade, 2)
        pix = calcular_preco_pix(preco_base, desconto_medio)
        diferenca_pix = None if pix is None else round(total - pix, 2)
        registro = {
            "plataforma": plataforma,
            "parcelas": quantidade,
            "parcela": parcela,
            "total": total,
            "preco_pix": pix,
            "diferenca_pix": diferenca_pix,
            "cabe_orcamento": limite_mensal <= 0 or parcela <= limite_mensal
        }
        resultados.append(registro)
        texto_diferenca = "Nao calculada" if diferenca_pix is None else formatar_moeda(diferenca_pix)
        print(
            f"{quantidade:>9} {formatar_moeda(parcela):>18} "
            f"{formatar_moeda(total):>20} {texto_diferenca:>19}"
        )

    if desconto_medio is None:
        print("Desconto Pix medio nao cadastrado para esta plataforma.")
    else:
        print("Desconto Pix medio da amostra:", formatar_percentual(desconto_medio))

    if limite_mensal > 0:
        primeiro_compativel = None
        for registro in resultados:
            if registro["parcela"] <= limite_mensal:
                primeiro_compativel = registro
                break
        if primeiro_compativel is None:
            print("Nenhum prazo analisado cabe no limite mensal informado.")
        else:
            print(
                "Primeiro prazo que cabe no limite mensal: ",
                primeiro_compativel["parcelas"], "parcelas; parcela de",
                formatar_moeda(primeiro_compativel["parcela"]),
                "e total de", formatar_moeda(primeiro_compativel["total"])
            )
    return resultados


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]

# Autor: [Seu nome]
def executar_simulacao_avulsa():
    """Simula uma compra independente da base de ofertas reais."""

    print("\nSIMULACAO AVULSA DE SMARTPHONE")

    # 1. Receber os dados do aparelho
    modelo = ler_texto("Nome do smartphone: ")

    preco_base = ler_float(
        "Preco-base no cartao (R$): ", 0.0, False
    )

    entrada = ler_float(
        "Valor da entrada (R$): ", 0.0, True
    )

    if entrada >= preco_base:
        print("A entrada deve ser menor que o preco-base.")
        return

    # 2. Permitir escolher somente uma plataforma
    print("\nESCOLHA A PLATAFORMA")

    for indice in range(len(PLATAFORMAS)):
        print(indice + 1, "-", PLATAFORMAS[indice])

    escolha = ler_inteiro(
        "Escolha a loja: ", 1, len(PLATAFORMAS)
    )

    plataforma = PLATAFORMAS[escolha - 1]

    # 3. Receber a quantidade exata de parcelas
    parcelas = ler_inteiro(
        "Quantidade de parcelas: ", 1, 48
    )

    print("\nPROCESSANDO SIMULACAO...")

    # 4. Calcular usando a media pesquisada da loja
    resultado = simular_condicao_plataforma(
        plataforma,
        preco_base,
        entrada,
        parcelas
    )

    if resultado is None:
        print("\nTaxa media ainda nao cadastrada para esta loja.")
        print("Preencha AMOSTRAS_TAXAS_MENSAIS no codigo.")
        return

    # 5. Apresentar os resultados
    print("\n" + "=" * 55)
    print("RESULTADO DA SIMULACAO")
    print("=" * 55)

    print("Smartphone:", modelo)
    print("Plataforma:", plataforma)
    print("Preco-base:", formatar_moeda(preco_base))
    print("Entrada:", formatar_moeda(entrada))
    print("Capital financiado:", formatar_moeda(preco_base - entrada))

    print(
        "Taxa mensal estimada:",
        formatar_percentual(resultado["taxa_media"])
    )

    print("Quantidade de parcelas:", parcelas)

    print(
        "Valor de cada parcela:",
        formatar_moeda(resultado["valor_parcela"])
    )

    print(
        "Total parcelado:",
        formatar_moeda(resultado["total_parcelado"])
    )

    print(
        "Juros/acrescimo estimado:",
        formatar_moeda(resultado["acrescimo_sobre_base"])
    )

    print(
        "Percentual de acrescimo:",
        formatar_percentual(
            resultado["acrescimo_sobre_base"] / preco_base * 100
        )
    )

    if resultado["preco_pix"] is not None:
        print(
            "Preco estimado no Pix:",
            formatar_moeda(resultado["preco_pix"])
        )

        print(
            "Diferenca entre parcelado e Pix:",
            formatar_moeda(resultado["diferenca_vs_pix"])
        )
    else:
        print("Desconto Pix medio ainda nao cadastrado.")

    print("=" * 55)
    print("Simulacao baseada nas medias da pesquisa do grupo.")


# =====================================================================
# 6. PROJECAO ACADEMICA COM K (OPCAO 3)
# =====================================================================


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]
def calcular_parametros_k(k):
    """Calcula taxa mensal e prazo conforme as formulas do professor."""
    if not isinstance(k, int) or k < 0:
        raise ValueError("K deve ser um inteiro nao negativo.")
    taxa = (k % 5) + 1
    meses = (k % 6) + 6
    return taxa, meses


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]
def simular_juros_compostos(valor, taxa, meses):
    """Simula juros compostos com for, sem operador de potencia ou pow()."""
    if valor <= 0:
        raise ValueError("O capital inicial deve ser maior que zero.")
    if taxa < 0:
        raise ValueError("A taxa nao pode ser negativa.")
    if not isinstance(meses, int) or meses <= 0:
        raise ValueError("O prazo deve ser um inteiro positivo.")

    saldo = valor
    resultados = []
    for mes in range(1, meses + 1):
        saldo_anterior = saldo
        saldo = saldo * (1 + taxa / 100)
        juros_mes = saldo - saldo_anterior
        juros_acumulados = saldo - valor
        resultados.append({
            "mes": mes,
            "saldo": round(saldo, 2),
            "juros_mes": round(juros_mes, 2),
            "juros_acumulados": round(juros_acumulados, 2)
        })
    return resultados


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]
def executar_projecao_k():
    """Solicita smartphone e capital, aplicando somente taxa e prazo do K."""
    print("\nPROJECAO HIPOTETICA COM K")
    modelo = ler_texto("Nome/modelo do smartphone: ")
    preco_base = ler_float("Preco-base normal no cartao (R$): ", 0.0, False)
    taxa, meses = calcular_parametros_k(K)
    resultados = simular_juros_compostos(preco_base, taxa, meses)

    print("\nProduto:", modelo)
    print("Capital inicial:", formatar_moeda(preco_base))
    print("K:", K)
    print("Taxa mensal determinada pelo K:", formatar_percentual(taxa))
    print("Prazo determinado pelo K:", meses, "meses")
    print("\nEvolucao mensal:")
    print(f"{'Mes':>5} {'Saldo':>18} {'Juros do mes':>18} {'Juros acumulados':>21}")
    print("-" * 68)
    for item in resultados:
        print(
            f"{item['mes']:>5} {formatar_moeda(item['saldo']):>18} "
            f"{formatar_moeda(item['juros_mes']):>18} "
            f"{formatar_moeda(item['juros_acumulados']):>21}"
        )
    print("Montante final:", formatar_moeda(resultados[-1]["saldo"]))
    print("Juros hipoteticos acumulados:", formatar_moeda(resultados[-1]["juros_acumulados"]))
    print("Esta projecao e academica e nao representa juros cobrados por uma loja.")


# =====================================================================
# 7. MENU PRINCIPAL
# =====================================================================


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]
def exibir_menu():
    """Mostra as quatro opcoes principais do sistema."""
    print("\n" + "=" * 66)
    print("COMPARADOR DE OFERTAS DE SMARTPHONES - PROJETO 15")
    print("=" * 66)
    print("1 - Comparar ofertas reais cadastradas (planilha futura)")
    print("2 - Simular parcelamento avulso com medias pesquisadas")
    print("3 - Fazer projecao hipotetica com K")
    print("0 - Sair")
    print("=" * 66)


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]
def executar_comparacao_real():
    """Executa a opcao 1 usando a base de ofertas reais cadastradas."""
    ofertas = carregar_ofertas_reais()
    if len(ofertas) == 0:
        print("A base de ofertas reais esta vazia.")
        return
    codigo = selecionar_modelo_real(ofertas)
    ofertas_modelo = buscar_ofertas_por_modelo(ofertas, codigo)
    exibir_comparacao_real(ofertas_modelo)


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]
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
        elif opcao == "0":
            print("Programa encerrado.")
            break
        else:
            print("Opcao invalida. Digite 1, 2, 3 ou 0.")


# =====================================================================
# 8. TESTES MANUAIS DE APOIO (NAO RODAM AUTOMATICAMENTE)
# =====================================================================


# Autor: [JOSUÉ GABRIEL SOUSA CUNHA]
def executar_testes_basicos():
    """Executa verificacoes simples das funcoes matematicas do pre-codigo."""
    # Teste do K = 10: taxa 1% e prazo 10 meses.
    taxa, meses = calcular_parametros_k(10)
    assert taxa == 1
    assert meses == 10

    # Teste de juros compostos: R$ 1.000 a 1% por 10 meses.
    resultado = simular_juros_compostos(1000.00, 1.0, 10)
    assert resultado[0]["saldo"] == 1010.00
    assert resultado[2]["saldo"] == 1030.30

    # Teste de parcela sem juros: R$ 1.200 em 12 parcelas = R$ 100.
    parcela = calcular_parcela_simulada(1200.00, 0.00, 0.0, 12)
    assert parcela == 100.00

    # Teste de taxa positiva: uma taxa positiva deve elevar o total pago.
    parcela_com_juros = calcular_parcela_simulada(1200.00, 0.00, 2.0, 12)
    assert parcela_com_juros * 12 > 1200.00

    # Teste da taxa implicita
    taxa_estimada = calcular_taxa_implicita(1000.00, 0.00, 10, 110.00)
    assert taxa_estimada is not None and taxa_estimada > 0

    print("Todos os testes basicos foram aprovados.")


if __name__ == "__main__":
    main()
