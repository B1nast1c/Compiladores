from Lexer import return_tokens
from Lexer import entrada
import pandas as pd
import graphviz

def Syntax(): #Función a usarse en las próximas fases del compilador
  if len(entrada) == 0:
    print ("Sintaxis Correcta")
    return True
  else:
    print ("Sintaxis Incorrecta")
    return False 

class nodo: #Nodo de un arbol
    global id
    def __init__(self, token, valor, padre = None):
      self.children = []
      self.valor = valor
      self.token = token
      self.visitado = False #Visit, pre-order
      self.muerto = False #No puede tener más hijos
      #self.valor.islower()
      
    def agregar_hijo(self, hijo):
      self.children.append(hijo)
      hijo.padre = self

    def recorridoPreordenv2(self): #Recorreido preorden IMPRESION
      nodes=[]
      nodes.append(self)
      while (len(nodes)): 
          curr = nodes[0]
          nodes.pop(0)
          # current node has been travarsed
          #print(curr.token,': ',curr.visitado, '|',curr.muerto)

          for it in range(len(curr.children)-1,-1,-1): 
              nodes.insert(0,curr.children[it])

    def meterhijo(self, hijo, numero): #INSERTAR
      nodes=[]
      # push the current node onto the stack
      nodes.append(self)
      # loop while the stack is not empty
      while (len(nodes)): 
          # store the current node and pop it from the stack
          curr = nodes[0]
          if len(curr.children) == 0 and curr.muerto == False:
            #print ("el padre al que meter es ", curr.token)
            hijo = nodo(hijo, numero)
            curr.agregar_hijo(hijo)
            return
          nodes.pop(0)
          # current node has been travarsed
          cont = 0
          for it in range(len(curr.children)-1,-1,-1): 
              nodes.insert(0,curr.children[it])
              if curr.children[it].visitado == True:
                cont = cont + 1
          if cont == 0 and curr.muerto == False:
            #print ("el padre al que meter es ", curr.token)
            hijo = nodo(hijo, numero)
            curr.agregar_hijo(hijo)
            return

    def visitarNodo(self): #VISITAR HIJOS / IRSE POR CIGARROS XDDDDDDDD
      nodes=[]
      # push the current node onto the stack
      nodes.append(self)
      # loop while the stack is not empty
      while (len(nodes)): 
          # store the current node and pop it from the stack
          curr = nodes[0]
          if curr.visitado == True:
            curr.muerto = True
          if curr.visitado == False:
            curr.visitado = True
            #print ("Nodo visitado es ", curr.token)
            return
          nodes.pop(0)
          # current node has been travarsed
          for it in range(len(curr.children)-1,-1,-1): #Vista preorden 
              nodes.insert(0,curr.children[it]) 

def parsing():
  stack = return_tokens('Prueba3.txt') #Lectura de archivos
  
  # if stack.pop()[0] == "key_fin": #Obtiene el id del token que se ha demostrado
    # print("ta bien.")

  df = pd.read_csv('tablaF.csv', index_col=0) #Lectura de tablas

  stack =["$"] #Stack 
  entrada.append("$") #Append a la entrada para verificar que sea el final de todo
  # print(entrada)
  valorToken = "PROGRAM"
  valorInput = entrada[0]

  numero = 1 #Identificador 
  raiz = nodo('PROGRAM', numero)
  raiz.visitado = True

  while (df.at[valorToken,valorInput]) == (df.at[valorToken,valorInput]):
    data = (df.at[valorToken,valorInput]).split(" ",2)
    data = data.pop()
    data = data.split(" ")
    if data[0] != 'ε':
      ramas=[]
      for i in range(len(data)):
        Token = data.pop()
        ramas.append(Token)
        stack.append(Token)
      ramas.reverse()
      for i in ramas:
        numero = numero + 1
        raiz.meterhijo(i, numero)
    else:
      numero = numero + 1
      raiz.meterhijo(data[0],numero)
      raiz.visitarNodo()

   # raiz.recorridoPreordenv2()

    #print()
    valorToken = stack.pop()
    raiz.visitarNodo()

    while valorToken == valorInput:
      entrada.remove(valorInput)
      if len(entrada) == 0:
        break
      raiz.visitarNodo()
     # raiz.recorridoPreordenv2()
      #print()
      valorToken = stack.pop()
      valorInput = entrada[0]
    
    #print(valorToken," ",valorInput)
    if len(entrada) == 0: #Si no hay más entrada
      break
    if valorToken.islower():#Si es terminal muere en ese nodo
      break

  raiz.recorridoPreordenv2()
  if Syntax():
    crear_grafico(raiz)
    return True
  return False

def crear_grafico(raiz): #Creacion del grafico
  g = graphviz.Digraph('G', filename='hello2.gv', node_attr={'color':'lightblue', 'style': 'filled'})
  nodos = []
  nodos.append(raiz)

  while (len(nodos)):
    curr = nodos[0]
    # print(curr.token) #Imprime el token actual
    g.node(str(curr.valor), str(curr.token))
    nodos.pop(0)
    for it in range(len(curr.children)): 
      nodos.insert(0,curr.children[it])
      if curr.children[it].token.islower():
        g.node(str(curr.children[it].valor), str(curr.children[it].token), color='lightcoral')
      else:
        #g.attr(style='filled', color='lightblue')
        g.node(str(curr.children[it].valor), str(curr.children[it].token), color='lightblue')
      
      g.edge(str(curr.valor),str(curr.children[it].valor))
    # print("------")
  g.view()
    
#----------------------------------------------------
#------------------------MAIN------------------------
#----------------------------------------------------

if __name__=='__main__':
  parsing() #Retorna Bool
