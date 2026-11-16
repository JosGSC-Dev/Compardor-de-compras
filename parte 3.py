"""

PROJETO 15 - COMPARADOR DE OFERTAS E SIMULADOR DE PARCELAMENTO

Disciplina: Programacao I - Python

Grupo: [PREENCHER]

Integrantes: [PREENCHER]

K do grupo: 10 (confirmar calculo com as matriculas e com o professor)



OBJETIVO DO PRE-CODIGO

1. Comparar ofertas reais previamente cadastradas (opcao 1).

2. Simular um smartphone informado pelo usuario (opcao 2), combinando:

   - taxa mensal de referencia do banco/cartao escolhido;

   - desconto medio no Pix da plataforma escolhida;

   - preco-base, entrada e quantidade de parcelas informados pelo usuario.

3. Fazer a simulacao academica de juros compostos definida pelo K (opcao 3).



FONTE DAS TAXAS BANCARIAS

As taxas cadastradas abaixo foram transcritas do Banco Central do Brasil,

modalidade "Cartao de credito - parcelado - Prefixado", Pessoa Fisica,

periodo de 09/10/2026 a 16/10/2026. Sao referencias estatisticas por instituicao,

nao uma promessa da taxa individual oferecida a cada cliente/cartao.

Fonte oficial:

https://www.bcb.gov.br/estatisticas/reporttxjuroshistorico?InicioPeriodo=2024-01-&codigoModalidade=215101&codigoSegmento=1&historicotaxajurosdiario_page=1&tipoModalidade=D



RESTRICOES ADOTADAS NESTE PRE-CODIGO

- Nenhum import.

- Nenhuma biblioteca financeira.

- Nenhum operador **.

- Nenhuma funcao pow().

- Juros compostos e fator de valor presente calculados com lacos for.



IMPORTANTE SOBRE A OPCAO 1

A leitura automatica de planilha ainda nao foi implementada, pois o grupo

precisa confirmar com o professor se ela sera permitida. Por enquanto, os

registros reais ficam na lista OFERTAS_REAIS.



IMPORTANTE SOBRE A OPCAO 2

A taxa e selecionada pelo banco emissor informado pelo usuario, usando a

referencia do Banco Central. O desconto Pix e selecionado pela plataforma.

As listas de descontos devem ser validadas com evidencias reais do grupo.

A simulacao e uma estimativa academica, nao substitui a taxa/CET do contrato.



# [IA] Este pre-codigo foi estruturado e atualizado com apoio de IA. O grupo

# deve revisar, testar, compreender e adaptar todas as funcoes antes da entrega.

"""



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

# 2. PARAMETROS FINANCEIROS DA OPCAO 2 - TAXA POR BANCO, DESCONTO POR LOJA



# TAXAS DE REFERENCIA POR INSTITUICAO FINANCEIRA

# Fonte: Banco Central do Brasil (BCB).

# Modalidade: Cartao de credito - parcelado - Prefixado (Pessoa Fisica).

# Periodo de referencia: 09/10/2026 a 16/10/2026.

# Unidade: percentual ao mes (% a.m.).

#

# IMPORTANTE:

# - Os nomes comerciais foram associados as instituicoes listadas pelo BCB.

# - Nubank corresponde ao registro "NU FINANCEIRA S.A. CFI".

# - A taxa publicada e uma media estatistica da modalidade, nao a taxa

#   contratual garantida para todo cliente ou cartao dessa instituicao.

# - Confirmar no cartao/contrato quem e o emissor da operacao.

# - Para atualizar, consulte a mesma modalidade e registre o novo periodo.

# Fonte oficial:

# https://www.bcb.gov.br/estatisticas/reporttxjuroshistorico?InicioPeriodo=2024-01-&codigoModalidade=215101&codigoSegmento=1&historicotaxajurosdiario_page=1&tipoModalidade=D



PERIODO_TAXAS_BCB = "09/10/2026 a 16/10/2026"

MODALIDADE_TAXAS_BCB = "Cartao de credito - parcelado - Prefixado (Pessoa Fisica)"



