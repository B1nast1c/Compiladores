import os
file = open("Intento.s", "w")

def crearArch():
  file.write(".data" + os.linesep)
  file.write(".text" + os.linesep)
  file.write("main:" + os.linesep)
  file.write(os.linesep)

def gene(x):
  file.write("li $a0 " + str(x) + os.linesep)
  file.write(os.linesep)
  
def movS():
  file.write("sw $a0 0($sp)"+ os.linesep )
  file.write("addiu $sp $sp-4"+ os.linesep )
  file.write(os.linesep)

def sumO():
  file.write("lw $t1 4($sp)" + os.linesep)
  file.write("add $a0 $t1 $a0" + os.linesep)
  file.write("addiu $sp $sp 4" + os.linesep)
  file.write(os.linesep)

def cerrarE():
  file.write("jr $ra")
  file.close()

def crearSum(x,y):
  gene(x)
  movS()
  gene(y)
  sumO()





