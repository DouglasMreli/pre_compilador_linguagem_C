"""
        Trabalho de implementação de um pré compilador para linguagem C
        Para inserção de bibliotecas e outros arquivos, os mesmo devem
        estar na mesma pasta que o arquivo
"""


def pre_compilador(nome_arq, novo_arq):
    arq = open(nome_arq, "r")

    lista_include = []
    dic_defines = {}
    achou_define = False
    eh_comentario = False

    for linha in arq:

        if eh_comentario:
            if '*/' in linha:
                nova_linha = comentario_bloco_final(linha)
                if nova_linha is not None:
                    novo_arq.write(nova_linha)
                eh_comentario = False
            else:
                continue
        elif '/*' in linha:
            nova_linha = comentario_bloco_inicio(linha)
            if nova_linha is not None:
                novo_arq.write(nova_linha)
            eh_comentario = True
        elif "//" in linha:
            nova_linha = comentario_linha(linha)
            novo_arq.write(nova_linha)
        elif "#" in linha:
            if "#define" in linha:
                linha_dividida = linha.split()
                if len(linha_dividida) == 3:
                    chave, valor = linha_dividida[1], linha_dividida[2]
                    dic_defines[chave] = valor
                    achou_define = True
            elif '#include' in linha:
                include(linha, novo_arq, lista_include)
            else:
                novo_arq.write(linha)
        else:
            if achou_define:
                print(linha)
                nova_linha = troca_valor(linha, dic_defines)
                novo_arq.write(nova_linha)
            else:
                novo_arq.write(linha.strip())

    arq.close()


def comentario_bloco_inicio(linha):
    indice_comentario = linha.strip().find('/*')
    if indice_comentario != 0:
        return linha[0: indice_comentario + 1].strip()
    else:
        return None


def comentario_bloco_final(linha):
    indice_comentario = linha.find('*/')
    if linha[indice_comentario + 2].strip() != '\n':
        return linha[indice_comentario + 2:].strip()
    else:
        return None


def comentario_linha(linha):
    indice_comentario = linha.find('//')
    if indice_comentario != 0:
        return linha[0: indice_comentario].strip()
    else:
        return None


def em_string(linha, palavra):
    indice_comeco = linha.find('"')
    indice_final = linha.find('"', indice_comeco+1)
    indice_palavra = linha.find(palavra)

    if indice_comeco < indice_palavra < indice_final:
        return True
    else:
        return False


def troca_valor(linha, dic):
    nova_linha = linha
    for elemento in dic:
        indice_palavra = linha.find(elemento)
        if indice_palavra != -1:
            eh_string = em_string(linha, elemento)
            if not eh_string:
                nova_linha = linha.replace(elemento, dic[elemento])
                print(nova_linha)
                print(linha)

    return nova_linha.strip()


def include(linha, novo_arq, lista):

    linha_dividida = linha.split()
    if linha_dividida[1].startswith('"'):
        nome_arq = linha_dividida[1].removeprefix('"').removesuffix('"')
    else:
        nome_arq = linha_dividida[1].removeprefix('<').removesuffix('>')

    if nome_arq not in lista:
        lista.append(nome_arq)
        arq_include = open(nome_arq, "r")
       # novo_arq.write(arq_include.read())
        arq_include.close()


arquivo = input("Digite o nome do arquivo.c a ser compilado: ")
arq_compilado = open("PreCompiled{}".format(arquivo), "w")
pre_compilador(arquivo, arq_compilado)
arq_compilado.close()