BANCOS_CARTAO = [

    "Itaú",

    "Nubank",

    "Bradesco",

    "Santander",

    "Caixa Econômica Federal"

]



# Os valores estao em listas para permitir incluir observacoes de outros

# periodos e calcular uma media simples, se essa for a metodologia escolhida.

# Neste pre-codigo, cada banco possui uma observacao do periodo acima.

# Valores consultados na tabela do BCB em 16/11/2026:

# Bradesco: 9,02%; Nu Financeira: 9,06%; Itau: 9,91%;

# Santander: 10,16%; Caixa: 8,62% ao mes.

AMOSTRAS_TAXAS_MENSAIS = {

    "Itaú": [9.91],

    "Nubank": [9.06],

    "Bradesco": [9.02],

    "Santander": [10.16],

    "Caixa Econômica Federal": [8.62]

}



# DESCONTOS MEDIOS POR PLATAFORMA

# [PESQUISA OBRIGATORIA]

# Os percentuais abaixo foram informados pelo grupo no rascunho.

# Antes da entrega, confirmem que cada desconto foi calculado comparando

# preco-base no cartao e preco Pix da MESMA oferta, vendedor e variante.

# Formula: (preco_base - preco_pix) / preco_base * 100.

# Removam amostras sem print, link, data ou preco-base confirmado.

AMOSTRAS_DESCONTOS_PIX = {

    "Amazon": [19.0, 9.0, 24.0],

    "Magazine Luiza": [21.0, 15.0, 10.0],

    "Mercado Livre": [22.0, 20.0, 15.0]

}



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

def converter_valor_numerico(texto):
    """Converte valores como 6767, 6767,50 ou R$ 6.767,50 para float."""
    texto = texto.strip().replace("R$", "").replace(" ", "")
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif "." in texto:
        partes = texto.split(".")
        if len(partes) > 2 or (len(partes) == 2 and len(partes[1]) == 3):
            texto = "".join(partes)
    return float(texto)


# Autor: [Nome do integrante responsavel]
def ler_float(mensagem, minimo=0.0, permitir_igual=True):
    """Le um numero, aceitando ponto, virgula e formato monetario brasileiro."""
    while True:
        texto = input(mensagem).strip()
        try:
            valor = converter_valor_numerico(texto)
            if valor != valor or valor == float("inf") or valor == float("-inf"):
                print("Digite um valor finito.")
                continue
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
    """Calcula o acrescimo sobre o preco-base normal do cartao confirmado."""
    preco_base = oferta["preco_base_cartao"]
    if not oferta["base_confirmada"] or preco_base is None or preco_base <= 0:
        return None
    return round(calcular_total_prazo(oferta) - preco_base, 2)


# Autor: [Nome do integrante responsavel]
def calcular_juros_percentual(oferta):
    """Calcula o acrescimo percentual sobre o preco-base normal do cartao."""
    preco_base = oferta["preco_base_cartao"]
    if not oferta["base_confirmada"] or preco_base is None or preco_base <= 0:
        return None
    juros = calcular_juros_reais(oferta)
    return round((juros / preco_base) * 100, 2)








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
            print("  Acrescimo/juros sobre o preco-base do cartao:", formatar_moeda(acrescimo))
            print("  Percentual sobre o preco-base do cartao:", formatar_percentual(percentual))
        else:
            print("  Juros nao calculados: preco-base do cartao nao confirmado.")

        if oferta["preco_a_vista"] is not None:
            diferenca_pix = round(calcular_total_prazo(oferta) - oferta["preco_a_vista"], 2)
            print("  Diferenca entre total parcelado e preco Pix/a vista:", formatar_moeda(diferenca_pix))





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





# Autor: [Nome do integrante responsavel]

def calcular_media(valores):

    """Calcula a media aritmetica usando acumulador e laco for."""

    if len(valores) == 0:

        return None

    soma = 0.0

    for valor in valores:

        soma = soma + valor

    return soma / len(valores)





