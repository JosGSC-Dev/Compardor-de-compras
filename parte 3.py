#módulo do terceiro integrante do grupo
k = 10

#Espécie de "banco de dados"
ofertas = [
    {
        "plataforma": "Magazine Luiza",
        "marca": "Samsung",
        "modelo": "Galaxy S26 256GB + Buds Core",
        "valor_vista": 4843.80,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 538.20,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 5382.00,
        "referencia_preco": "Pix",
        "observacao": "Oferta em combo com Galaxy Buds Core; nao e apenas o celular."
    },
    {
        "plataforma": "Mercado Livre",
        "marca": "Samsung",
        "modelo": "Galaxy S26 Ultra 256GB",
        "valor_vista": 6578.53,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 730.95,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 7309.48,
        "referencia_preco": "Pix",
        "observacao": "A tela informa total R$ 7.309,48; 10 x R$ 730,95 resulta em R$ 7.309,50."
    },
    {
        "plataforma": "Mercado Livre",
        "marca": "Samsung",
        "modelo": "Galaxy Z Flip 8 512GB",
        "valor_vista": 6699.00,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 643.89,
        "condicao": "Nao esclarecida",
        "total_anunciado": None,
        "referencia_preco": "Preco exibido; modalidade nao confirmada",
        "observacao": "A captura mostra R$ 6.699,00 e 12 x R$ 643,89, mas nao confirma a modalidade do preco-base nem ausencia de juros."
    },
    {
        "plataforma": "Magazine Luiza",
        "marca": "Samsung",
        "modelo": "Galaxy Z Flip 8 256GB",
        "valor_vista": 7739.10,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 859.90,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 8599.00,
        "referencia_preco": "Pix",
        "observacao": "A captura tambem mostra opcao alternativa de 21x R$ 409,48."
    },
    {
        "plataforma": "Magazine Luiza",
        "marca": "Samsung",
        "modelo": "Galaxy Z Flip 8 256GB",
        "valor_vista": 7739.10,
        "entrada": 0.00,
        "parcelas": 21,
        "valor_parcela": 409.48,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": None,
        "referencia_preco": "Pix",
        "observacao": "Opcao alternativa do mesmo anuncio; 21 x R$ 409,48 resulta em R$ 8.599,08."
    },
    {
        "plataforma": "Amazon",
        "marca": "Apple",
        "modelo": "iPhone 17 Pro Max 256GB Azul",
        "valor_vista": 9998.99,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 883.25,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 10599.00,
        "referencia_preco": "Preco exibido; anuncio menciona 5% off a vista",
        "observacao": "A tela mostra 12x R$ 883,25 e total parcelado de R$ 10.599,00."
    },
    {
        "plataforma": "Magazine Luiza",
        "marca": "Apple",
        "modelo": "iPhone 17 Pro Max 256GB Laranja",
        "valor_vista": 11494.05,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 1209.90,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 12099.00,
        "referencia_preco": "Pix",
        "observacao": "Vendido e entregue pela loja iPlace no marketplace Magalu."
    },
    {
        "plataforma": "Mercado Livre",
        "marca": "Apple",
        "modelo": "iPhone 17 Pro Max 512GB Azul",
        "valor_vista": 10799.00,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 1199.90,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 11999.00,
        "referencia_preco": "Pix",
        "observacao": "Configuracao de 512GB; nao e diretamente equivalente aos modelos de 256GB."
    },
    {
        "plataforma": "Amazon",
        "marca": "Xiaomi",
        "modelo": "POCO X8 Pro 256GB 8GB RAM",
        "valor_vista": 2474.80,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 224.24,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 2690.00,
        "referencia_preco": "Preco exibido / desconto a vista",
        "observacao": "12 x R$ 224,24 resulta em R$ 2.690,88; a tela informa total de R$ 2.690,00."
    },
    {
        "plataforma": "Amazon",
        "marca": "Xiaomi",
        "modelo": "Redmi Note 15 Pro 512GB 8GB RAM",
        "valor_vista": 2038.40,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 186.74,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 2240.00,
        "referencia_preco": "Preco exibido / desconto a vista",
        "observacao": "12 x R$ 186,74 resulta em R$ 2.240,88; a tela informa total de R$ 2.240,00."
    },
    {
        "plataforma": "Amazon",
        "marca": "Xiaomi",
        "modelo": "POCO C85 256GB 8GB RAM",
        "valor_vista": 1182.09,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 108.25,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 1299.00,
        "referencia_preco": "Preco exibido / desconto a vista",
        "observacao": "Total das parcelas confere com o total mostrado na captura."
    },
    {
        "plataforma": "Amazon",
        "marca": "Xiaomi",
        "modelo": "Redmi Note 15 256GB 8GB RAM",
        "valor_vista": 1534.25,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 134.62,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 1615.00,
        "referencia_preco": "Preco exibido / desconto a vista",
        "observacao": "12 x R$ 134,62 resulta em R$ 1.615,44; a tela informa total de R$ 1.615,00."
    },
    {
        "plataforma": "Magazine Luiza",
        "marca": "Xiaomi",
        "modelo": "Redmi 15C 256GB 8GB RAM",
        "valor_vista": 1274.15,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 149.90,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 1499.00,
        "referencia_preco": "Pix",
        "observacao": "Vendido por Atacado Import e entregue pelo Magalu."
    },
    {
        "plataforma": "Mercado Livre",
        "marca": "Xiaomi",
        "modelo": "Redmi Note 15 Pro 5G 256GB 8GB RAM",
        "valor_vista": 2625.00,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 262.50,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 2625.00,
        "referencia_preco": "Preco exibido",
        "observacao": "A captura mostra modalidade de parcelamento sem juros e 10 x R$ 262,50."
    },
    {
        "plataforma": "Mercado Livre",
        "marca": "Xiaomi",
        "modelo": "POCO C85 4G 256GB 8GB RAM",
        "valor_vista": 1278.99,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 139.56,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 1395.55,
        "referencia_preco": "Menor preco exibido; modalidade nao confirmada",
        "observacao": "A tela separa o menor preco de R$ 1.278,99 da opcao parcelada de 10 x R$ 139,56. Multiplicacao resulta em R$ 1.395,60."
    },
    {
        "plataforma": "Mercado Livre",
        "marca": "Xiaomi",
        "modelo": "Redmi Note 17 Pro 5G 256GB 8GB RAM",
        "valor_vista": 2469.00,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 261.00,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 2610.00,
        "referencia_preco": "Preco exibido",
        "observacao": "Modelo conforme nome exibido na captura; confirmar identificacao do produto no link original."
    },
    {
        "plataforma": "Mercado Livre",
        "marca": "Xiaomi",
        "modelo": "POCO X8 Pro 512GB 12GB RAM",
        "valor_vista": 2865.00,
        "entrada": 0.00,
        "parcelas": 10,
        "valor_parcela": 325.50,
        "condicao": "Sem juros (anuncio)",
        "total_anunciado": 3255.00,
        "referencia_preco": "Pix",
        "observacao": "A captura exibe 10 x R$ 325,50 no quadro de parcelamento sem juros. Configuracao 512GB/12GB."
    },
    {
        "plataforma": "Mercado Livre",
        "marca": "Xiaomi",
        "modelo": "Redmi 17 256GB",
        "valor_vista": 1849.00,
        "entrada": 0.00,
        "parcelas": 12,
        "valor_parcela": 177.72,
        "condicao": "Nao esclarecida",
        "total_anunciado": None,
        "referencia_preco": "Preco exibido; modalidade nao confirmada",
        "observacao": "A captura mostra 12 x R$ 177,72, mas nao identifica claramente se ha juros."
    }
] #Estruturadoa partir de um arquivo csv, este feito com auxílio da IA, de dados coletados manualmente.

