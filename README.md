Projeto 15 — Comparador de Ofertas e Simulador de Parcelamento
Relatório técnico do Integrante 3
Responsabilidade: juros compostos, testes, integração e documentação técnica.
Disciplina: Programação I — Python
K utilizado nesta versão: xx — confirmar o valor definitivo com o cálculo das matrículas do grupo.
1. Objetivo da minha parte
A contribuição do Integrante 3 consiste em implementar a projeção acadêmica de juros compostos definida pelo parâmetro K, verificar o comportamento dessa simulação em diferentes situações e testar a integração com as funcionalidades construídas pelos Integrantes 1 e 2.

A projeção não representa uma oferta real de uma loja ou a taxa contratual de um cartão. Trata-se de uma simulação matemática definida pelo exercício, que parte de um capital informado pelo usuário e aplica a taxa mensal e o prazo derivados de K.
2. Cálculo dos parâmetros K
O projeto utiliza as fórmulas:
- K do grupo: valor calculado a partir dos dois últimos dígitos de matrícula, conforme a regra estabelecida no enunciado.
- Taxa mensal: (K % 5) + 1 por cento.
- Prazo: (K % 6) + 6 meses.
Para o valor atualmente usado pelo grupo, K = 10:
- Taxa mensal: (10 % 5) + 1 = 1%.
- Prazo: (10 % 6) + 6 = 10 meses.
Caso a conferência das matrículas resulte em outro K, basta atualizar a variável global K. A taxa e o prazo serão recalculados pela função calcular_parametros_k.
3. Funcionamento da simulação de juros compostos
A função simular_juros_compostos(capital, taxa_mensal, meses) recebe três parâmetros: capital inicial, taxa mensal percentual e quantidade de meses.

O saldo é atualizado mês a mês por meio de um laço for. A cada repetição, o programa:
1. guarda o saldo anterior;
2. calcula o novo saldo aplicando a taxa sobre o saldo atualizado;
3. calcula os juros daquele mês pela diferença entre o novo saldo e o anterior;
4. calcula os juros acumulados pela diferença entre o saldo atual e o capital inicial;
5. registra os valores em uma lista de dicionários.
A implementação utiliza for, não utiliza bibliotecas financeiras, não utiliza operador de potência e não utiliza pow(). Os valores são arredondados para duas casas na apresentação do histórico; o saldo interno mantém a precisão entre os meses para evitar arredondamento acumulado a cada etapa.
4. Integração com o programa do grupo
A função executar_projecao_k() reutiliza funções que já existem no programa principal:
Função compartilhada	Responsabilidade	Integrante responsável
ler_texto()	Receber o modelo do smartphone e impedir texto vazio	Integrante 1
ler_float()	Receber o preço-base e validar o número	Integrante 1
formatar_moeda()	Exibir valores no padrão brasileiro	Integrante 1
formatar_percentual()	Exibir a taxa com duas casas decimais	Estrutura compartilhada
calcular_parametros_k()	Derivar taxa e prazo a partir de K	Integrante 3
simular_juros_compostos()	Calcular a evolução mensal	Integrante 3


No menu principal, a opção 3 deve chamar executar_projecao_k(). Essa chamada já aparece no código integrado revisado. Não é necessário criar outro menu nem duplicar as funções de entrada e formatação.

Cuidado na integração: mantenha apenas uma variável global K no arquivo principal. Copie as funções do Integrante 3 para o programa do grupo, substituindo as versões anteriores dessas mesmas funções. A função de testes de integração deve ser executada somente depois que as funções dos três integrantes estiverem definidas.
Passos para integrar e executar os testes
1. Abra o arquivo principal do grupo.
2. Substitua a seção antiga da projeção com K pelas funções calcular_parametros_k, simular_juros_compostos e executar_projecao_k do arquivo parte_integrante3_final.py. Mantenha somente uma definição de K.
3. Copie também as funções auxiliares _i3_numero_finito, _i3_esperar_value_error e executar_testes_integracao para o arquivo principal. Coloque executar_testes_integracao depois das funções dos Integrantes 1 e 2, pois os testes chamam essas funções.
4. Confirme que a opção 3 do menu chama executar_projecao_k().
5. Durante a validação, deixe temporariamente o final do arquivo assim:
if __name__ == "__main__":
    executar_testes_integracao()
    main()