# Autor: [Nome do integrante responsavel]

def obter_media_taxa_banco(banco):

    """Retorna a taxa mensal media cadastrada para o banco selecionado."""

    if banco not in AMOSTRAS_TAXAS_MENSAIS:

        return None

    return calcular_media(AMOSTRAS_TAXAS_MENSAIS[banco])





# Autor: [Nome do integrante responsavel]

def obter_media_desconto(plataforma):

    """Retorna o desconto medio Pix pesquisado para uma plataforma."""

    if plataforma not in AMOSTRAS_DESCONTOS_PIX:

        return None

    return calcular_media(AMOSTRAS_DESCONTOS_PIX[plataforma])





# Autor: [Nome do integrante responsavel]

def selecionar_banco_cartao():

    """Apresenta bancos disponiveis e recebe o emissor do cartao do usuario."""

    print("\nSELECIONE O BANCO/EMISSOR DO CARTAO")

    for indice in range(len(BANCOS_CARTAO)):

        print(str(indice + 1) + " - " + BANCOS_CARTAO[indice])

    escolha = ler_inteiro("Banco do cartao: ", 1, len(BANCOS_CARTAO))

    return BANCOS_CARTAO[escolha - 1]





# Autor: [Nome do integrante responsavel]

def selecionar_plataforma():

    """Apresenta as plataformas e recebe a loja desejada pelo usuario."""

    print("\nSELECIONE A PLATAFORMA DE COMPRA")

    for indice in range(len(PLATAFORMAS)):

        print(str(indice + 1) + " - " + PLATAFORMAS[indice])

    escolha = ler_inteiro("Plataforma: ", 1, len(PLATAFORMAS))

    return PLATAFORMAS[escolha - 1]





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

def simular_condicao_plataforma(plataforma, banco, preco_base, entrada, parcelas):

    """Simula uma compra usando taxa do banco e desconto da plataforma."""

    taxa_banco = obter_media_taxa_banco(banco)

    desconto_medio = obter_media_desconto(plataforma)



    if taxa_banco is None or desconto_medio is None:

        return None



    valor_parcela = calcular_parcela_simulada(

        preco_base, entrada, taxa_banco, parcelas

    )

    total_parcelado = round(entrada + valor_parcela * parcelas, 2)

    preco_pix = calcular_preco_pix(preco_base, desconto_medio)



    return {

        "plataforma": plataforma,

        "banco": banco,

        "taxa_banco": taxa_banco,

        "desconto_medio": desconto_medio,

        "preco_pix": preco_pix,

        "valor_parcela": valor_parcela,

        "total_parcelado": total_parcelado,

        "acrescimo_sobre_base": round(total_parcelado - preco_base, 2),

        "diferenca_vs_pix": None if preco_pix is None else round(total_parcelado - preco_pix, 2)

    }



# Autor: [Nome do integrante responsavel]

