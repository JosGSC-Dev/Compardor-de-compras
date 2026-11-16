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
