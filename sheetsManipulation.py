from sheetsAPI import runSheets;
from style import printCabecalho, printColor, cor;
id = '1KfcO6J8_oLxTQIsdZ1l4XmBz-teP-pbpGoU7NnZa_KA'

class Gasto:
    def __init__(self, runSheetsReturn):
        self.gasto = runSheetsReturn[0]
        self.data = runSheetsReturn[1]
        self.valor = float(runSheetsReturn[2])
        self.categoria = runSheetsReturn[3]
        self.tipo = runSheetsReturn[4]
        self.parcelas = runSheetsReturn[5]
    def print(self):
        aux = ('{:<20}   {:<11}   {:>7}   {:<20}  {:<8}  {:<5}'.format(self.gasto,self.data, round(self.valor, 2),
                                                         self.categoria, self.tipo, self.parcelas))
        printColor(aux, color='vermelho')

class Entrada:
    def __init__(self, runSheetsReturn):
        self.entrada = runSheetsReturn[0]
        self.data = runSheetsReturn[1]
        self.valor = float(runSheetsReturn[2])
    def print(self):
        aux = '{:<20}   {:<11}   {:<7}'.format(self.entrada,self.data, round(self.valor, 2))
        printColor(aux, color='verde')

class Mes:
    def __init__(self, nome):
        self.nome = nome
        self.listaGastos = []
        self.listaEntradas = []
    def print(self):
        totalGastos = 0
        totalEntradas = 0
        printCabecalho(self.nome, color='azul')
        print(cor('Entradas'.center(80), color='verde', reverse=True))
        for item in self.listaEntradas:
             item.print()
             totalEntradas += item.valor
        print(cor('Saidas'.center(80), color='vermelho', reverse=True))
        for item in self.listaGastos:
            item.print()
            totalGastos += item.valor
        print(cor('Balanço Geral'.center(80), color='vermelho', reverse=True))
        printColor(f'Entradas: {totalEntradas}', color='verde')
        printColor(f'Gastos: {totalGastos}', color='vermelho')
        if totalEntradas > totalGastos:
            printColor(f'Balanço Total: {totalEntradas-totalGastos}', color='verde')
        else:
            printColor(f'Balanço Total: {totalEntradas-totalGastos}', color='vermelho')


def getData():
    listaMesesAux = ['Janeiro', 'Fevereiro', 'Marco', 'Abril', 
                  'Maio', 'Junho', 'Julho', 'Agosto',
                  'Setembro', 'Outubro', 'Novembro','Dezembro']
    listaMeses = []
    for mes in listaMesesAux:
        mesAux = Mes(mes)
        gastos = runSheets(id,mes, '!A2:G50')
        for i in gastos[0]:
            auxGasto = Gasto(i)
            mesAux.listaGastos.append(auxGasto)
        entradas = runSheets(id, mes,'!H2:J50')
        for i in entradas[0]:
            auxEntrada = Entrada(i)
            mesAux.listaEntradas.append(auxEntrada)
        listaMeses.append(mesAux)
    return listaMeses

if __name__ == '__main__':
    lista = getData()
    for i in lista:
        i.print()
    