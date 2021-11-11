from Parser import parsing
#-------------------------------------------------
#--------------TABLA DE SIMBOLOS------------------
#-------------------------------------------------
padres_table = [['Global', 0]]
padres = ['FUN_DECL', 'PRINC', 'IF_STAT', 'WHILE_STAT', 'ELIF', 'FOR_STAT']
symbol_table = []
variables = []
diccionario = {'number' : 'tempo', 'texto' : 'corda', 'char' : 'acapella', 'true' : 'scelta', 'false' : 'scelta' }

class symbol:
  def __init__(self, token, lexema = None, valor = None, linea = None, padre = None, padreCod = None):
    self.token = token
    self.lexema = lexema
    self.valor = valor
    self.linea = linea 
    self.padre = padre #ES SU FUNCION xd
    self.padreCod = padreCod
    self.encontrado = False #Para diferentes funciones y eso
#--------------------------------
  def meterLexema(self, lexema):
    self.lexema = lexema
  
  def meterValor(self, valor):
    self.valor = valor
  
  def meterLinea(self, linea):
    self.linea = linea

  def meterPadre(self, padre, id):
    self.padre = padre
    self.padreCod = id
#--------------------------------
def add_symbol(s):
  if find_symbol(s.lexema, s.padreCod):
    print('ERROR')
    print("La variable ", s.lexema, ' ya existe.')
  else:
    for var in s.valor:
      if var[0] == 'id':
        if find_variable(var[1]) == False:
          print('ERROR')
          print('No existe la variable ', var[1])
          print()
          return
    
    tip_res = verif_tipo(s.valor)

    if tip_res == False:
      print("Operacion de tipos no válida.")
      print()
      return
    
    if tip_res != s.token:
      print("Incompatibilidad de tipos.")
      print()
      return
    symbol_table.append(s)
    print("Simbolo añadido.")
    for i in symbol_table:
      print(i.token, i.lexema, " ", i.valor, " ", i.padre, ' ', i.padreCod)
    print()
  
def limpiar(s):
  for x in range(len(s)):
    if ['ε', ' '] in s:
      s.remove(['ε', ' '])
  return s


def find_symbol(nom_var, cod_pad):
  symbol_table.reverse()
  for e in symbol_table:
    if e.lexema == nom_var and e.padreCod == cod_pad:
      symbol_table.reverse()
      return e
  symbol_table.reverse()
  return 
      
def find_variable(var):
  symbol_table.reverse()
  for e in symbol_table:
    if e.lexema == var:
      symbol_table.reverse()
      return True
  symbol_table.reverse()
  return False

def find_token_variable(var):
  symbol_table.reverse()
  for e in symbol_table:
    if e.lexema == var:
      symbol_table.reverse()

      return e.token
  symbol_table.reverse()
  return False

def remove_symbol(func_padre, cod_pad):
  for i in symbol_table:
    if func_padre == i.padre and cod_pad == i.padreCod:
      symbol_table.remove(i)
      print("Simbolo/s eliminado/s.")
      for i in symbol_table:
        print(i.token, i.lexema, " ", i.valor, " ", i.padre, ' ', i.padreCod)
      print()
      remove_symbol(func_padre, cod_pad) 


def crear_lista_simbolos(raiz):
  nodes=[]
  nodes.append(raiz)
  pos = 0
  ingresando = False
  ingresandofor = False
  BlokPadre1 = False
  PadreElegido = ''
  PadreElegidoId = ''
  texto = []
  while (len(nodes)): 
      curr = nodes[0]
#-------------Mete lista simbolos---------------
      if curr.token == 'VAR_DECL':
        ingresando = True
      if curr.token.islower() and ingresando == True and ingresandofor == False :
        if pos == 0:
          simbolo = symbol(curr.lexema)
          pos = pos +1
        elif pos == 1:
          simbolo.meterLexema(curr.lexema)
          pos = pos +1
        elif pos == 2:
          pos = pos +1
        elif pos == 3 and curr.lexema != ';':
          variable = [curr.token, curr.lexema]
          texto.append(variable)
        else:
          texto = limpiar(texto)
          simbolo.meterValor(texto)
          padres_table.reverse()
          simbolo.meterPadre(padres_table[0][0], padres_table[0][1])
          padres_table.reverse()
          texto = []
          ingresando = False
          
          add_symbol(simbolo)
          pos = 0
      if curr.token == 'VAR_DECL_FOR':
        ingresandofor = True
      if curr.token.islower() and ingresandofor == True and ingresando == False:
        if pos == 0:
          simbolo = symbol(curr.lexema)
          pos = pos +1
        elif pos == 1:
          simbolo.meterLexema(curr.lexema)
          pos = pos +1
        elif pos == 2:
          pos = pos +1
        elif pos == 3 and curr.lexema != ',':
          variable = [curr.token, curr.lexema]
          texto.append(variable)
        else:
          simbolo.meterValor(texto)
          padres_table.reverse()
          simbolo.meterPadre(padres_table[0][0], padres_table[0][1])
          padres_table.reverse()
          texto = []
          ingresandofor = False
          
          add_symbol(simbolo)
          pos = 0
# Mete a los padres, cola de padres
      if curr.token in padres:
        PadreElegido = curr.token
        PadreElegidoId = curr.valor
        BlokPadre1 = True
      if curr.lexema == '{' or curr.lexema == '(': 
        if BlokPadre1 == True:
          padres_table.append([PadreElegido, PadreElegidoId])
          BlokPadre1 = False
      if curr.lexema == '}':
        padreElim =padres_table.pop()
        remove_symbol(padreElim[0], padreElim[1])
        BlokPadre1 = False
      nodes.pop(0)

      for it in range(len(curr.children)-1,-1,-1): 
          nodes.insert(0,curr.children[it])    

def verif_tipo(lista):
  if lista[0][0] == 'id': #Si es variable en lugar de tipo
    tipo = find_token_variable(lista[0][1])
  else:
    tipo = diccionario[lista[0][0]]
  parametros1 = ['number', 'texto', 'char', 'true' ,'false']
  parametros2 = ['tempo', 'corda', 'acapella', 'scelta']
  for i in range(len(lista)):
    if lista[i][0] == 'id':
      
      if find_token_variable(lista[i][0]) in parametros2:
        if tipo != find_token_variable(lista[i][0]):
          return False
    elif [lista[i][0]] in parametros1:
      if tipo != diccionario[lista[i][0]]:
        return False
      
  return tipo #Clave valor


if __name__=='__main__':
  root = parsing()
  if root != None:
    crear_lista_simbolos(root)