#====================================================================
#                 FUNÇÕES DE CÁLCULO E COMPARAÇÃO
#====================================================================

def calcular_parametros_k(k):
    #validar o k calculador anteriomente
    if not isinstance(k, int) or k < 0:
        raise ValueError("O valor de k deve ser um inteiro não negativo.")

    taxa = (k % 5) + 1
    meses = (k % 6) + 1
    return taxa, meses

#simular os juros compostos de acordo com os meses
def simular_juros_compostos(valor, taxa, meses):
    #uso de laços for, sem ** e pow()
    if valor < 0:
        raise ValueError("O valor não pode ser negativo!")
    if taxa < 0:
        raise ValueError("A taxa não pode ser negativa!")
    if not isinstance(meses, int) or meses < 0:
        raise ValueError("O prazo (meses) deve ser um inteiro não negativo.")

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
            "juros_acumulados": juros_acumulados
        })

        return resultados

#compara o valor inicial + o total
def calcular_total_prazo(oferta):
    """Compara a entrada + (numero de parcelas X valor de cada parcela)."""
    return round(
        oferta["entrada"] + oferta["parcelas"] * oferta["valor_parcela"], 
        2
    )

#compara o valor, o total parcelado e a projecao hipotetica com o valor k
def calcular_comparativo(oferta, taxa, meses):
    total_prazo = calcular_total_prazo(oferta)
    diferenca = round(total_prazo - oferta["valor_vista"], 2)

    if oferta["valor_vista"] > 0:
        percentual = (diferenca / oferta["valor_vista"]) * 100
    else:
        percentual = 0.0

    simulacao = simular_juros_compostos(oferta["valor_vista"], taxa, meses)
    montante_k = simulacao[-1]["saldo"]
    juros_k = montante_k - oferta["valor_vista"]

    return{
        "total_prazo": total_prazo,
        "diferenca": diferenca,
        "percentual": percentual,
        "montante_k": montante_k,
        "juros_k": juros_k
    }


#====================================================================
#                 FUNCOES DE FORMATACAO E EXIBICAO
#====================================================================

#exibe valores em reais (moedas)
def formatar_moeda(valor):
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R${texto}"

#formata um percentual com duas casas decimais
def formatar_percentual(valor):
    return f"{valor:.2f}%".replace(".", ",")

#exibição das ofertas por marcas