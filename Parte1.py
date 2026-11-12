def cadastrar_oferta():
    nome = input('Informe o nome da loja:')
    produto = input('Informe o produto:')
    preco = float(input('Informe o preço do produto:'))
    entrada = float(input('Valor da 1° parcela:'))
    quant_parcelas = int(input('Número de parcelas:'))
    valor_parcelas = float(input('Informe o valor de cada parcela:'))

    return {
        'nome': nome,
        'produto': produto,
        'preco': preco,
        'entrada': entrada,
        'quant_parcelas': quant_parcelas,
        'valor_parcelas': valor_parcelas,
    }

def menu():
    oferta = None

    while True:
        print('\n--- MENU ---')
        print('1. Cadastrar oferta')
        print('2. Consultar informações')
        print('0. Sair')

        opcao = input('Escolha uma opção:')

        if opcao == '1':
            oferta = cadastrar_oferta()
            print('Oferta cadastrada!')

        elif opcao == '2':                            #[IA]
            if oferta is None:
                print('Nenhuma oferta cadastrada ainda')
            else:
                print(f"\nLoja: {oferta['nome']}")
                print(f"Produto: {oferta['produto']}")
                print(f"Preço: R$ {oferta['preco']:.2f}")
                print(f"Entrada: R$ {oferta['entrada']:.2f}")
                print(f"Parcelas: {oferta['quant_parcelas']}x de R$ {oferta['valor_parcelas']:.2f}")                                  #[IA]

        elif opcao == '0':
            print('Saindo...')
            break

        else:
            print('Opção inválida')

menu()
