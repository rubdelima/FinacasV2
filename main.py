from tqdm import tqdm; #Barra de loading
from style import printColor, printCabecalho, cor;
from classes import Mes, Gasto, Entrada, Category;
from sheetsAPI import *
import matplotlib.pyplot as plt
import time


id = '1KfcO6J8_oLxTQIsdZ1l4XmBz-teP-pbpGoU7NnZa_KA'
listaMesesAux = ['Janeiro', 'Fevereiro', 'Marco', 'Abril', 
                  'Maio', 'Junho', 'Julho', 'Agosto',
                  'Setembro', 'Outubro', 'Novembro','Dezembro']

def getData():
    listaMeses = []
    printColor('Carregando meses... Aguarde', color='azul')
    for mes in tqdm(listaMesesAux):
        mesAux = Mes(mes)
        gastos = getSheets(id,mes, '!A2:G50')
        for i in gastos[0]:
            auxGasto = Gasto(i)
            mesAux.listaGastos.append(auxGasto)
        entradas = getSheets(id, mes,'!H2:J50')
        for i in entradas[0]:
            auxEntrada = Entrada(i)
            mesAux.listaEntradas.append(auxEntrada)
        listaMeses.append(mesAux)
    return listaMeses

def updateData(listaMeses):
    printColor('Atualizando dados... Aguarde', color='azul')
    for mes in tqdm(listaMeses):
        updateSheets(id, mes.nome, '!A2:G50' , mes.getArray(type='gastos'))
        updateSheets(id, mes.nome, '!H2:J50', mes.getArray(type='entradas'))

def getTime(type=None):
    named_tuple = time.localtime() # get struct_time
    if type == 'm':
        return time.strftime("%m", named_tuple)
    else:
        return time.strftime("%d/%m/%Y", named_tuple)