def simular_faixa_parcelas(plataforma, banco, preco_base, entrada, limite_parcelas, limite_mensal):

    """Compara varios prazos usando o banco escolhido e uma plataforma."""

    taxa_banco = obter_media_taxa_banco(banco)

    desconto_medio = obter_media_desconto(plataforma)



    if taxa_banco is None:

        print("Sem taxa de referencia cadastrada para", banco)

        return []



    if desconto_medio is None:

        print("Sem amostras de desconto Pix cadastradas para", plataforma)

        return []



    resultados = []

    preco_pix = calcular_preco_pix(preco_base, desconto_medio)



    print("\nBANCO/EMISSOR:", banco)

    print("Taxa mensal de referencia BCB:", formatar_percentual(taxa_banco))

    print("Periodo BCB:", PERIODO_TAXAS_BCB)

    print("PLATAFORMA:", plataforma)

    print("Desconto Pix medio da amostra:", formatar_percentual(desconto_medio))

    print("Preco estimado no Pix:", formatar_moeda(preco_pix))

    print("\nCOMPARACAO DOS PRAZOS")

    print(f"{'Parcelas':>9} {'Valor mensal':>18} {'Total parcelado':>20} {'Diferenca vs Pix':>19}")

    print("-" * 75)



    for quantidade in range(1, limite_parcelas + 1):

        parcela = calcular_parcela_simulada(

            preco_base, entrada, taxa_banco, quantidade

        )

        total = round(entrada + parcela * quantidade, 2)

        diferenca_pix = round(total - preco_pix, 2)



        registro = {

            "plataforma": plataforma,

            "banco": banco,

            "parcelas": quantidade,

            "parcela": parcela,

            "total": total,

            "preco_pix": preco_pix,

            "diferenca_pix": diferenca_pix,

            "cabe_orcamento": limite_mensal <= 0 or parcela <= limite_mensal

        }

        resultados.append(registro)



        print(

            f"{quantidade:>9} {formatar_moeda(parcela):>18} "

            f"{formatar_moeda(total):>20} {formatar_moeda(diferenca_pix):>19}"

        )



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

                "Primeiro prazo que cabe no orcamento:",

                primeiro_compativel["parcelas"], "parcelas; parcela de",

                formatar_moeda(primeiro_compativel["parcela"]),

                "e total de", formatar_moeda(primeiro_compativel["total"])

            )



    return resultados





# Autor: [Nome do integrante responsavel]

def executar_simulacao_avulsa():

    """Simula smartphone livre usando banco escolhido e loja escolhida."""

    print("\nSIMULACAO AVULSA - TAXA DO BANCO + DESCONTO DA PLATAFORMA")

    modelo = ler_texto("Nome/modelo do smartphone: ")

    preco_base = ler_float("Preco-base normal no cartao (R$): ", 0.0, False)

    entrada = ler_float("Entrada (R$; digite 0 se nao houver): ", 0.0, True)



    if entrada >= preco_base:

        print("A entrada deve ser menor que o preco-base.")

        return



    banco = selecionar_banco_cartao()

    plataforma = selecionar_plataforma()

    limite_parcelas = ler_inteiro(

        "Quantidade maxima de parcelas a analisar (1 a 48): ", 1, 48

    )

    limite_mensal = ler_float(

        "Limite que pode pagar por mes (0 se nao quiser filtrar): R$ ",

        0.0,

        True

    )



    print("\nProduto:", modelo)

    print("Preco-base B:", formatar_moeda(preco_base))

    print("Entrada:", formatar_moeda(entrada))

    print("Banco selecionado:", banco)

    print("Plataforma selecionada:", plataforma)

    print("Prazos analisados: de 1 ate", limite_parcelas, "parcelas")



    resultados = simular_faixa_parcelas(

        plataforma, banco, preco_base, entrada,

        limite_parcelas, limite_mensal

    )



    if len(resultados) == 0:

        print("Simulacao nao realizada. Verifique as taxas e descontos cadastrados.")

        return



    menor_total = resultados[0]

    menor_parcela = resultados[0]



    for registro in resultados[1:]:

        if registro["total"] < menor_total["total"]:

            menor_total = registro

        if registro["parcela"] < menor_parcela["parcela"]:

            menor_parcela = registro



    print("\nMENOR CUSTO TOTAL ENTRE OS PRAZOS ANALISADOS:")

    print(

        menor_total["parcelas"], "parcelas de",

        formatar_moeda(menor_total["parcela"]),

        "- total", formatar_moeda(menor_total["total"])

    )

    print("MENOR PRESTACAO MENSAL:")

    print(

        menor_parcela["parcelas"], "parcelas de",

        formatar_moeda(menor_parcela["parcela"]),

        "- total", formatar_moeda(menor_parcela["total"])

    )



    print("\nObservacoes metodologicas:")

    print("- A taxa e uma referencia media do BCB para a instituicao selecionada.")

    print("- A taxa real do contrato/cartao pode ser diferente.")

    print("- O desconto Pix e a media das ofertas pesquisadas na plataforma.")

    print("- A menor parcela mensal nao significa o menor custo total.")

    print("- Para comparar outra loja, repita a opcao 2 e altere a plataforma.")





