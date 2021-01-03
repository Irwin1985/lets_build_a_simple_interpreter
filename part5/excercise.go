package main

/**
* This interpreter was written without looking at
* other resources but my head.
* exercise from: https://ruslanspivak.com/lsbasi-part5/
 */

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

// NONE indica que hemos alcanzado el final del input.
const NONE = 255

const (
	// INTEGER representa un entero sin signo.
	INTEGER = "INTEGER"
	// PLUS representa la suma de enteros.
	PLUS = "PLUS"
	// MINUS representa la resta de enteros.
	MINUS = "MINUS"
	// MUL representa la multiplicación de enteros.
	MUL = "MUL"
	// DIV representa la división de enteros.
	DIV = "DIV"
	// EOF representa un token vacío.
	EOF = "EOF"
	// LPAREN abre agrupador.
	LPAREN = "LPAREN"
	// RPAREN cierra agrupador.
	RPAREN = "RPAREN"
)

// TokenType para agrupar los tipos.
type TokenType string

// Token unidad básica que contiene todos los tokens.
type Token struct {
	Type  TokenType
	Value interface{}
}

// Lexer divide la cadena de entrada en tokens.
type Lexer struct {
	input       string
	currentChar byte
	currentPos  int
}

// NewLexer crea un objeto Lexer
func NewLexer(input string) *Lexer {
	l := &Lexer{input: input, currentPos: 0}
	l.currentChar = l.input[l.currentPos]
	return l
}

// IsAtEnd indica si estamos al final del input.
func (l *Lexer) IsAtEnd() bool {
	return l.currentPos > len(l.input)-1
}

// Advance avanza el puntero al siguiente caracter.
func (l *Lexer) Advance() {
	l.currentPos++
	if !l.IsAtEnd() {
		l.currentChar = l.input[l.currentPos]
	} else {
		l.currentChar = NONE
	}
}

// SkipWhiteSpace ignora todos los espacios en blanco.
func (l *Lexer) SkipWhiteSpace() {
	for l.IsSpace(l.currentChar) && l.currentChar != NONE {
		l.Advance()
	}
}

// Digit extrae un token de tipo INTEGER del input.
func (l *Lexer) Digit() int {
	var result string
	for l.IsDigit(l.currentChar) && l.currentChar != NONE {
		result += string(l.currentChar)
		l.Advance()
	}
	num, _ := strconv.Atoi(result)
	return num
}

// GetNextToken obtiene un token bajo demanda
func (l *Lexer) GetNextToken() *Token {
	for l.currentChar != NONE {
		if l.IsSpace(l.currentChar) {
			l.SkipWhiteSpace()
		}
		if l.IsDigit(l.currentChar) {
			return &Token{Type: INTEGER, Value: l.Digit()}
		}
		if l.currentChar == '+' {
			l.Advance()
			return &Token{Type: PLUS, Value: "+"}
		}
		if l.currentChar == '-' {
			l.Advance()
			return &Token{Type: MINUS, Value: "-"}
		}
		if l.currentChar == '*' {
			l.Advance()
			return &Token{Type: MUL, Value: "*"}
		}
		if l.currentChar == '/' {
			l.Advance()
			return &Token{Type: DIV, Value: "/"}
		}
		if l.currentChar == '(' {
			l.Advance()
			return &Token{Type: LPAREN, Value: "("}
		}
		if l.currentChar == ')' {
			l.Advance()
			return &Token{Type: RPAREN, Value: ")"}
		}
		l.Error()
	}
	return &Token{Type: EOF, Value: " "}
}

// Error muestra un error al usuario
func (l *Lexer) Error() {
	fmt.Printf("Invalid character %c\n", l.currentChar)
	os.Exit(1)
}

// IsSpace indica si el caracter actual es un espacio en blanco
func (l *Lexer) IsSpace(ch byte) bool {
	return ch == ' '
}

// IsDigit indica si el caracter actual es un digito.
func (l *Lexer) IsDigit(ch byte) bool {
	return '0' <= ch && ch <= '9'
}

// Interpreter es el encargado de "Reconocer y Ejecutar" la sintaxis.
type Interpreter struct {
	lexer        *Lexer
	currentToken *Token
}

// NewInterpreter crea un objeto de tipo Interpreter
func NewInterpreter(lexer *Lexer) *Interpreter {
	return &Interpreter{lexer: lexer, currentToken: lexer.GetNextToken()}
}

// Eat compara el token actual con el token dado y si son iguales entonces avanza el lookAhead.
func (i *Interpreter) Eat(tokenType TokenType) {
	if i.currentToken.Type == tokenType {
		i.currentToken = i.lexer.GetNextToken()
	} else {
		i.Error()
	}
}

// Error de sintaxis
func (i *Interpreter) Error() {
	fmt.Printf("Error de sintaxis: %v\n", i.currentToken)
	os.Exit(1)
}

// Expr   : term   ( (PLUS | MINUS) term  )*
// term   : factor ( (MUL  | DIV)   factor)*
// factor : INTEGER
func (i *Interpreter) Expr() int {
	result := i.Term()
	for i.currentToken.Type == PLUS || i.currentToken.Type == MINUS {
		sType := i.currentToken.Type
		if sType == PLUS {
			i.Eat(PLUS)
			result += i.Term()
		}
		if sType == MINUS {
			i.Eat(MINUS)
			result -= i.Term()
		}
	}
	return result
}

// Term : factor ( ( MUL | DIV ) factor )*
func (i *Interpreter) Term() int {
	result := i.Factor()
	for i.currentToken.Type == MUL || i.currentToken.Type == DIV {
		sType := i.currentToken.Type
		if sType == MUL {
			i.Eat(MUL)
			result *= i.Factor()
		}
		if sType == DIV {
			i.Eat(DIV)
			result /= i.Factor()
		}
	}
	return result
}

// Factor es un INTEGER o una Expresión agrupada.
func (i *Interpreter) Factor() int {
	var result int
	if i.currentToken.Type == LPAREN {
		i.Eat(LPAREN)
		result = i.Expr()
		i.Eat(RPAREN)
	} else {
		result, _ = i.currentToken.Value.(int)
		i.Eat(INTEGER)
	}
	return result
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("goCalc> ")
		scanned := scanner.Scan()
		if !scanned {
			return
		}
		input := scanner.Text()
		lexer := NewLexer(input)
		interpreter := NewInterpreter(lexer)
		result := interpreter.Expr()
		fmt.Println(result)
	}
}
