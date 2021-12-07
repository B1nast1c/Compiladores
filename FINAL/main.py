from Parser import parsing
from Generador import crearArch, genVar,cerrarE, genFunc
from Generador import operVar,comMain, initIf, cuerpIf
import sys



#-------------------------------------------------
#--------------TABLA DE SIMBOLOS------------------
#-------------------------------------------------
padres_table = [['Global', 0]]
padres = ['FUN_DECL', 'PRINC', 'IF_STAT', 'WHILE_STAT', 'ELIF', 'FOR_STAT']
symbol_table = []
variables = []
diccionario = {'number' : 'tempo', 'texto' : 'corda', 'char' : 'acapella', 'true' : 'scelta', 'false' : 'scelta' }
variablesEns = []

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
    sys.exit()
  else:
    for var in s.valor:
      if var[0] == 'id':
        if find_variable(var[1]) == False:
          print('ERROR')
          print('No existe la variable ', var[1])
          print()
          sys.exit()
          return
    
    tip_res = verif_tipo(s.valor)
    print(tip_res, "  ", s.token)
    if tip_res == False:
      print("Operacion de tipos no válida.")
      print()
      sys.exit()
      return
    
    if tip_res != s.token:
      print("Incompatibilidad de tipos.")
      print()
      sys.exit()
      return
    symbol_table.append(s)
    
    if s.lexema not in variablesEns:
      variablesEns.append(s.lexema)

    print("Simbolo añadido.")
    for i in symbol_table:
      print(i.token, i.lexema, " ", i.valor, " ", i.padre, ' ', i.padreCod)
    print()
  
def limpiar(s):
  for x in range(len(s)):
    if ['ε', ' '] in s:
      s.remove(['ε', ' '])
  return s

def limpiarmod(s):
  for x in range(len(s)):
    if [' '] in s:
      s.remove([' '])
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
      if find_token_variable(lista[i][1]) in parametros2:
        if tipo != find_token_variable(lista[i][1]):
          return False
    elif lista[i][0] in parametros1:
      if tipo != diccionario[lista[i][0]]:
        return False
      
  return tipo #Clave valor

def find_suma():
  print(symbol_table)



listaifs = []
listaelse = []
listafor = []
listaestados = []
listafunciones = []
def generarEnSum(raiz):
  nodes=[]
  nodes.append(raiz)
  pos = 0

  ingresando = False
  ingresandofor = False
  ingresandoif = False
  ingresandoFunDecl = False

  BlokPadre1 = False
  PadreElegido = ''
  PadreElegidoId = ''
  texto = []
  codif = ''
  codfun = ''
  nomFun = ''

  variableid = ''
  resultado = []

  while (len(nodes)): 
      curr = nodes[0]
#--------------------DETECCION DE ESTADOS------------------------
      if curr.token == 'IF_STAT':
        ingresandoif = True
        listaestados.append([curr.valor,curr.token])
        codif = curr.valor
      if curr.token == 'ELIF' :
        listaestados.append([curr.valor,curr.token])
      if curr.token == 'FUN_DECL':
        listaestados.append([curr.valor,curr.token])
        ingresandoFunDecl = True
        codfun = curr.valor

#---------------EJECUCION DE LINEAS --------------------
      if curr.token == 'VAR_DECL':
        ingresando = True

      if curr.token.islower() and ingresando == True and ingresandofor == False :
        if pos == 0:
          pos = pos +1
        elif pos == 1:
          variableid = curr.lexema
          pos = pos +1
        elif pos == 2:
          pos = pos +1
        elif pos == 3 and curr.lexema != ';':
          variable = curr.lexema
          texto.append(variable)

        else:
          texto = limpiarmod(texto)
          resultado = texto
          texto = []

          if len(listaestados) >= 1:
            if listaestados[len(listaestados)-1][1] == 'IF_STAT':
              listaifs.append([variableid,resultado, variablesEns])
            if listaestados[len(listaestados)-1][1] == 'ELIF':
              listaelse.append([variableid,resultado, variablesEns])
            if listaestados[len(listaestados)-1][1] == 'FUN_DECL':
              listafunciones.append([variableid,resultado, variablesEns])

          else:
            operVar(variableid,resultado, variablesEns)
          ingresando = False
          pos = 0


#--------------------CONDICION DEL IF ----------------
      if curr.token.islower() and ingresandoif == True and ingresando == False:

        if pos == 0:
          pos = pos +1
        elif pos == 1:
          pos = pos +1
        elif pos == 2:
          pos = pos +1
        elif pos == 3:
          n1 = curr.lexema
          pos = pos +1
        elif pos == 4:
          comp = curr.lexema
          pos = pos +1
        elif pos == 5:
          n2 = curr.lexema
          pos = pos +1
        elif pos == 6:
          initIf(n1,comp,n2, variablesEns, codif)
          pos = 0
          ingresandoif = False

#--------------------CONDICION DEL LA FUNCION ----------------
      '''if curr.token.islower() and ingresandoFunDecl == True and ingresando == False:

        if pos == 0:
          pos = pos +1
        elif pos == 1:
          pos = pos +1
        elif pos == 2:
          pos = pos +1
        elif pos == 3:
          n1 = curr.lexema
          pos = pos +1
        elif pos == 4:
          comp = curr.lexema
          pos = pos +1
        elif pos == 5:
          n2 = curr.lexema
          pos = pos +1
        elif pos == 6:
          initIf(n1,comp,n2, variablesEns, codif)
          pos = 0
          ingresandoif = False
 '''
 #SERÁ NECESARIO?

#---------------ELIMINACION DE ESTADOS---------------
      if curr.lexema == '}' and len(listaestados) >= 1:
        #print("Entro prro") #xd
        if listaestados[len(listaestados)-1][1] == 'IF_STAT':
          listaestados.pop()
        elif listaestados[len(listaestados)-1][1] == 'ELIF':
        #  print("llamo al else")
          cuerpIf(listaifs, listaelse, codif)
          listaestados.pop()
        elif listaestados[len(listaestados)-1][1] == 'VAR_DECL':
          genFunc(nomFun, listafunciones, listavar)
          listaestados.pop()

        




if __name__=='__main__':
  crearArch()
  root = parsing()
  if root != None:
    crear_lista_simbolos(root)
    genVar(variablesEns)
    comMain()
    generarEnSum(root)
  cerrarE()
  print(variablesEns)
  






