import string
import errno
import os
import sys


def obtem_projeto_mes(arquivo):
    """
    :param arquivo: uma string com o nome do arquivo para abrir
    :return: um dicionario no qual a chave eh o nome do projeto e o valor eh o mes (no formato AAAAMM) em que foi criado
    """
    print 'entrando na funcao', sys._getframe().f_code.co_name
    arquivo_criacao_projetos = open(arquivo, 'r')
    projeto_mes = {}
    for linha in arquivo_criacao_projetos:
        tokens = string.split(linha.rstrip(), ',')
        projeto_mes[tokens[0]] = tokens[1]

    return projeto_mes


def obter_linguagens(arquivo):
    """
    :param arquivo: uma string com o nome do arquivo para abrir
    :return: um dicionario no qual a chave eh o nome do projeto e o valor eh o mes (no formato AAAAMM) em que foi criado
    """
    print 'entrando na funcao', sys._getframe().f_code.co_name
    arquivo_linguagens = open(arquivo, 'r')
    retorno = []
    for linha in arquivo_linguagens:
        if not linha.startswith('#'):
            retorno.append(linha.rstrip())

    return retorno


def obtem_projetos_linguagens(arquivo):
    """
    :param arquivo: arquivo a ser aberto, contendo em cada linha, separado por virgulas, o projeto e suas linguagens
    :return: um dicionario com o nome do projeto como chave e uma lista com as linguagens que ele usa como valor
    """
    print 'entrando na funcao', sys._getframe().f_code.co_name
    arquivo_linguagens = open(arquivo, 'r')
    projetos_linguagens = {}
    for linha in arquivo_linguagens:
        tokens = string.split(linha.rstrip(), ',')
        if (len(tokens) > 1) and projeto_mes.has_key(tokens[0]):
            # pega todas as linguagens do projeto da lista de tokens, desprezando a primeira posicao, que eh o nome
            # do projeto
            projetos_linguagens[tokens[0]] = tokens[1:]

    return projetos_linguagens


def filtra_projetos(projetos_mes, projetos_linguagens, universo):
    """
    :param projetos_mes: um dicionario no qual a chave eh o nome do projeto e o valor eh o mes (no formato AAAAMM) em
    que foi criado
    :param projetos_linguagens: um dicionario com o nome do projeto como chave e uma lista com as linguagens que ele
    usa como valor
    :param universo: uma lista com as linguagens a serem consideradas
    :return: um subconjunto do dicionario projetos_mes, contendo apenas os projetos que usam linguagens presentes no
    universo
    """
    print 'entrando na funcao', sys._getframe().f_code.co_name
    # coisa linda demais essa linha de codigos
    return {k:v for (k, v) in projetos_mes.iteritems() if k in projetos_linguagens and not set(projetos_linguagens[k]).isdisjoint(universo)}


def obter_projetos_usuarios(arquivo):
    """
    :param arquivo: o arquivo a ser aberto
    :return: um dicionario em que a chave eh o nome do projeto e o valor eh uma lista dos usuarios que participam dele
    """
    print 'entrando na funcao', sys._getframe().f_code.co_name
    arquivo_usuarios = open(arquivo, 'r')
    retorno = {}
    for linha in arquivo_usuarios:
        tokens = string.split(linha.rstrip(), ',')
        nome_projeto = tokens[0]
        retorno[nome_projeto] = tokens[1:]

    return retorno


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
    print 'entrando na funcao', sys._getframe().f_code.co_name
    chaves_projetos_mes = projetos_mes.keys()
    lista_usuarios = []
    for projeto in chaves_projetos_mes:
        for usuario in projetos_usuarios[projeto]:
            if usuario not in lista_usuarios:
                lista_usuarios.append(usuario)

    return len(lista_usuarios)


def criar_diretorio_se_nao_existe(arquivo):
    print 'entrando na funcao', sys._getframe().f_code.co_name
    if not os.path.exists(arquivo):
        try:
            os.makedirs(arquivo)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def obtem_projetos_no_mes(projetos_mes):
    """
    organiza o dicionario para que a partir de um mes, saber-se quais projetos foram criados naquele mes
    :param projetos_mes: dicionario com chave sendo o nome do projeto e valor o mes de sua criacao
    :return: um dicionaro com chave o mes de criacao e valor uma lista com os nomes dos projetos criados naquele mes
    """
    print 'entrando na funcao', sys._getframe().f_code.co_name
    retorno = {}
    for chave, valor in projetos_mes.iteritems():
        if retorno.has_key(valor):
            retorno[valor].append(chave)
        else:
            lista = [chave]
            retorno[valor] = lista

    return retorno


def preenche_espacos_vazios(projetos_no_mes):
    """
    preenche espacos vazios no dicionario, inserindo meses que antes nao existiam, como chave, e como valor listas
    vazias
    :param projetos_no_mes: dicionario em que a chave eh o mes e o valor uma lista com os projetos criados naquel mes
    :return: a lista projeto mes com os buracos de meses preenchidos
    """
    print 'entrando na funcao', sys._getframe().f_code.co_name
    chaves_ordenadas = projetos_no_mes.keys()
    chaves_ordenadas.sort()
    limite_iteracao = len(chaves_ordenadas)
    i = 0
    while i < limite_iteracao:
        if i + 1 < len(chaves_ordenadas):
            if chaves_ordenadas[i] != '' and proximo_mes(chaves_ordenadas[i]) != chaves_ordenadas[i + 1]:
                projetos_no_mes[proximo_mes(chaves_ordenadas[i])] = []
                chaves_ordenadas = projetos_no_mes.keys()
                chaves_ordenadas.sort()
                limite_iteracao += 1
        i += 1


