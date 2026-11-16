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
    entrada = ler_float_positivo('Valor da entrada (0 se não tiver): R$', permitir_zero=True)
    parcelas = ler_int_positivo('Número de parcelas:')
    valor_parcela = ler_float_positivo('Informe o valor de cada parcela: R$')

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

menu()

