import string
import errno
import os
# import copy
# import collections
# from string import Template
# from string import ascii_lowercase as al


class Contagem:
    """
    Define a contagem para uma linguagem.
    Seu atributo contagem_ano guarda um dicionario, cujas chaves sao um
    determinado mes (no formaro AAAAMM) e o valor a quantidade de projetos
    criados com aquela linguagem naquele mes
    """
    def __init__(self):
        self.linguagem = ''
        self.contagem_ano = {}

    def set_linguagem(self, param):
        self.linguagem = param

    def incrementa_contagem(self, data):
        if self.contagem_ano.has_key(data):
            self.contagem_ano[data] += 1
        else:
            self.contagem_ano[data] = 1

    def preenche_espacos_vazios(self):
        chaves_ordenadas = self.contagem_ano.keys()
        chaves_ordenadas.sort()
        limite_iteracao = len(chaves_ordenadas)
        for i in range(limite_iteracao):
            if i + 1 < len(chaves_ordenadas):
                if chaves_ordenadas[i] != '' and self.proximo(chaves_ordenadas[i]) != chaves_ordenadas[i + 1]:
                    self.contagem_ano[self.proximo(chaves_ordenadas[i])] = 0;
                    chaves_ordenadas = self.contagem_ano.keys()
                    chaves_ordenadas.sort();
                    limite_iteracao += 1

    def proximo(self, valor):
        ano_inteiro = int(valor[:4])
        mes_inteiro = int(valor[4:6])

        mes_inteiro += 1

        if mes_inteiro > 12:
            mes_inteiro = 1
            ano_inteiro += 1

        if mes_inteiro < 10:
            mes_string = '0' + str(mes_inteiro)
        else:
            mes_string = str(mes_inteiro)

        return str(ano_inteiro) + mes_string


def corrige_ano_mes(data):
    """
    altera a representacao do mes de AAAAMM para AAAA-MMM.
    :param data: mes no formato AAAAMM
    :return: mes no formato AAAA-MMM, ex: 201011 sera alterado para 2010-NOV
    """
    ano = data[:4]
    mes = ''
    if data.endswith('01'):
        mes = '-JAN'
    elif data.endswith('02'):
        mes = '-FEB'
    elif data.endswith('03'):
        mes = '-MAR'
    elif data.endswith('04'):
        mes = '-APR'
    elif data.endswith('05'):
        mes = '-MAY'
    elif data.endswith('06'):
        mes = '-JUN'
    elif data.endswith('07'):
        mes = '-JUL'
    elif data.endswith('08'):
        mes = '-AUG'
    elif data.endswith('09'):
        mes = '-SEP'
    elif data.endswith('10'):
        mes = '-OCT'
    elif data.endswith('11'):
        mes = '-NOV'
    elif data.endswith('12'):
        mes = '-DEC'

    return ano + mes


def conta_projetos_por_mes(projeto_mes, projetos_linguagens, universo):
    """
    realiza a contagem de projetos criados por mes
    :param projeto_mes: um dicionario com projetos por mes (nome do projeto -> mes de criacao)
    :param projetos_linguagens: dicionario onde a chave eh o nome do projeto e o valor uma lista com as linguagens do projeto
    :param universo: lista com as possiveis linguagens a considerar no universo de contagem
    :return: um docionario com a contagem de projetos por mes, independente de linguagem (mes -> quantidade de projetos criados naquele mes)
    mas respeitando o universo
    """
    contagem = Contagem()
    contagem.set_linguagem('todas')
    chaves = projeto_mes.keys()
    iteracao = 0
    for chave in chaves:
        if chave in projetos_linguagens: # and checa_universo(projetos_linguagens[chave], universo):
            contagem.incrementa_contagem(projeto_mes[chave])

        print iteracao
        iteracao += 1

    contagem.preenche_espacos_vazios()
    return contagem.contagem_ano


def checa_universo(lista_linguagens_projeto, universo):
    for linguagem in lista_linguagens_projeto:
        if linguagem in universo:
            return True

    return False


def obtem_projeto_mes(arquivo):
    """
    :param arquivo: uma string com o nome do arquivo para abrir
    :return: um dicionario no qual a chave eh o nome do projeto e o valor eh o mes (no formato AAAAMM) em que foi criado
    """
    arquivo_criacao_projetos = open(arquivo, 'r')
    projeto_mes = {}
    for linha in arquivo_criacao_projetos:
        tokens = string.split(linha.rstrip(), ',')
        projeto_mes[tokens[0]] = tokens[1]

    return projeto_mes


