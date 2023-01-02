dictColors = {
    'preto': '\033[1;30m',
    'cinza-claro':  '\033[1;37m',
    'cinza-escuro':  '\033[1;90m',
    'vermelho':  '\033[1;91m',
    'verde':  '\033[1;92m',
    'amarelo':  '\033[1;93m',
    'azul':  '\033[1;94m',
    'magenta':  '\033[1;95m',
    'cyan':  '\033[1;96m',
    'branco':  '\033[1;97m'
}

def cor(texto, color=None, reverse=False, bold=False):
    if color in dictColors.keys():
        texto = dictColors[color]+texto
    if bold:
        texto = "\033[;1m"+texto
    if reverse:
        texto = "\033[;7m"+texto
    return texto+"\033[0;0m"

def printCabecalho(texto, tam_cab=1, color=None, reverse=False):
    for i in range(1+tam_cab*2):
        if i == tam_cab:
            print(cor(f'|{str(texto).center(78)}|', color=color, reverse=reverse))
        else:
            print(cor(f"{'-'*80}", color=color, reverse=reverse))
        
def printColor(texto, color=None, reverse=False, bold=False):
    print(cor(texto=texto, color=color, reverse=reverse, bold=bold))