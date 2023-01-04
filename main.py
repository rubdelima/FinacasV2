from tqdm import tqdm; #Barra de loading
from style import printColor, printCabecalho, cor;
from classes import Mes, Gasto, Entrada;
from sheetsAPI import *
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
        
    def showData(self, mes=None):
        if mes == None:
            for i in self.listaMeses:
                i.print()
        else:
            self.listaMeses[mes].print()
            
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
    }
    while(True):
        print("""O que deseja fazer?
[1] - Listar ano        [2] - Listar um mês
[3] - Adicionar gasto   [4] - Remover gasto
[5] - Adicionar entrada [6] - Remover entrada
[7] - Salvar Alterações [8] - Salvar e Sair""")
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
        else:
            printColor(f'ERRO! Digite um valor válido', color='vermelho')
    #obs: remover itens de compras no cartão