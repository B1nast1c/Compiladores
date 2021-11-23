.data
.text
main:

li $a0 3

sw $a0 0($sp)
addiu $sp $sp-4

li $a0 8

lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4

jr $ra