# =====================================================================

# 6. PROJECAO ACADEMICA COM K (OPCAO 3)

# =====================================================================





# Autor: [Nome do integrante responsavel]

def calcular_parametros_k(k):

    """Calcula taxa mensal e prazo conforme as formulas do professor."""

    if not isinstance(k, int) or k < 0:

        raise ValueError("K deve ser um inteiro nao negativo.")

    taxa = (k % 5) + 1

    meses = (k % 6) + 6

    return taxa, meses





# Autor: [Nome do integrante responsavel]

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





# Autor: [Nome do integrante responsavel]

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





# Autor: [Nome do integrante responsavel]

def exibir_menu():

    """Mostra as quatro opcoes principais do sistema."""

    print("\n" + "=" * 66)

    print("COMPARADOR DE OFERTAS DE SMARTPHONES - PROJETO 15")

    print("=" * 66)

    print("1 - Comparar ofertas reais cadastradas (planilha futura)")

    print("2 - Simular parcelamento avulso (banco + plataforma)")

    print("3 - Fazer projecao hipotetica com K")

    print("0 - Sair")

    print("=" * 66)





# Autor: [Nome do integrante responsavel]

def executar_comparacao_real():

    """Executa a opcao 1 usando a base de ofertas reais cadastradas."""

    ofertas = carregar_ofertas_reais()

    if len(ofertas) == 0:

        print("A base de ofertas reais esta vazia.")

        return

    codigo = selecionar_modelo_real(ofertas)

    ofertas_modelo = buscar_ofertas_por_modelo(ofertas, codigo)

    exibir_comparacao_real(ofertas_modelo)





# Autor: [Nome do integrante responsavel]

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





# Autor: [Nome do integrante responsavel]

def executar_testes_basicos():

    """Executa verificacoes simples das funcoes matematicas do pre-codigo."""

    # Testes do parser de moeda brasileira.
    assert converter_valor_numerico("6767,50") == 6767.50
    assert converter_valor_numerico("R$ 6.767,50") == 6767.50

    # O nome da base de taxas deve ser o mesmo usado pela funcao de consulta.
    assert "Itaú" in AMOSTRAS_TAXAS_MENSAIS
    assert obter_media_taxa_banco("Itaú") == 9.91

    # Oferta anunciada sem juros: total parcelado igual ao preco-base do cartao.
    oferta_sem_juros = OFERTAS_REAIS[0]
    assert calcular_juros_reais(oferta_sem_juros) == 0.00
    assert calcular_juros_percentual(oferta_sem_juros) == 0.00

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



    # Teste da taxa implicita: R$ 1.000 financiados em 10 parcelas de R$ 110.

    taxa_estimada = calcular_taxa_implicita(1000.00, 0.00, 10, 110.00)

    assert taxa_estimada is not None and taxa_estimada > 0



    # Teste das taxas bancarias transcritas do BCB.

    assert obter_media_taxa_banco("Bradesco") == 9.02

    assert obter_media_taxa_banco("Nubank") == 9.06

    assert obter_media_taxa_banco("Itaú") == 9.91

    assert obter_media_taxa_banco("Santander") == 10.16

    assert obter_media_taxa_banco("Caixa Econômica Federal") == 8.62



    # Teste das medias de descontos informadas pelo grupo.

    assert round(obter_media_desconto("Amazon"), 2) == 17.33

    assert round(obter_media_desconto("Magazine Luiza"), 2) == 15.33

    assert round(obter_media_desconto("Mercado Livre"), 2) == 19.00



    # Teste de simulacao avulsa: taxa do banco e desconto da loja sao separados.

    teste_avulso = simular_condicao_plataforma(

        "Amazon", "Itaú", 3000.00, 300.00, 12

    )

    assert teste_avulso is not None

    assert teste_avulso["taxa_banco"] == 9.91

    assert round(teste_avulso["desconto_medio"], 2) == 17.33



    print("Todos os testes basicos foram aprovados.")





if __name__ == "__main__":

    main()
