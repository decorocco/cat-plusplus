import sys
from os import error
import re

class PrePro:

    def filter(code):
        
        res = re.sub('/\*.*?\*/', '', code)
        
        return res

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):
        if (self.position >= len(self.origin)):
            self.actual = Token(value='', type='EOF')
            return self.actual
        elif (self.origin[self.position] == ' ' or self.origin[self.position] == '\n'):
            self.position += 1
            self.selectNext()

        elif (self.origin[self.position] == ','):
            self.actual = Token(value='', type='COMMA')
            self.position += 1
            return self.actual

        elif (self.origin[self.position] == '>'):
            self.position += 1
            if (self.origin[self.position] == '/'):
                self.position += 1
                if (self.origin[self.position] == '/'):
                    self.position += 1
                    if (self.origin[self.position] == '/'):
                        self.position += 1
                        if (self.origin[self.position] == '<'):
                            self.actual = Token(value='RETURN', type='RETURN')
                            self.position += 1
                            return self.actual
            else:
                raise error

        elif (self.origin[self.position].isnumeric()):
            candidate = self.origin[self.position]
            self.position += 1
            while (self.position < len(self.origin) and self.origin[self.position].isnumeric()):
                candidate += self.origin[self.position]
                self.position += 1
            self.actual = Token(value=int(candidate), type='INT')
            return self.actual

        elif (self.origin[self.position] == '"'):
            self.position += 1
            candidate = self.origin[self.position]
            self.position += 1
            while (self.position < len(self.origin) and self.origin[self.position] != '"'):
                candidate += self.origin[self.position]
                self.position += 1
            if (self.position == len(self.origin)):
                raise error
            self.actual = Token(value=candidate, type='STR')
            self.position += 1
            return self.actual
        
        elif (self.origin[self.position].isalpha()):
            candidate = self.origin[self.position]
            self.position += 1
            while (self.position < len(self.origin) and (self.origin[self.position].isalnum() or self.origin[self.position] == '_')):
                candidate += self.origin[self.position]
                self.position += 1
            if (candidate == "pwus"):
                self.actual = Token(value='', type='PLUS')
                return self.actual
            elif (candidate == "mwinus"):
                self.actual = Token(value='', type='MINUS')
                return self.actual
            elif (candidate == "twimes"):
                self.actual = Token(value='', type='MULT')
                return self.actual
            elif (candidate == "dwivided"):
                self.actual = Token(value='', type='DIV')
                return self.actual
            elif (candidate == "RAWR"):
                self.actual = Token(value='', type='OPAR')
                return self.actual
            elif (candidate == "XD"):
                self.actual = Token(value='', type='CPAR')
                return self.actual
            elif (candidate == "UwU"):
                self.actual = Token(value='', type='OBRA')
                return self.actual
            elif (candidate == "UMU"):
                self.actual = Token(value='', type='CBRA')
                return self.actual
            elif (candidate == "nyassign"):
                self.actual = Token(value='', type='EQUL')
                return self.actual
            elif (candidate == "nyequals"):
                self.actual = Token(value='', type='EQEQ')
                return self.actual
            elif (candidate == "nya"):
                self.actual = Token(value='', type='SMCL')
                return self.actual
            elif (candidate == "smyaller"):
                self.actual = Token(value='', type='LESS')
                return self.actual
            elif (candidate == "biggew"):
                self.actual = Token(value='', type='GRTR')
                return self.actual
            elif (candidate == "nyot"):
                self.actual = Token(value='', type='NOT')
                return self.actual
            elif (candidate == "concatenyate"):
                self.actual = Token(value='', type='DOT')
                return self.actual
            elif (candidate == "showo"):
                self.actual = Token(value='', type='PRNT')
                return self.actual
            elif (candidate == "fornyow"):
                self.actual = Token(value='', type='WHILE')
                return self.actual
            elif (candidate == "nyif"):
                self.actual = Token(value='', type='IF')
                return self.actual
            elif (candidate == "nyelse"):
                self.actual = Token(value='', type='ELSE')
                return self.actual
            elif (candidate == "nyinput"):
                self.actual = Token(value='', type='SCAN')
                return self.actual
            elif (candidate == "nyint"):
                self.actual = Token(value='INT', type='TYPE')
                return self.actual
            elif (candidate == "stwing"):
                self.actual = Token(value='STR', type='TYPE')
                return self.actual
            elif (candidate == 'vwoid'):
                self.actual = Token(value='VOID', type='TYPE')
                return self.actual
            elif (candidate == '>///<'):
                self.actual = Token(value='RETURN', type='RETURN')
                return self.actual
            self.actual = Token(value=candidate, type='IDENT')
            return self.actual

        else:
            print(self.origin[self.position])
            raise error

