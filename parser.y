%{
  #include<stdio.h>
  int yylex();
  void yyerror(const char *s) { printf("ERROR: %sn", s); }
%}

%token PLUS MINUS MULT DIV EQUL EQEQ LESS GRTR NOT AND OR OPAR CPAR OBRA CBRA SMCL PRNT SCAN WHILE IF ELSE TYPE DOT RETURN COMMA INT STR IDENT


%start program

%%

program : block ;
block : OBRA statement CBRA | OBRA CBRA ;
statement : assigment | block | print | if | while | var_type SMCL ;
relexpression: expression EQEQ | expression LESS | expression GRTR | expression ;
expression: term PLUS | term MINUS | term OR | term DOT | term ;
term: factor | factor MULT | factor DIV | factor AND ;
factor: INT | STR | IDENT | PLUS factor | MINUS factor | NOT factor | SCAN OPAR CPAR | OPAR relexpression CPAR ;
assigment: var_type IDENT EQUL relexpression;
print: PRNT OPAR relexpression CPAR;
if: IF OPAR relexpression CPAR statement else;
while: WHILE OPAR relexpression CPAR statement;
else: ELSE statement | ;
var_type: TYPE IDENT | COMMA IDENT ;

%%

int main(){
  yyparse();
  return 0;
}