def proximo_mes(valor):
    """
    identifica qual seria o mes seguinte baseado no mes passado como parametro
    :param valor: o mes (no formato AAAAMM) a ter seu proximo mes identificado
    :return: o proximo mes em relacao ao mes passado como parametro
    """
    # print 'entrando na funcao', sys._getframe().f_code.co_name
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
    print 'entrando na funcao', sys._getframe().f_code.co_name
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


def integra_suc_infec(linguagem, projetos_usuarios, projetos_linguagens, projetos_mes, universo):
    """
    :param linguagem: linguagem de interesse
    :param projetos_usuarios: dicionario com chave o nome do projeto e valor uma lista com seus participantes
    :param projetos_linguagens: dicionario com chave o nome do projeto e valor uma lista com suas linguagens
    :param projetos_mes: dicionario com chave o nome do projeto e valor o seu mes de criacao (AAAAMM)
    :param universo: lista com nomes das linguagens de programacao que compoem o universo de linguagens relevantes para
    analise
    :return:
    """
    print 'entrando na funcao', sys._getframe().f_code.co_name
    suc = []  # cada item da lista representa como a populacao de suscetiveis evoluiu
    infec = []  # cada item da lista representa como a populacao de infectados evoluiu
    usuarios_infectados = []  # usuarios que ja foram contabilizados como infectados. evita contar o mesmo usuario duas vezes

    suc_inicial = conta_usuarios(projetos_mes, projetos_usuarios)

    projetos_no_mes = obtem_projetos_no_mes(projetos_mes)
    preenche_espacos_vazios(projetos_no_mes)
    chaves_projeto_mes = projetos_no_mes.keys()
    chaves_projeto_mes.sort()

    tupla_suc_inicial = ('AAAAMM', '000000', suc_inicial)
    suc.append(tupla_suc_inicial)

    tupla_infec_inicial = ('AAAAMM', '000000', 0)
    infec.append(tupla_infec_inicial)

    infectados = 0
    suscetiveis = suc_inicial

    novos_infectados = 0
    for chave_mes in chaves_projeto_mes:
        projetos = projetos_no_mes[chave_mes]
        for projeto in projetos:
            if linguagem in projetos_linguagens[projeto]:  # checa se o projeto usa a linguagem sendo investigada
                usuarios = projetos_usuarios[projeto]
                for usuario in usuarios:
                    if usuario not in usuarios_infectados:
                        novos_infectados += 1
                        usuarios_infectados.append(usuario)

        infectados += novos_infectados
        suscetiveis -= novos_infectados
        novos_infectados = 0

        tupla1 = (corrige_ano_mes(chave_mes), chave_mes, suscetiveis)
        tupla2 = (corrige_ano_mes(chave_mes), chave_mes, infectados)
        suc.append(tupla1)
        infec.append(tupla2)

    return suc, infec


projeto_mes = obtem_projeto_mes('created2')
projetos_linguagens = obtem_projetos_linguagens('programming-language')
projetos_usuarios = obter_projetos_usuarios('foaf-nick')

# linguagens a considerar no universo de possiveis de projetos OO
with open('linguagens-relacionadas-java.txt') as arquivo_universo:
    linguagens_universo = arquivo_universo.read().splitlines()

# filtra os projetos para incluir apenas aqueles que usam linguagens que estao no universo
projeto_mes = filtra_projetos(projeto_mes, projetos_linguagens, linguagens_universo)

linguagens = obter_linguagens('linguagens.txt')

for linguagem in linguagens:
    suc, infec = integra_suc_infec(linguagem, projetos_usuarios, projetos_linguagens, projeto_mes, linguagens_universo)

    diretorio = os.path.dirname(os.path.abspath(__file__)) + '/' + linguagem

    # vai criar o diretorio para salvar os arquivos caso ele nao exista
    criar_diretorio_se_nao_existe(diretorio)

    try:
        arquivo_saida = open(diretorio + '/saida_' + linguagem + '_suc.txt', 'w')
        for i in range(len(suc)):
            arquivo_saida.write(str(i) + '   ' + str(suc[i][0]) + '   ' + str(suc[i][1]) + '   ' + str(suc[i][2]) + '\n')
            arquivo_saida.flush()
    except TypeError:
        print 'i: ' + str(i) + ', suc[i]: ' + str(suc[i])

    try:
        arquivo_saida = open(diretorio + '/saida_' + linguagem + '_infec.txt', 'w')
        for i in range(len(infec)):
            arquivo_saida.write(str(i) + '   ' + str(infec[i][0]) + '   ' + str(infec[i][1]) + '   ' + str(infec[i][2]) + '\n')
            arquivo_saida.flush()
    except TypeError:
        print 'i: ' + str(i) + ', infec[i]: ' + str(infec[i])
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