class Main:
    def __init__(self):
        self.listaMeses = getData()
        
    def showData(self, mes=None, graph=False):
        listaEntradas = []
        listaSaidas = []
        listaES = []
        listaSaldo = [0]
        if mes == None:
            for i in self.listaMeses:
                e, s = i.print()
                listaEntradas.append(e)
                listaSaidas.append(s)
                listaES.append(e-s)
                listaSaldo.append(listaSaldo[-1]+e-s)
        else:
            self.listaMeses[mes].print()
        if graph and mes == None:
            del listaSaldo[0]
            self.showGraph(listaEntradas, listaSaidas, listaES, listaSaldo)
    def showGraph(self, e, s, es, sal):
        plt.plot(listaMesesAux, e, c='g', label='Entradas', marker='o', ls='-', lw='1')
        plt.plot(listaMesesAux, s, c='r', label='Gastos', marker='o', ls='-', lw='1')
        plt.plot(listaMesesAux, es, c='y', label='Balanço Mês', marker='o',ls='-', lw='1')
        plt.plot(listaMesesAux,sal, c='b', label='Saldo', marker='o', ls='-', lw='1')
        plt.legend(loc='lower left')
        plt.show()
    
    def addInCategory(self,nome, mes, valor):
        aux = Category(nome)
        aux.dictGastos[mes] = valor
        return aux
    
    def updateInCategory(self):
        self.listaCategorias = [] #lista de Categorias
        for i in self.listaMeses: #um for pelos objetos de classe Mes
            for j in i.listaGastos: #para cada item gastos
                if j.categoria in [k.nome for k in self.listaCategorias]: #se a categoria ja estiver na lista
                    for k in self.listaCategorias: #pecorro a lista
                        if j.categoria == k.nome: #se eu achar o nome certo
                            if i.nome not in k.dictGastos.keys():
                                k.dictGastos[i.nome] = j.valor
                            else:
                                k.dictGastos[i.nome] += j.valor
                else:
                    aux = self.listaCategorias.append(
                        self.addInCategory(j.categoria, i.nome, j.valor))
        
    
    def showCategorias(self):
        self.updateInCategory()
        for i in self.listaCategorias:
            i.show()
    
    def categoriasGraphic(self):
        self.updateInCategory()
        listaC = []
        listaCV =[]
        for i in self.listaCategorias:
            listaC.append(i.nome)
            listaCV.append(sum(i.dictGastos.values()))
        figl, axl = plt.subplots()
        axl.pie(listaCV, labels=listaC, autopct='%1.1f%%',
                shadow=True, startangle=90)
        axl.axis('equal')
        plt.show()

                            
    def addNewGasto(self):
        while(True):
            try:
                inMes= int(input('Deseja inserir na data atual ou em outra? 0->Atual/ 1->Outra'))
                if not inMes == True:
                    data = getTime()
                else:
                    data = int(input('Digite a data: '))
                parcelas = int(input('Insira a quantidade de parcelas: '))
                valor = float(input('Insira o valor: '))
                parcela = round(valor/parcelas, 2)
                gasto = [input('Insira o nome do gasto: '), data, parcela, input('Insira a categoria: '),
                        input('Insira o tipo (Cartão/Dinheiro/Débito): '),'1/1', input('Insira o propietário: '),]
                mesAtual=int(getTime('m'))-1
                for i in range(parcelas):
                    if mesAtual + i >= 12:
                        break
                    gasto[5] = f'{i+1}/{parcelas}'
                    self.listaMeses[mesAtual+i].listaGastos.append(Gasto(gasto))
                return
            except:
                printColor(f'ERRO! Digite um valor válido', color='vermelho')
    def removeGasto(self):
        while(True):
            try:
                inMes= int(input('Deseja remover o gasto da data atual ou em outra? 0->Atual/ 1->Outra'))
                if not inMes == True:
                    data = int(getTime('m'))
                else:
                    data = int(input('Digite o mês em inteiro: '))
                self.showData(mes=data-1)
                #self.listaMeses[data-1].print()
                removido = int(input('Insira a posição do item que deseja remover: '))
                del self.listaMeses[data-1].listaGastos[removido]
                return
            except:
                printColor(f'ERRO! Digite um valor válido', color='vermelho')
    def addEntradas(self):
        while(True):
            try:
                inData= int(input('Deseja usar a data atual ou outra? [1-Atual]/[0-Outra]: '))
                if inData:
                    data = getTime()
                else:
                    data = input('Digite a data: ')
                inMes = int(input('Desjeja inserir nesse ou em outro mês? [1-Atual]/[0-Outro]: '))
                if inMes:
                    mesAtual = int(getTime('m')) -1
                else:
                    mesAtual = int(input('Digite o mês em inteiro: '))-1
                entrada = [input('Insira o nome da entrada: '), data, input('Insira o valor: ')]
                self.listaMeses[mesAtual].listaEntradas.append(Entrada(entrada))
                return
            except:
                printColor(f'ERRO! Digite um valor válido', color='vermelho')
    def removeEntradas(self):
        while(True):
            try:
                inMes= int(input('Deseja remover a entrada da data atual ou em outra? 0->Atual/ 1->Outra'))
                if inMes == True:
                    data = int(getTime('m'))
                else:
                    data = int(input('Digite o mês em inteiro: '))
                self.showData(mes=data-1)
                #self.listaMeses[data-1].print()
                removido = int(input('Insira a posição do item que deseja remover: '))
                del self.listaMeses[data-1].listaEntradas[removido]
                return
            except:
                printColor(f'ERRO! Digite um valor válido', color='vermelho')
    def updateSheets(self):
        updateData(self.listaMeses)
    
        
if __name__ == '__main__':
    printCabecalho('Bem vindo a Finanças V2', color='azul', reverse=True, tam_cab=2)
    main = Main()
    switch = {
        '1': main.showData,
        '2': '',
        '3': main.addNewGasto,
        '4': main.removeGasto,
        '5': main.addEntradas,
        '6': main.removeEntradas,
        '7': main.updateSheets,
        '11': main.showCategorias,
        '12' : main.categoriasGraphic
    }
    while(True):
        print("""O que deseja fazer?
[1] - Listar ano         [2] - Listar um mês      [3] - Adicionar gasto   
[4] - Remover gasto      [5] - Adicionar entrada  [6] - Remover entrada
[7] - Salvar Alterações  [8] - Salvar e Sair      [9] -Sair sem Salvar
[10] - Ano c/ Gráfico    [11] - Listar Categoria  [12] - Gráfico Categorias""")
        entrada = input()
        if entrada in switch.keys():
            if entrada == '2':
                if(bool(input('Deseja ver do mês atual ou de outro?[1-Atual/0-Outro]: '))):
                    main.showData(mes=int(getTime('m'))-1)
                else:
                    main.showData(
                        mes=int(input('Digite o mês em inteiro: '))-1
                    )
            else:
                switch[entrada]()
        elif entrada == '8':
            main.updateSheets()
            printCabecalho('Obrigado, até mais', color='azul', reverse=True, tam_cab=2)
            break
        elif entrada == '9':
            break
        elif entrada == '10':
            main.showData(graph=True)
        else:
            printColor(f'ERRO! Digite um valor válido', color='vermelho')
    #obs: remover itens de compras no cartão