6. Execute o programa. O terminal deve mostrar Resultado: 12 de 12 grupos de testes aprovados. antes de exibir o menu. Depois da validação, o grupo pode manter a chamada dos testes para demonstração ou removê-la do fluxo normal, preservando a função no código para repetir a verificação quando necessário.
5. Testes automatizados
Foi criada a função executar_testes_integracao(), com 12 grupos de testes. Ela verifica a lógica de K, a evolução dos juros, entradas inválidas e chamadas entre as três partes do sistema.
Nº	Cenário testado	Resultado esperado	Resultado da execução
1	K atual igual a 10	Taxa de 1% e prazo de 10 meses	Aprovado
2	K igual a 0 e K igual a 5	Parâmetros calculados conforme as fórmulas	Aprovado
3	K negativo, decimal ou booleano	Rejeição com ValueError	Aprovado
4	Simular R$ 1.000,00 por 10 meses	Dez registros mensais	Aprovado
5	Primeiro mês, taxa de 1%	Saldo de R$ 1.010,00	Aprovado
6	Segundo mês, taxa de 1%	Saldo de R$ 1.020,10	Aprovado
7	Terceiro mês, taxa de 1%	Saldo de R$ 1.030,30 e juros acumulados de R$ 30,30	Aprovado
8	Décimo mês, taxa de 1%	Montante de R$ 1.104,62 e juros acumulados de R$ 104,62	Aprovado
9	Taxa igual a zero	Saldo permanece igual ao capital	Aprovado
10	Capital zero, taxa negativa, prazo zero, NaN ou infinito	Rejeição de entradas inválidas	Aprovado
11	Integração com leitura monetária e taxa bancária	Converter R$ 6.767,50 e consultar a taxa de Itaú	Aprovado
12	Integração com ofertas e simulação financeira	Oferta sem juros, parcela sem juros e simulação banco/plataforma	Aprovado


Resultado verificado nesta versão: 12 de 12 grupos de testes aprovados. O teste foi executado com as funções do Integrante 3 inseridas no espaço de nomes do programa integrado revisado.

Se o K definitivo for alterado, atualize a expectativa do teste 1 para corresponder à nova taxa e ao novo prazo.
6. Testes manuais e rastreamento
Teste manual 1 — entrada válida
Entradas:
- Modelo: Redmi Note 15
- Preço-base: 1000
- K: 10
Parâmetros calculados: taxa de 1% ao mês e prazo de 10 meses.
Mês	Saldo	Juros do mês	Juros acumulados
1	R$ 1.010,00	R$ 10,00	R$ 10,00
2	R$ 1.020,10	R$ 10,10	R$ 20,10
3	R$ 1.030,30	R$ 10,20	R$ 30,30
4	R$ 1.040,60	R$ 10,30	R$ 40,60
5	R$ 1.051,01	R$ 10,41	R$ 51,01
6	R$ 1.061,52	R$ 10,51	R$ 61,52
7	R$ 1.072,14	R$ 10,62	R$ 72,14
8	R$ 1.082,86	R$ 10,72	R$ 82,86
9	R$ 1.093,69	R$ 10,83	R$ 93,69
10	R$ 1.104,62	R$ 10,94	R$ 104,62


