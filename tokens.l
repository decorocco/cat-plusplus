%{
#include <stdio.h>
#include <string.h>
#include "parser.tab.h"
%}

%%

[ \t\n]

"pwus"                  return PLUS;
"mwinus"                return MINUS;
"twimes"                return MULT;
"dwivided"              return DIV;
"nyassign"              return EQUL;
"nyequals"              return EQEQ;
"smyaller"              return LESS;
"biggew"                return GRTR;
"nyot"                  return NOT;
"nyand"                 return AND;
"nyor"                  return OR;
"UwU"                   return OPAR;
"UMU"                   return CPAR;
"RAWR"                  return OBRA;
"XD"                    return CBRA;
"nya"                   return SMCL;
"showo"                 return PRNT;
"nyinput"               return SCAN;
"fornyow"               return WHILE;
"nyif"                  return IF;
"nyelse"                return ELSE;
"nyint"                 return TYPE;
"stwing"                return TYPE;
"concatenyate"          return DOT;
">///<"                 return RETURN;
","                     return COMMA;
[0-9]+                  return INT;
[a-zA-Z0-9]             return STR;
[a-zA-Z_][_a-zA-Z0-9]   return IDENT;

.                       printf("Unknown token!n"); yyterminate();

%%