package main

// Write your own version of the interpreter of arithmetic expressions
// as described in this article.
// Remember: repetition is the mother of all learning.

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

const (
	INTEGER = "INTEGER"
	PLUS    = "PLUS"
	MINUS   = "MINUS"
	MUL     = "MUL"
	DIV     = "DIV"
	LPAREN  = "LPAREN"
	RPAREN  = "RPAREN"
	EOF     = "EOF"
	NONE    = 255
)

type TokenType string

type Token struct {
	Type  TokenType
	Value interface{}
}

type Lexer struct {
	input       string
	currentPos  int
	currentChar byte
}

func NewLexer(input string) *Lexer {
	l := &Lexer{input: input}
	l.currentPos = 0
	l.currentChar = l.input[l.currentPos]
	return l
}

func (l *Lexer) error() {
	fmt.Printf("Unknown character %c\n", l.currentChar)
	os.Exit(1)
}

func (l *Lexer) advance() {
	l.currentPos++
	if l.currentPos > len(l.input)-1 {
		l.currentChar = NONE
	} else {
		l.currentChar = l.input[l.currentPos]
	}
}

func (l *Lexer) skipWhiteSpace() {
	for l.isSpace(l.currentChar) && l.currentChar != NONE {
		l.advance()
	}
}

func (l *Lexer) integer() int {
	var result string
	for l.isDigit(l.currentChar) && l.currentChar != NONE {
		result += string(l.currentChar)
		l.advance()
	}
	num, _ := strconv.Atoi(result)
	return num
}

func (l *Lexer) getNextToken() *Token {
	for l.currentChar != NONE {
		if l.isSpace(l.currentChar) {
			l.skipWhiteSpace()
		}
		if l.isDigit(l.currentChar) {
			return &Token{Type: INTEGER, Value: l.integer()}
		}
		if l.currentChar == '+' {
			l.advance()
			return &Token{Type: PLUS, Value: "+"}
		}
		if l.currentChar == '-' {
			l.advance()
			return &Token{Type: MINUS, Value: "-"}
		}
		if l.currentChar == '*' {
			l.advance()
			return &Token{Type: MUL, Value: "*"}
		}
		if l.currentChar == '/' {
			l.advance()
			return &Token{Type: DIV, Value: "/"}
		}
		if l.currentChar == '(' {
			l.advance()
			return &Token{Type: LPAREN, Value: "("}
		}
		if l.currentChar == ')' {
			l.advance()
			return &Token{Type: RPAREN, Value: ")"}
		}
		l.error()
	}
	return &Token{Type: EOF, Value: NONE}
}

func (l *Lexer) isSpace(ch byte) bool {
	return ch == ' '
}

func (l *Lexer) isDigit(ch byte) bool {
	return '0' <= ch && ch <= '9'
}

// Interpreter ->
type Interpreter struct {
	lexer        *Lexer
	currentToken *Token
}

// NewInterpreter ->
func NewInterpreter(lexer *Lexer) *Interpreter {
	i := &Interpreter{lexer: lexer}
	i.currentToken = i.lexer.getNextToken()
	return i
}

func (i *Interpreter) error() {
	fmt.Printf("Syntax Error %v\n", i.currentToken)
	os.Exit(1)
}

func (i *Interpreter) eat(tokenType TokenType) {
	if i.currentToken.Type == tokenType {
		i.currentToken = i.lexer.getNextToken()
	} else {
		i.error()
	}
}

func (i *Interpreter) factor() int {
	token := i.currentToken
	var result int
	if token.Type == LPAREN {
		i.eat(LPAREN)
		result = i.expr()
		i.eat(RPAREN)
	} else {
		i.eat(INTEGER)
		result = token.Value.(int)
	}
	return result
}

func (i *Interpreter) term() int {
	result := i.factor()
	for i.currentToken.Type == MUL || i.currentToken.Type == DIV {
		if i.currentToken.Type == MUL {
			i.eat(MUL)
			result *= i.factor()
		}
		if i.currentToken.Type == DIV {
			i.eat(DIV)
			result /= i.factor()
		}
	}
	return result
}

func (i *Interpreter) expr() int {
	result := i.term()
	for i.currentToken.Type == PLUS || i.currentToken.Type == MINUS {
		if i.currentToken.Type == PLUS {
			i.eat(PLUS)
			result += i.term()
		}
		if i.currentToken.Type == MINUS {
			i.eat(MINUS)
			result -= i.term()
		}
	}
	return result
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("calc> ")
		scanned := scanner.Scan()
		if !scanned {
			continue
		}
		input := scanner.Text()
		lexer := NewLexer(input)
		interpreter := NewInterpreter(lexer)
		result := interpreter.expr()
		fmt.Printf("%d\n", result)
	}
}