def conta_linguagem(arquivo, projeto_mes, universo):
    """
    :param arquivo: uma string com o nome do arquivo a ser aberto
    :param projeto_mes: um dicionario com a contagem de projetos por mes (nome do projeto -> mes de criacao)
    :return: um dicionario que armazena objetos do tipo Contagem a chave para o dicionario eh o nome da linguagem
    """
    arquivo_linguagens = open(arquivo, 'r')
    contagem_linguagem = {}
    for linha in arquivo_linguagens:
        tokens = string.split(linha.rstrip(), ',')
        if (len(tokens) > 1) and tokens[0] in projeto_mes:
            for x in range(1, len(tokens)):
                # if tokens[x] in universo: # checa se a linguagem esta no universo de linguagens a considerar
                if tokens[x] != '' and contagem_linguagem.has_key(tokens[x]):
                    contagem_linguagem[tokens[x]].incrementa_contagem(projeto_mes[tokens[0]])
                else:
                    conta = Contagem()
                    conta.set_linguagem(tokens[x])
                    conta.incrementa_contagem(projeto_mes[tokens[0]])
                    contagem_linguagem[tokens[x]] = conta;

    return contagem_linguagem


def obtem_projetos_linguagens(arquivo):
    """
    :param arquivo: arquivo a ser aberto, contendo em cada linha, separado por virgulas, o projeto e suas linguagens
    :return: um dicionario com o nome do projeto como chave e uma lista com as linguagens que ele usa como valor
    """
    arquivo_linguagens = open(arquivo, 'r')
    projetos_linguagens = {}
    for linha in arquivo_linguagens:
        tokens = string.split(linha.rstrip(), ',')
        if (len(tokens) > 1) and projeto_mes.has_key(tokens[0]):
            # pega todas as linguagens do projeto da lista de tokens, desprezando a primeira posicao, que eh o nome do projeto
            projetos_linguagens[tokens[0]] = tokens[1:]

    return projetos_linguagens


def integra_suc_infec(linguagem, projetos_usuarios, projetos_linguagens, projetos_mes, universo):
    """
    :param contagem_projetos_mes:
    :param contagem_linguagem:
    :param projetos_usuarios:
    :param projetos_linguagens:
    :param universo:
    :return:
    """
    suc = []
    infec = []

    suc_inicial = conta_usuarios(projetos_mes, projetos_usuarios)

    chaves_projeto_mes = contagem_projetos_mes.keys()
    chaves_projeto_mes.sort()

    chaves_contagem_linguagem = contagem_linguagem.contagem_ano.keys()
    chaves_contagem_linguagem.sort()

    suc.append(suc_inicial)
    infec.append(0)

    infectados = 0
    suscetiveis = 0

    # TODO mudar a semantica da contagem de infectados e suscetiveis para usar a ideia de contar os usuarios, nao os
    # os projetos. Desta forma, nao pode-se mais contar os projetos como sendo individuos infectados, mas o usuario em
    # si. Assim, quando um projeto for criado com a linguagem de interesse, todos os participantes daquele projeto
    # devem ser considerados infectados
    for chave_contagem_linguagem in chaves_contagem_linguagem:
        infectados += contagem_linguagem.contagem_ano[chave_contagem_linguagem]
        infec.append(infectados)
        suscetiveis -= contagem_linguagem.contagem_ano[chave_contagem_linguagem]
        suc.append(suscetiveis)

    return suc, infec


def conta_usuarios(projetos_mes, projetos_usuarios):
    """
    Conta a quantidade de usuarios que participam de projetos que utilizam linguagem no universo de interesse assumindo
    que o dicionario projetos_mes ja foi filtrado para conter apenas projetos que utilizam pelo menos uma linguagem
    no universo de linguagens de interesse
    :param projetos_mes: dicionario onde a chave eh o nome do projeto e o valor o mes de sua criacao
    :param projetos_usuarios: dicionario onde a chave eh o nome do projeto e o valor uma lista com os usuarios que
    participam desse projeto
    :return: a quantidade total de usuarios
    """
    chaves_projetos_mes = projetos_mes.keys()
    lista_usuarios = []
    for projeto in chaves_projetos_mes:
        for usuario in projetos_usuarios[projeto]:
            if usuario not in lista_usuarios:
                lista_usuarios.append(usuario)

    return len(lista_usuarios)


