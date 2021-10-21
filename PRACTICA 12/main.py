from Parser import parsing
#-------------------------------------------------
#--------------TABLA DE SIMBOLOS------------------
#-------------------------------------------------

symbol_table = []
variables = []
class symbol:
  def __init__(self, token, lexema = None, valor = None, linea = None, padre = None):
    self.token = token
    self.lexema = lexema
    self.valor = valor
    self.linea = linea
    self.padre = padre
    self.encontrado = False #Para diferentes funciones y eso
#--------------------------------
  def meterLexema(self, lexema):
    self.lexema = lexema
  
  def meterValor(self, valor):
    self.valor = valor
  
  def meterLinea(self, linea):
    self.linea = linea
#--------------------------------
def add_symbol(s):
  symbol_table.append(s)
  
def finf_symbol(nom_var):
  symbol_table.reverse()
  for e in symbol_table:
    if e.lexema == nom_var:
      return e
      
def remove_symbol(func_padre):
  for i in symbol_table:
    if func_padre == symbol_table[i].padre:
      symbol_table.remove[i]

def crear_lista_simbolos(raiz):
  nodes=[]
  nodes.append(raiz)
  pos = 0
  ingresando = False
  texto = ''
  while (len(nodes)): 
      curr = nodes[0]
      if curr.token == 'VAR_DECL':
        ingresando = True
      if curr.token.islower() and ingresando == True:
        if pos == 0:
          simbolo = symbol(curr.lexema)
          pos = pos +1
        elif pos == 1:
          simbolo.meterLexema(curr.lexema)
          pos = pos +1
        elif pos == 2:
          pos = pos +1
        elif pos == 3 and curr.lexema != ';':
          texto = texto + str(curr.lexema)
        else:
          simbolo.meterValor(texto)
          texto = ''
          ingresando = False
          add_symbol(simbolo)
          pos = 0

      nodes.pop(0)

      for it in range(len(curr.children)-1,-1,-1): 
          nodes.insert(0,curr.children[it])    

if __name__=='__main__':
  root = parsing()
  crear_lista_simbolos(root)
  for i in symbol_table:
    print(i.token, " ", i.lexema, " ", i.valor)
  
 





