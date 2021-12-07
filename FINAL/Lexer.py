# ------------------------------------------------------------
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex


reserved = {
    'Bsi' : 'if',
    'Bno' : 'else',
    'tremolo' : 'while',
    'bis' : 'for',
    'finito' : 'break',
    'DC' : 'return',
    'vero' : 'true',
    'falso' : 'false',
    'niente' : 'null',
    'e' : 'and',
    'o' : 'or',
    'D' : 'not',
    'tempo' : 'integer',
    'acapella' : 'character',
    'corda' : 'string',
    'scelta' : 'boolean',
    'silencio' : 'void',
    'pentagrama' : 'main',
    'compone' : 'input',
    'lee' : 'output'
}
 
# List of token names. This is always required
tokens = ('comment_init',
'comment_fin',
'id',
'char',
'number',
'oper_suma',
'oper_dif',
'oper_div',
'oper_mult',
'oper_asign',
'oper_mod',
'oper_mayor',
'oper_menor',
'oper_identico',
'oper_diferente',
'oper_neg',
'oper_mayorigu',
'oper_menorigu',
'par_init',
'par_fin',
'key_init',
'key_fin',
'corch_init',
'corch_fin',
'comma',
'texto', 'break_line') + tuple(reserved.values()) #"Concatenación de listas"
# Regular expression rules for simple tokens
t_comment_init = r'\|\|\:'
t_comment_fin = r'\:\|\|'
#t_oper_pot  = r'\*\*'
t_oper_identico = r'=='
t_oper_mayorigu = r'>='
t_oper_menorigu = r'<='
t_oper_diferente = r'\!=' #Here
t_oper_suma = r'\+'
t_oper_dif = r'-'
t_oper_mult = r'\*'
t_oper_div = r'/'
t_par_init = r'\('
t_par_fin = r'\)'
t_oper_asign = r'='
t_oper_mod = r'%'
t_oper_mayor = r'>'
t_oper_menor = r'<'
t_oper_neg = r'\!'
t_key_init = r'{'
t_key_fin = r'}'
t_corch_init = r'\['
t_corch_fin = r'\]'
t_comma = r','
t_break_line = r'\;'

entrada = [] #---------------------------------

def t_texto(t):
  r'"([^\\"]|\\")*"'
  #r'"[a-zA-Z_][a-zA-Z_0-9-.]*( [a-zA-Z_][a-zA-Z_0-9]*)*"'
  t.type = reserved.get(t.value,'texto')   
  # Check for reserved words
  return t

def t_char(t):
     r'\|([^\\"]|\\")\|'
     t.type = reserved.get(t.value,'char')   
      # Check for reserved words
     return t

def t_id(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'id')   
      # Check for reserved words
     return t
# A regular expression rule with some action code
def t_number(t):
  r'\d+'
  t.value = int(t.value) # guardamos el valor del lexema
  return t
# Define a rule so we can track line numbers
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)
  # A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'
  # Error handling rule
def t_error(t):
  print("Illegal character ’ %s’" % t.value[0])
  t.lexer.skip(1)
# Build the lexer
lexer = lex.lex()
  # Test it out

def return_tokens(file):
  tokens=list()
  f = open(file, 'r')
  mensaje = f.read()
  f.close()
  lexer.input(mensaje)
  # Tokenize
  while True:
    tok = lexer.token()
    if not tok:
      break # No more input
    #print(tok)
    tokens.append([tok.type, tok.value, tok.lineno, tok.lexpos])

  return tokens
