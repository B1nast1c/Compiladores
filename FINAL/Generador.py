import os
file = open("Intento.s", "w")


def crearArch():
  file.write(".data" + os.linesep)

def comMain():
  file.write(".text" + os.linesep)
  file.write("main:" + os.linesep)
  file.write(os.linesep)

def gene(x,variables):
  if x in variables:
    leerVar(x)
    file.write(os.linesep)
  else:
    file.write("li $a0 " + str(x) + os.linesep)
    file.write(os.linesep)
  
def movS():
  file.write("sw $a0 0($sp)"+ os.linesep )
  file.write("addiu $sp $sp-4"+ os.linesep )
  file.write(os.linesep)

def operVar(x,y,z):

  cont = 3
  if len(y)-1 > 1:
    crearOpe(y[0],y[2],y[1],z)
    file.write(os.linesep)
    while len(y) -1> cont:
      continurOpe(y[cont+1],y[cont],z)
      file.write(os.linesep)
      cont += 2
  else:
    gene(y[0],z)
    file.write(os.linesep)
  asigVar(x)

def sumO():
  file.write("lw $t1 4($sp)" + os.linesep)
  file.write("add $a0 $t1 $a0" + os.linesep)
  file.write("addiu $sp $sp 4" + os.linesep)
  file.write(os.linesep)

def cerrarE():
  file.write("jr $ra")
  file.close()

def genVar(x):
  for i in x:
    file.write("var_"+ str(i) + ": .word 0:1" + os.linesep)

def leerVar(x):
  file.write("la $t0, var_"+ str(x) + os.linesep)
  file.write("lw $a0, 0($t0)" + os.linesep) 

def asigVar(x):
  file.write("la $t0, var_"+ str(x) + os.linesep)
  file.write("sw $a0, 0($t0)" + os.linesep) 

def crearOpe(x,y,z,variables):
  print(z, "entro")
  if z == '+':
    gene(x,variables)
    movS()
    gene(y,variables)
    sumO()

def continurOpe(y,z,variables):
  if z == '+':
    movS()
    gene(y, variables)
    sumO()

def mostrarAcum():
  file.write("li $v0, 1" + os.linesep)
  file.write("syscall" + os.linesep)

def initIf(n1,comp,n2,variables,id):
  print("initIF")
  print(n1, "  ",comp ,"  ",n2)
  gene(n1,variables)

  file.write("sw $a0, 0($sp)" + os.linesep)
  file.write("add $sp, $sp, -4" + os.linesep)

  gene(n2,variables)

  file.write("lw $t1, 4($sp)" + os.linesep)
  file.write("add $sp, $sp, 4" + os.linesep)
  if comp == '>':
    file.write("blt $a0, $t1, label_true_" + str(id) + os.linesep)
  elif comp == '<':
    file.write("blt $t1, $a0, label_true_" + str(id) + os.linesep)

def cuerpIf(listaif, listaelse, id):
  print("Cuerpo if")
  print(listaif)
  print("Cuerpo else")
  print(listaelse)

  file.write("label_false_"+ str(id)+":"+ os.linesep)
  # e_4
  if listaelse != []:
    for i in listaelse:
      operVar(i[0],i[1],i[2])
  file.write("b label_end_"+ str(id)+ os.linesep)
  file.write(os.linesep)
  file.write("label_true_"+ str(id)+":"+ os.linesep)
  if listaif != []:
    for i in listaif:
      operVar(i[0],i[1],i[2])
      
  file.write(os.linesep)
  file.write("label_end_"+ str(id)+":"+ os.linesep)
  file.write(os.linesep)
  return

#CREACION Y EJECUCION DE FUNCIONES
def invocaFuc(listavar,nomFun):
  file.write("sw $fp 0($sp)" + os.linesep)
  file.write("addiu $sp $sp-4" + os.linesep)
  listavar.reverse()
  for i in listavar:
    file.write("li $a0 " + str(i) + os.linesep)
    file.write("sw $a0 0($sp)" + os.linesep)
    file.write("addiu $sp $sp-4" + os.linesep)

  file.write("jal function_" + str(nomFun) + os.linesep)

def genFunc(nomFun, listacomandos, listavar):
  file.write("jal function_" + str(nomFun) + ":" + os.linesep)
  file.write("move $fp $sp" + os.linesep)
 
  file.write("sw $ra 0($sp)" + os.linesep)
  file.write("addiu $sp $sp -4" + os.linesep)

  for i in listacomandos:
    operVarFun(i[0],i[1], listavar)
  file.write("lw $ra 4($sp)" + os.linesep)
  file.write("addiu $sp $sp"+ str(len(listavar)*4 +8) + os.linesep) # 12 = 4*num_param + 8
  file.write("lw $fp 0($sp)" + os.linesep)
  file.write("jr $ra" + os.linesep)

def operVarFun(x,y,z):

  cont = 3
  if len(y)-1 > 1:
    crearOpeFun(y[0],y[2],y[1],z)
    file.write(os.linesep)
    while len(y) -1> cont:
      continurOpeFun(y[cont+1],y[cont],z)
      file.write(os.linesep)
      cont += 2
  else:
    geneFun(y[0],z)
    file.write(os.linesep)
  asigVar(x)

def crearOpeFun(x,y,z,variables):
  print(z, "entro")
  if z == '+':
    geneFun(x,variables)
    movS()
    geneFun(y,variables)
    sumO()

def continurOpeFun(y,z,variables):
  if z == '+':
    movS()
    geneFun(y, variables)
    sumO()

def geneFun(x,variables):
  if x in variables:
    leerVarFun(x,variables)
    file.write(os.linesep)
  else:
    file.write("li $a0 " + str(x) + os.linesep)
    file.write(os.linesep)

def leerVarFun(x,variables):
  file.write("lw $a0, " + str(4+4*(variables.index(x)+1)) +"($sp)" + os.linesep)
