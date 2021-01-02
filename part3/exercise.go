/*
 * This little calculator evaluates arithmetical expressions
 * with the following format: `INTEGER operator INTEGER`
 * is required by the part 3 of the series "Let's build a simple interpreter"
 */
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type Type string

// Token es el tipo por defecto para todos los tokens.
type Token struct {
	Type    Type
	Literal string
}

const (
	INTEGER = "INTEGER"
	PLUS    = "+"
	MINUS   = "-"
	EOF     = "EOF"
)

// Interpreter el objeto principal
type Interpreter struct {
	input        string
	currentChar  byte
	position     int
	currentToken *Token
}

// NewInterpreter crea una instancia de Interpreter
func NewInterpreter(input string) *Interpreter {
	i := &Interpreter{input: input, position: 0}
	return i
}

func (i *Interpreter) getNextToken() *Token {
	if i.isAtEnd() {
		return &Token{Type: EOF, Literal: " "}
	}

	i.currentChar = i.input[i.position]

	for i.currentChar == ' ' && !i.isAtEnd() {
		i.advance()
	}

	if i.isDigit(i.currentChar) {
		tokenStr := string(i.currentChar)
		i.advance()
		for i.isDigit(i.currentChar) {
			tokenStr += string(i.currentChar)
			i.advance()
		}
		return &Token{Type: INTEGER, Literal: tokenStr}
	}

	if i.currentChar == '+' {
		i.advance()
		return &Token{Type: PLUS, Literal: "+"}
	} else if i.currentChar == '-' {
		i.advance()
		return &Token{Type: MINUS, Literal: "-"}
	} else {
		fmt.Println("Parsing error")
		os.Exit(1)
	}

	return &Token{Type: EOF, Literal: " "}
}

func (i *Interpreter) advance() {
	i.position++
	if !i.isAtEnd() {
		i.currentChar = i.input[i.position]
		return
	}
	i.currentChar = 0
}

func (i *Interpreter) isDigit(ch byte) bool {
	return '0' <= ch && ch <= '9'
}

func (i *Interpreter) isAtEnd() bool {
	return i.position >= len(i.input)
}

func (i *Interpreter) eat(tokenType Type) {
	if i.currentToken.Type == tokenType {
		i.currentToken = i.getNextToken()
	} else {
		fmt.Printf("expected %v got %v\n", tokenType, i.currentToken.Type)
		os.Exit(1)
	}
}

// Expr = (INTEGER '+'|'-' INTEGER)*
func (i *Interpreter) Expr() int {
	i.currentToken = i.getNextToken()
	result, _ := strconv.Atoi(i.currentToken.Literal)
	i.eat(i.currentToken.Type)

	for i.currentToken.Type == PLUS || i.currentToken.Type == MINUS {
		if i.currentToken.Type == PLUS {
			i.eat(PLUS) // Match '+' and getNextToken()
			num, _ := strconv.Atoi(i.currentToken.Literal)
			result += num
		} else if i.currentToken.Type == MINUS {
			i.eat(MINUS)
			num, _ := strconv.Atoi(i.currentToken.Literal)
			result -= num
		}
		i.eat(i.currentToken.Type)
	}
	/*
		i.currentToken = i.getNextToken()
		left, _ := strconv.Atoi(i.currentToken.Literal)
		i.eat(INTEGER)

		op := i.currentToken.Literal
		i.eat(PLUS)

		right, _ := strconv.Atoi(i.currentToken.Literal)
		i.eat(INTEGER)

		var result int
		if op == "+" {
			result = left + right
		}
	*/

	return result
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("Calculator> ")
		scanned := scanner.Scan()
		if !scanned {
			return
		}
		text := scanner.Text()
		interpreter := NewInterpreter(text)
		fmt.Printf("%d\n", interpreter.Expr())
	}
}