def criar_diretorio_se_nao_existe(arquivo):
    if not os.path.exists(arquivo):
        try:
            os.makedirs(arquivo)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def obter_projetos_usuarios(arquivo, projetos_mes, projetos_usuarios):
    """
    :param arquivo: o arquivo a ser aberto
    :return: um dicionario em que a chave eh o nome do projeto e o valor eh uma lista dos usuarios que participam dele
    """
    arquivo_usuarios = open('foaf-nick', 'r')
    retorno = {}
    for linha in arquivo_usuarios:
        tokens = string.split(linha.rstrip(), ',')
        nome_projeto = tokens[0]
        retorno[nome_projeto] = tokens[1:]

    return retorno


def filtra_projetos(projetos_mes, projetos_linguagens, universo):
    """
    :param projetos_mes: um dicionario no qual a chave eh o nome do projeto e o valor eh o mes (no formato AAAAMM) em que foi criado
    :param projetos_linguagens: um dicionario com o nome do projeto como chave e uma lista com as linguagens que ele usa como valor
    :param universo: uma lista com as linguagens a serem consideradas
    :return: um subconjunto do dicionario projetos_mes, contendo apenas os projetos que usam linguagens presentes no
    universo
    """
    # coisa linda demais essa linha de codigos
    return {k:v for (k, v) in projetos_mes.iteritems() if not set(projetos_linguagens[k]).isdisjoint(universo)}


# linguagens a considerar no universo de possiveis de projetos OO
with open('linguagens-relacionadas-java.txt') as arquivo_universo:
    linguagens_universo = arquivo_universo.read().splitlines()

projeto_mes = obtem_projeto_mes('created2')
projetos_linguagens = obtem_projetos_linguagens('programming-language')

# filtra os projetos para incluir apenas aqueles que usam linguagens que estao no universo
projeto_mes = filtra_projetos(projeto_mes, projetos_linguagens, linguagens_universo)

contagem_linguagem = conta_linguagem('programming-language', projeto_mes, linguagens_universo)
contagem_projetos_mes = conta_projetos_por_mes(projeto_mes, projetos_linguagens, linguagens_universo)
projetos_usuarios = obter_projetos_usuarios('foaf-nick')

arquivo_linguagens = open('linguagens.txt', 'r')
for linha in arquivo_linguagens:
    if not linha.startswith('#'):
        linguagem = linha.rstrip()
        contagem_linguagem[linguagem].preenche_espacos_vazios()
        chaves = contagem_linguagem[linguagem].contagem_ano.keys()

        suc, infec = integra_suc_infec(linguagem, projetos_linguagens, projeto_mes, linguagens_universo)

        diretorio = os.path.dirname(os.path.abspath(__file__)) + '/' + linguagem

        # vai criar o diretorio para salvar os arquivos caso ele nao exista
        criar_diretorio_se_nao_existe(diretorio)

        arquivo_saida = open(diretorio + '/saida_' + linguagem + '_suc.txt', 'w')
        for i in range(len(suc)):
            arquivo_saida.write(str(i) + '   ' + str(suc[i]) + '\n')
            arquivo_saida.flush()

        arquivo_saida = open(diretorio + '/saida_' + linguagem + '_infec.txt', 'w')
        for i in range(len(infec)):
            arquivo_saida.write(str(i) + '   ' + str(infec[i]) + '\n')
            arquivo_saida.flush()

        # arquivo_saida = open(diretorio + '/saida_' + linguagem + '_nasc.txt', 'w')
        # for i in range(len(nascimentos)):
            # arquivo_saida.write(str(i) + '   ' + str(nascimentos[i]) + '\n')
            # arquivo_saida.flush()

        # chaves.sort()

        # arquivo_saida = open('saida_' + linguagem + '_infec.txt', 'w')
        # acumulado = 0
        # for chave in chaves:
            # acumulado = acumulado + contagem_linguagem[linguagem].contagem_ano[chave]
            # arquivo_saida.write(corrige_ano_mes(chave) + '	' + str(contagem_linguagem[linguagem].contagem_ano[chave]) + '	' + str(acumulado) + '\n')