from style import*

dictionaryMeses = {
    1: 'Janeiro', 'Janeiro' : 1,
    2: 'Fevereiro', 'Fevereiro' : 2,
    3: 'Marco', 'Marco' : 3,
    4: 'Abril', 'Abril' : 4,
    5: 'Maio', 'Maio' : 5,
    6: 'Junho', 'Junho' : 6,
    7: 'Julho', 'Julho' : 7,
    8: 'Agosto', 'Agosto' : 8,
    9: 'Setembro', 'Setembro' : 9,
    10: 'Outubro', 'Outubro' : 10,
    11: 'Novembro', 'Novembro' : 11,
    12: 'Dezembro', 'Dezembro' : 12
}



class Gasto:
    def __init__(self, getSheetsReturn):
        self.gasto = getSheetsReturn[0]
        self.data = getSheetsReturn[1]
        self.valor = float(getSheetsReturn[2])
        self.categoria = getSheetsReturn[3]
        self.tipo = getSheetsReturn[4]
        self.parcelas = getSheetsReturn[5]
        self.proprietary = getSheetsReturn[6]
    def print(self):
        aux = ('{:<20} {:<11}  {:>7} {:<20} {:<8} {:<5}'.format(self.gasto,self.data, round(self.valor, 2),
                                                         self.categoria, self.tipo, self.parcelas))
        printColor(aux, color='vermelho')
    def getUpdate(self):
        return [self.gasto, self.data, self.valor, self.categoria, self.tipo, self.parcelas, self.proprietary]

class Entrada:
    def __init__(self, getSheetsReturn):
        self.entrada = getSheetsReturn[0]
        self.data = getSheetsReturn[1]
        self.valor = float(getSheetsReturn[2])
    def print(self):
        aux = '{:<20}   {:<11}   {:<7}'.format(self.entrada,self.data, round(self.valor, 2))
        printColor(aux, color='verde')
    def getUpdate(self):
        return [self.entrada, self.data, self.valor]

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
        for n, item in enumerate(self.listaEntradas):
            print(cor(f'{n}', color='verde'), end=' ')
            item.print()
            totalEntradas += item.valor
        print(cor('Saidas'.center(80), color='vermelho', reverse=True))
        for n, item in enumerate(self.listaGastos):
            print(cor(f'{n}', color='vermelho'), end=' ')
            item.print()
            totalGastos += item.valor
        print(cor('Balanço Geral'.center(80), color='azul', reverse=True))
        printColor(f'Entradas: {totalEntradas}', color='verde')
        printColor(f'Gastos: {totalGastos}', color='vermelho')
        if totalEntradas > totalGastos:
            printColor(f'Balanço Total: {totalEntradas-totalGastos}', color='verde')
        else:
            printColor(f'Balanço Total: {totalEntradas-totalGastos}', color='vermelho')
    def getArray(self, type):
        array = []
        if type == 'gastos':
            for item in self.listaGastos:
                array.append(item.getUpdate())
        elif type == 'entradas':
            for item in self.listaEntradas:
                array.append(item.getUpdate())
        return array