class Parser:
    
    token = None

    def ParseProgram():
        list_funcs = []
        while Parser.token.actual.type != 'EOF':
            node = Parser.ParseDeclaration()
            list_funcs.append(node)
        Parser.token.selectNext()
        return list_funcs

    def ParseDeclaration():
        if Parser.token.actual.type == 'TYPE':
            children = []
            varType = Parser.token.actual.value
            Parser.token.selectNext()
            if Parser.token.actual.type == 'IDENT':
                node = VarDec(varType, [Parser.token.actual]) 
                name = Parser.token.actual.value
                children.append(node)
                Parser.token.selectNext()
                if Parser.token.actual.type == 'OPAR':
                    Parser.token.selectNext()
                    if Parser.token.actual.type == 'TYPE':
                        varType = Parser.token.actual.value
                        Parser.token.selectNext()
                        if Parser.token.actual.type == 'IDENT':
                            node = VarDec(varType, [Parser.token.actual.value])
                            children.append(node)
                            Parser.token.selectNext()
                            while Parser.token.actual.type == 'COMMA':
                                Parser.token.selectNext()
                                if Parser.token.actual.type == 'TYPE':
                                    varType = Parser.token.actual.value
                                    Parser.token.selectNext()
                                    if Parser.token.actual.type == 'IDENT':
                                        node = VarDec(varType, [Parser.token.actual.value])
                                        children.append(node)
                                        Parser.token.selectNext()
                                        if Parser.token.actual.type == 'CPAR':
                                            Parser.token.selectNext()
                                            node = Parser.parseBlock()
                                            children.append(node)
                    
                    elif (Parser.token.actual.type == 'CPAR'):
                        Parser.token.selectNext()
                        node = Parser.parseBlock()
                        children.append(node)

                    else:
                        raise error
        else:
            raise error

        return DecFunc(name, children)
                    

    def parseBlock():

        if Parser.token.actual.type == 'OBRA':
            Parser.token.selectNext()
            node = BlockOp('', [])
            while(Parser.token.actual.type != 'CBRA'):
                node.children.append(Parser.parseStatement())
            Parser.token.selectNext()
            return node
        else:
            raise error

    def parseStatement():

        if Parser.token.actual.type == 'IDENT':
            valor = GetOp(Parser.token.actual.value ,[])
            Parser.token.selectNext()
            if Parser.token.actual.type == 'EQUL':
                Parser.token.selectNext()
                node = AssignmentOp('EQUL', [valor ,Parser.parseRelExpression()])
                if Parser.token.actual.type == 'SMCL':
                    Parser.token.selectNext()
                    return node
                else:
                    raise error
            elif Parser.token.actual.type == 'OPAR':
                Parser.token.selectNext()
                if Parser.token.actual.type != 'CPAR':
                    node = CallFunc(Parser.token.actual.value, [Parser.parseRelExpression()])
                else:
                    Parser.tokens.selectNext()
                    if Parser.token.actual.type == 'SMCL':
                        Parser.token.selectNext()
                        return node
            else:
                raise error
        
        elif Parser.token.actual.type == 'PRNT':
            Parser.token.selectNext()
            if Parser.token.actual.type == 'OPAR':
                Parser.token.selectNext()
                node = PrintOp('PRNT', [Parser.parseRelExpression()])
                if Parser.token.actual.type != 'CPAR':
                    raise error
                Parser.token.selectNext()
                if Parser.token.actual.type == 'SMCL':
                    Parser.token.selectNext()
                    return node
                else:
                    raise error

        elif Parser.token.actual.type == 'TYPE':
            node = VarDec(Parser.token.actual.value, [])
            Parser.token.selectNext()
            if (Parser.token.actual.type == 'IDENT'):
                node.children.append(Parser.token.actual.value)
                Parser.token.selectNext()
            else:
                raise error
            while(Parser.token.actual.type == 'COMMA'):
                Parser.token.selectNext()
                if (Parser.token.actual.type == 'IDENT'):
                    node.children.append(Parser.token.actual.value)
                    Parser.token.selectNext()
                else:
                    raise error
            if (Parser.token.actual.type == 'SMCL'):
                Parser.token.selectNext()
            return node

        elif Parser.token.actual.type == 'RETURN':
            Parser.token.selectNext()
            if Parser.token.actual.type == 'OPAR':
                Parser.token.selectNext()
                node = ReturnOp('RETURN', [Parser.parseRelExpression()])
                if Parser.token.actual.type != 'CPAR':
                    raise error
                Parser.token.selectNext()
                if Parser.token.actual.type == 'SMCL':
                    Parser.token.selectNext()
                    return node
                else:
                    raise error
            else:
                raise error
        
        elif Parser.token.actual.type == 'WHILE':
            Parser.token.selectNext()
            if Parser.token.actual.type == 'OPAR':
                Parser.token.selectNext()
                node = WhileOp('WHILE', [Parser.parseRelExpression()])
                if Parser.token.actual.type != 'CPAR':
                    raise error
                Parser.token.selectNext()
                node.children.append(Parser.parseStatement())
                return node

        elif Parser.token.actual.type == 'IF':
            Parser.token.selectNext()
            if Parser.token.actual.type == 'OPAR':
                Parser.token.selectNext()
                node = IfOp('IF', [Parser.parseRelExpression()])
                if Parser.token.actual.type != 'CPAR':
                    raise error
                Parser.token.selectNext()
                node.children.append(Parser.parseStatement())
                if Parser.token.actual.type == 'ELSE':
                    Parser.token.selectNext()
                    node.children.append(Parser.parseStatement())
                return node

        elif Parser.token.actual.type == 'SMCL':
            Parser.token.selectNext()
            node = NoOp('', [])
            return node

        else:
            return Parser.parseBlock()

    def parseRelExpression():

        node = Parser.parseExpression()

        while Parser.token.actual.type in ['EQEQ','GRTR','LESS']:
            if Parser.token.actual.type == 'EQEQ':
                Parser.token.selectNext()
                node = BinOp('EQEQ', [node, Parser.parseExpression()])
            elif Parser.token.actual.type == 'GRTR':
                Parser.token.selectNext()
                node = BinOp('GRTR', [node, Parser.parseExpression()])
            elif Parser.token.actual.type == 'LESS':
                Parser.token.selectNext()
                node = BinOp('LESS', [node, Parser.parseExpression()])

        return node


    def parseExpression():

        node = Parser.parseTerm()

        while Parser.token.actual.type in ['PLUS', 'MINUS', 'OR', 'DOT']:

            if Parser.token.actual.type == 'PLUS':
                Parser.token.selectNext()
                node = BinOp('PLUS', [node , Parser.parseTerm()])
            elif Parser.token.actual.type == 'MINUS':
                Parser.token.selectNext()
                node = BinOp('MINUS', [node , Parser.parseTerm()])
            elif Parser.token.actual.type == 'OR':
                Parser.token.selectNext()
                node = BinOp('OR', [node, Parser.parseTerm()])
            elif Parser.token.actual.type == 'DOT':
                Parser.token.selectNext()
                node = BinOp('DOT', [node, Parser.parseTerm()])

        return node

    def parseTerm():

        node = Parser.parseFactor()

        while Parser.token.actual.type in ['MULT', 'DIV', 'AND']:
            if Parser.token.actual.type == 'MULT':
                Parser.token.selectNext()
                node = BinOp('MULT', [node , Parser.parseFactor()])
            elif Parser.token.actual.type == 'DIV':
                Parser.token.selectNext()
                node = BinOp('DIV', [node , Parser.parseFactor()])
            elif Parser.token.actual.type == 'AND':
                Parser.token.selectNext()
                node = BinOp('AND', [node, Parser.parseFactor()])
    
        return node
    
    def parseFactor():
        node = 0

        if (Parser.token.actual.type == 'INT'):
            node = IntVal(Parser.token.actual.value, [])
            Parser.token.selectNext()

            if (Parser.token.actual.type == 'INT'):
                raise error

        elif (Parser.token.actual.type == 'STR'):
            node = StrVal(Parser.token.actual.value, [])
            Parser.token.selectNext()

        elif (Parser.token.actual.type == 'IDENT'):
            funcName = Parser.token.actual.value
            node = GetOp(Parser.token.actual.value, [])
            Parser.token.selectNext()
            if Parser.token.actual.type == 'OPAR':
                children = []
                Parser.token.selectNext()
                if Parser.token.actual.type != 'CPAR':
                    node = Parser.parseRelExpression()
                    children.append(node)
                    while(Parser.token.actual.type == 'COMMA'):
                        Parser.token.selectNext()
                        node = Parser.parseRelExpression()
                        children.append(node)
                    if Parser.token.actual.type == 'CPAR':
                        Parser.token.selectNext()
                        node = CallFunc(funcName, children)
                    else:
                        raise error

                elif Parser.token.actual.type == 'CPAR':
                    Parser.token.selectNext()

        elif (Parser.token.actual.type == 'PLUS'):
            Parser.token.selectNext()
            node = UnOp('PLUS', [Parser.parseFactor()])

        elif (Parser.token.actual.type == 'MINUS'):
            Parser.token.selectNext()
            node = UnOp('MINUS', [Parser.parseFactor()])
        
        elif (Parser.token.actual.type == 'NOT'):
            Parser.token.selectNext()
            node = UnOp('NOT', [Parser.parseFactor()])

        elif (Parser.token.actual.type == 'OPAR'):
            Parser.token.selectNext()
            node = Parser.parseRelExpression()
            if (Parser.token.actual.type != 'CPAR'):
                raise error
            Parser.token.selectNext()

        elif (Parser.token.actual.type == 'SCAN'):
            Parser.token.selectNext()
            if (Parser.token.actual.type == 'OPAR'):
                Parser.token.selectNext()
                node = ScanOp('', [])
                if Parser.token.actual.type != 'CPAR':
                    raise error
                Parser.token.selectNext()
        else:
            raise error

        return node

    def run(inp):
        nocomment = PrePro.filter(inp)
        Parser.token = Tokenizer(nocomment)
        Parser.token.selectNext()
        result = Parser.ParseProgram()
        if Parser.token.actual.type != 'EOF':
            raise error
        result.append(CallFunc('main', []))

        return result
        


