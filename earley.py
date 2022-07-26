class Estado(object):
    def __init__(self, nome, regras, ponto, init, fim, id, origem, produtor):
        self.nome = nome
        self.regras = regras
        self.ponto = ponto
        self.init = init
        self.fim = fim
        self.id = id
        self.origem = origem
        self.produtor = produtor

    def __str__(self):
        str_inserçao_regra = ''
        for i, regra in enumerate(self.regras):
            if i == self.ponto:
                str_inserçao_regra += '/0 '
            str_inserçao_regra += regra + ' '
        if self.ponto == len(self.regras):
            str_inserçao_regra += '/0'

        if not(self.nome.islower()):
            return 'S%d %s -> %s [inicio: %d, fim: %d]' % (self.id, self.nome, str_inserçao_regra, self.init, 
                                                self.fim)
        return ""

    def __eq__(self, other):
        return (self.nome == other.nome and self.regras == other.regras and self.ponto == other.ponto and self.init == other.init and self.fim == other.fim)

    def prox(self):
        return self.regras[self.ponto]

    def final(self):
        return len(self.regras) == self.ponto

class Earley:
    def __str__(self):
        res = ''
        
        for i, ciclo in enumerate(self.ciclo):
            res += '\nD[%d]\n' % i
            for estado in ciclo:
                res += str(estado) + '\n'

        return res

    def __init__(self, palavras, gramática, terminais):
        self.ciclo = [[] for _ in range(len(palavras) + 1)]
        self.current_id = 0
        self.palavras = palavras
        self.gramática = gramática
        self.terminais = terminais

    def previsão(self, estado):
        for production in self.gramática[estado.prox()]:
            self.fila(estado(estado.prox(), production, 0, estado.fim, estado.fim, self.proximo(), [], 'previsão'), estado.fim)

    def varredura(self, estado):
        if self.palavras[estado.fim] in self.gramática[estado.prox()] :
            self.fila(estado(estado.prox(), [self.palavras[estado.fim]], 1, estado.fim, estado.fim + 1, self.proximo(), [], 'varredura'), estado.fim + 1)

    def conclusão(self, estado):
        for s in self.ciclo[estado.init]:
            if not s.final() and s.prox() == estado.nome and s.fim == estado.init and s.nome != 'S':
                self.fila(estado(s.nome, s.regras, s.ponto + 1, s.init, estado.fim, self.proximo(), s.origem + [estado.id], 'conclusão'), estado.fim)

    def parse(self):
        self.fila(estado('S', [inic], 0, 0, 0, self.proximo(), [], 'Inicio'), 0)
        
        for i in range(len(self.palavras) + 1):
            for estado in self.ciclo[i]:
                if not estado.final() and not self.eh_terminal(estado.prox()):
                    self.previsão(estado)
                elif i != len(self.palavras) and not estado.final() and self.eh_terminal(estado.prox()):
                    self.varredura(estado)
                else:
                    self.conclusão(estado)

    def proximo(self):
        self.current_id += 1
        return self.current_id - 1

    def fila(self, estado, ciclo_entry):
        if estado not in self.ciclo[ciclo_entry]:
            self.ciclo[ciclo_entry].append(estado)
        else:
            self.current_id -= 1

    def eh_terminal(self, tag):
        return tag in self.terminais

    def eh_fim(self, estado):
        return len(estado.regras) == estado.ponto

if __name__ == '__main__':
    op = input("Escolha entre digitar uma gramática (1) ou escolher uma pré-definida (2): ");

    if(op == "1"):
        print("Entrada de regras gramaticais:\n(formato A-> B C A D, com epsilon = % e $ para finalizar a entrada)\n----------------------------------------")
        gramática = {}
        prods = []
        vars = []
        term = []

        strng = ""
        while(strng != '$'):
            strng = input("Digite uma regra: ($ para finalizar)\n")
            if strng != '$': prods.append(strng)
            print("---")

        inic = input("Digite a variável inic:\n")
        gramática["S"] = inic
        print("----------------------------------------")

        for prod in prods:
            var = prod[0]
            if var not in vars and var.isupper(): 
                gramática[var] = []
                vars.append(var)

            auxDic = []

            for i,pi in enumerate(prod):
                if i<3: continue
                if pi not in [" ", "-", ">"]:
                    if(pi.islower()):
                        term.append(pi)
                        gramática[pi] = [pi]
                        auxDic.append(pi)
                    else:
                        auxDic.append(pi)

            gramática[var].append(auxDic)
        
        print(f'V = {vars} \nT = {term} \nP = {prods} \nS = {inic}')

        terminais = []

        for key in gramática:
            if key.islower():
                terminais.append(key)


        palavra = input("----------------------------------------\nDigite a palavra a ser analisada: ")

        letras = []
        for letra in palavra:
            letras.append(letra)

        earley = Earley(letras, gramática, terminais)
        earley.parse()
        print(earley)

    if (op == "2"):
        gramática = {
        'S':           [['E']],
        'E':           [['E','+','T'], ['T']],
        'T':           [['T', '*', 'F'], ['F']],
        'F':           [['(', 'E', ')'], ['x']],
        'Term':   ['(', ')', '*', '+', 'x'],
        '(':           ['('],
        ')':           [')'],
        '*':           ['*'],
        '+':           ['+'],
        'x':           ['x']
    }
        terminais = [ 'Term' ]

        print("V = { E, F, T } \nT= { ( , ) , *, +, x }\nP = [ E-> E+T, E-> T, T-> T*F, T-> F, F-> (E), F-> x ]\nS = E");

        palavra = input("Digite a palavra a ser analisada: ");
        letras = []

        for letra in palavra:
            letras.append(letra)

        earley = Earley(letras, gramática, terminais)
        earley.parse()
        print(earley)