Conclusão: com capital inicial de R$ 1.000,00, taxa de 1% ao mês e dez meses, o montante final é R$ 1.104,62. Os juros acumulados são R$ 104,62.
Teste manual 2 — validação de entradas
Sequência de entradas simulada:
1. Modelo vazio: o programa informa que o campo não pode ficar vazio e solicita novamente.
2. Modelo informado: Redmi Note 15.
3. Preço digitado como abc: o programa informa que o valor numérico é inválido e solicita novamente.
4. Preço digitado como 0: o programa informa que o valor está fora do limite permitido e solicita novamente.
5. Preço digitado como 1000: valor aceito; a projeção é executada normalmente.
Conclusão: os campos obrigatórios e os limites numéricos impedem que dados inválidos iniciem a simulação. Após a correção das entradas, o resultado final permanece R$ 1.104,62.
7. Problemas encontrados na revisão e correções
A revisão de integração apontou os seguintes problemas. Os dois primeiros eram defeitos de comportamento no código anterior; o terceiro é uma proteção de validação acrescentada à implementação do Integrante 3.
Problema 1 — leitura de moeda no padrão brasileiro
Comportamento anterior: a leitura substituía vírgula por ponto diretamente. Uma entrada como 6.767,50 podia se transformar em 6.767.50, que não é um número reconhecido por float().

Correção: utilizar a função converter_valor_numerico() para remover o separador de milhar e converter a vírgula decimal. A entrada R$ 6.767,50 passa a ser interpretada como 6767.50.

Verificação: teste 11 aprovado.
Problema 2 — referência inadequada para calcular os juros da oferta
Comportamento anterior: o cálculo de acréscimo usava o preço à vista/Pix como referência. Isso misturava o desconto concedido no pagamento à vista com o custo financeiro do parcelamento.

Correção: calcular o acréscimo do parcelamento em relação ao preço-base normal no cartão, desde que esse preço esteja confirmado. O preço Pix continua disponível como comparação separada.

Verificação: a primeira oferta cadastrada, cujo total parcelado é igual ao preço-base do cartão, deve apresentar juros de R$ 0,00 e percentual de 0%.
Problema 3 — validação permissiva do parâmetro K
Comportamento anterior: em Python, valores booleanos também são considerados inteiros (bool é uma subclasse de int). Assim, True poderia ser aceito como K, embora não seja um número de matrícula válido.

Correção: rejeitar explicitamente valores booleanos, números decimais e números negativos. Na simulação, também são rejeitados capital ou taxa não finitos, capital igual ou inferior a zero, taxa negativa e prazo que não seja inteiro positivo.

Verificação: testes 3 e 10 aprovados.

Observação sobre um erro anterior de execução: foi relatado anteriormente um NameError relacionado ao nome da variável das taxas bancárias. Na versão do código anexada que foi revisada, a declaração e a função de consulta já utilizavam o mesmo nome com o sufixo _BANCO, portanto esse erro específico não foi reproduzido nessa cópia. A versão integrada revisada padroniza o nome da variável e das referências; o teste 11 verifica a consulta de uma taxa.
8. Limitações e cuidados
- O K igual a 10 deve ser confirmado pelo cálculo definitivo das matrículas do grupo e pela orientação do professor.
- A projeção com K é acadêmica e hipotética. Não deve ser apresentada como taxa real cobrada por uma loja, banco ou cartão.
- A taxa e o prazo dependem do K. Alterações no K exigem atualizar a expectativa de resultado do teste 1.
- A simulação não substitui o Custo Efetivo Total (CET) ou as condições contratuais de uma instituição financeira.
- As funções de entrada e formatação são compartilhadas com o Integrante 1. A função de testes integrados pressupõe que as três partes estejam no mesmo programa principal.
9. Checklist da entrega do Integrante 3
- [x] Função para calcular taxa e prazo a partir de K.
- [x] Simulação de juros compostos com laço for.
- [x] Sem bibliotecas financeiras, operador de potência ou pow().
- [x] Histórico mensal com saldo, juros do mês e juros acumulados.
- [x] Validação de dados da simulação.
- [x] Integração com as funções compartilhadas e com a opção 3 do menu.
- [x] 12 grupos de testes automatizados aprovados.
- [x] 2 rastreamentos manuais executados.
- [x] 3 problemas documentados com suas correções.
- [x] Relatório técnico da contribuição.
Antes da entrega final: confirmar o K, inserir os nomes dos integrantes, manter a função de testes no código e executar novamente os testes na versão final que será apresentada ao professor.