class SymbolTable:
    def __init__(self):
        self.symbolTable = {}
    
    def Create(self, identifier, _type):
        if identifier in self.symbolTable:
            raise error
        self.symbolTable[identifier] = (None, _type)

    def Getter(self, identifier):
        if identifier not in self.symbolTable:
            raise error
        return self.symbolTable[identifier]

    def Setter(self, identifier, value, _type):
        if identifier not in self.symbolTable:
            raise error
        if _type != self.symbolTable[identifier][1]:
            raise error
        current = list(self.symbolTable[identifier])
        current[0] = value
        self.symbolTable[identifier] = tuple(current)


class FuncTable:
    funcTable = {}

    def Getter(funcName):
        if funcName not in FuncTable.funcTable.keys():
            raise error
        return FuncTable.funcTable[funcName]

    def Create(funcName, pointer):
        if funcName in FuncTable.funcTable.keys():
            raise error
        FuncTable.funcTable[funcName] = pointer


class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, st):
        pass

class BlockOp(Node):
    
    def Evaluate(self, st):
        for child in self.children:
            if child!=None:
                if child.value == "RETURN":
                    return child.Evaluate(st)
                child.Evaluate(st)

class UnOp(Node):

    def Evaluate(self, st):
        result = 0
        if self.children[0].Evaluate(st)[1] == 'INT':
            if self.value == 'PLUS':
                result = (self.children[0].Evaluate(st)[0], 'INT')
            elif self.value == 'MINUS':
                result = (-self.children[0].Evaluate(st)[0], 'INT')
            elif self.value == 'NOT':
                result = (not(self.children[0].Evaluate(st)[0]), 'INT')
            else:
                raise error
        else:
            raise error
        return result

class BinOp(Node):

    def Evaluate(self, st):
        child0 = self.children[0].Evaluate(st)
        child1 = self.children[1].Evaluate(st)

        if self.value == 'DOT':
            return (str(child0[0]) + str(child1[0]), 'STR')

        elif (child0[1] == 'INT' and child1[1] == 'INT'):
            if self.value == 'PLUS':
                return (child0[0] + child1[0], 'INT')
            elif self.value == 'MINUS':
                return (child0[0] - child1[0], 'INT')
            elif self.value == 'MULT':
                return (child0[0] * child1[0], 'INT')
            elif self.value == 'DIV':
                return (child0[0] // child1[0], 'INT')
            elif self.value == 'OR':
                return (child0[0] or child1[0], 'INT')
            elif self.value == 'AND':
                return (child0[0] and child1[0], 'INT')

        if (child0[1] == child1[1]):
            if self.value == 'EQEQ':
                if (child0[0] == child1[0]):
                    return (1 , 'INT')
                else:
                    return (0 , 'INT')
            elif self.value == 'GRTR':
                if (child0[0] > child1[0]):
                    return (1 , 'INT')
                else:
                    return (0 , 'INT')
            elif self.value == 'LESS':
                if (child0[0] < child1[0]):
                    return (1 , 'INT')
                else:
                    return (0 , 'INT')
            
        else: 
            raise ValueError("Imcompatible Typing")

class GetOp(Node):

    def Evaluate(self, st):
        return st.Getter(self.value)

class AssignmentOp(Node):

    def Evaluate(self, st):
        identifier = self.children[0].value
        identifiervalue = self.children[1].Evaluate(st)
        st.Setter(identifier=identifier, value=identifiervalue[0], _type=identifiervalue[1])

class PrintOp(Node):

    def Evaluate(self, st):
        print(self.children[0].Evaluate(st)[0])

class IntVal(Node):

    def Evaluate(self, st):
        return (self.value, 'INT')

class StrVal(Node):
    
    def Evaluate(self, st):
        return (self.value, 'STR')

class WhileOp(Node):

    def Evaluate(self, st):
        while self.children[0].Evaluate(st)[0]:
            self.children[1].Evaluate(st)

class IfOp(Node):

    def Evaluate(self, st):
        if self.children[0].Evaluate(st)[0]:
            self.children[1].Evaluate(st)
        elif len(self.children) > 2:
            self.children[2].Evaluate(st)

class ScanOp(Node):

    def Evaluate(self, st):
        return (int(input()), 'INT')

class NoOp(Node):

    def Evaluate(self, st):
        pass

class VarDec(Node):

    def Evaluate(self, st):
        for child in self.children:
            st.Create(child, self.value)

class DecFunc(Node):

    def Evaluate(self, st):
        FuncTable.Create(self.value, self)

class CallFunc(Node):

    def Evaluate(self, st):
        args = []
        newSt = SymbolTable()
        newFunc = FuncTable.Getter(self.value)
        for i in range(1, len(newFunc.children)-1):
            args.append(newFunc.children[i].children[0])
            newFunc.children[i].Evaluate(newSt)
        for j in range(len(args)):
            newSt.Setter(args[j], self.children[j].Evaluate(st)[0], self.children[j].Evaluate(st)[1])
        return newFunc.children[-1].Evaluate(newSt)

class ReturnOp(Node):

    def Evaluate(self, st):
        return self.children[0].Evaluate(st)

if __name__ == '__main__':
    f = open(sys.argv[1], "r")
    inp = f.read()
    f.close()
    a = Parser.run(inp)
    st = SymbolTable()
    for i in a:
        i.Evaluate(st)