grammar QLang;

// ==========================================
// PARSER RULES
// ==========================================

program: topLevelItem* EOF;

/** Elementy najwyższego rzędu */
topLevelItem
    : placeDecl
    | functionDecl
    | statement
    ;

/** Miejsce (Place) - może zawierać funkcje i instrukcje */
placeDecl: PLACE ID '{' placeMember* '}';

placeMember
    : functionDecl 
    | statement
    ;

/** Definicja funkcji - parametry rejestrowe muszą mieć sztywny rozmiar */
functionDecl: FUNCTION ID '(' paramList? ')' block;

paramList: param (',' param)*;
param: (STATE | OBS) ID ('[' NUMBER ']')?;

/** Bloki kodu */
block: '{' statement* '}';

statement
    : stateDecl ';'
    | obsDecl ';'
    | receiveDecl ';'
    | sendStmt ';'
    | gateStmt ';'
    | measureStmt ';'
    | assignStmt ';'
    | functionCallStmt ';'
    | ifStmt
    | forStmt
    | whileStmt
    | ioStmt ';'
    | BREAK ';'
    | CONTINUE ';'
    | RETURN expr? ';'
    | block
    ;

// --- DEKLARACJE ---

stateDecl
    : STATE stateDef (',' stateDef)*
    | STATE ID '=' SUPERPOSED
    ;

stateDef: ID ('[' expr ']')?;

obsDecl
    : OBS obsDef (',' obsDef)*
    | OBS ID ('[' expr ']')? '=' expr
    ;

obsDef: ID ('[' expr ']')?;

// --- KOMUNIKACJA ---

receiveDecl
    : (STATE | OBS) ID ('[' expr ']')? RECEIVED receiveOpt*
    ;

receiveOpt
    : FROM (STRING | ID)
    | AS STRING
    ;

sendStmt
    : SEND ID ('[' expr ']')? TO (STRING | ID) (AS STRING)?
    ;

// --- OPERACJE KWANTOWE ---

gateStmt
    : singleQubitGate ID ('[' expr ']')?
    | multiQubitGate ID ('[' expr ']')? '->' ID ('[' expr ']')?
    | SWAP ID ('[' expr ']')? ID ('[' expr ']')?
    ;

singleQubitGate: H | SUPERPOSE | S | SHIFT | X | NOT | Y | DUAL_NOT | Z | PHASE_NOT;
multiQubitGate: CNOT | ENTANGLE | CZ | ENTANGLE_PHASE;

measureStmt
    : ID ('[' expr ']')? '=' (MEASURE | MEASUREX) ID ('[' expr ']')?
    ;

// --- PRZYPISANIA I FUNKCJE ---

assignStmt: ID ('[' expr ']')? '=' expr;

functionCallStmt: ID '(' argList? ')';

// --- KONTROLA PRZEPŁYWU ---

ifStmt: IF '(' expr ')' block (ELSE block)?;
forStmt: FOR ID FROM expr TO expr (STEP expr)? block;
whileStmt: WHILE '(' expr ')' block;

// --- WEJŚCIE / WYJŚCIE (I/O) ---

ioStmt
    : PRINT '(' expr (',' format)? ')'
    | PRINTLN '(' (expr (',' format)?)? ')' // println() lub println(x) lub println(x, BIN)
    | DEBUG '(' ID ('[' expr ']')? ')'
    | INPUT '(' ID ('[' expr ']')? (',' format)? (',' constraint)? ')'
    ;

// Zakres przyjmowanych wartości do input
constraint
    : expr '..' expr
    | 'range' '(' expr ',' expr ')'
    ;

format: BIN | HEX;
argList: expr (',' expr)*;

// --- WYRAŻENIA (Z PRIORYTETAMI) ---

expr
    : '!' expr                           # NotExpr
    | expr '**' expr                     # PowExpr
    | expr ('*' | '/' | '%') expr        # MulDivModExpr
    | expr ('+' | '-') expr              # AddSubExpr
    | expr ('<' | '>' | '<=' | '>=') expr# RelExpr
    | expr ('==' | '!=') expr            # EqExpr
    | expr '&&' expr                     # AndExpr
    | expr '||' expr                     # OrExpr
    | ID '(' argList? ')'                # FuncCallExpr
    | ID ('[' expr ']')?                 # VarExpr
    | NUMBER                             # NumExpr
    | BOOL_VAL                           # BoolExpr
    | STRING                             # StrExpr
    | '(' expr ')'                       # ParenExpr
    ;

// ==========================================
// LEXER RULES
// ==========================================

// Słowa kluczowe
STATE: 'state';
OBS: 'obs';
SUPERPOSED: 'superposed';

H: 'H';
SUPERPOSE: 'superpose';
S: 'S';
SHIFT: 'shift';
X: 'X';
NOT: 'not';
Y: 'Y';
DUAL_NOT: 'dual_not';
Z: 'Z';
PHASE_NOT: 'phase_not';
CNOT: 'CNOT';
ENTANGLE: 'entangle';
CZ: 'CZ';
ENTANGLE_PHASE: 'entangle_phase';
SWAP: 'swap';

MEASURE: 'measure';
MEASUREX: 'measureX';

IF: 'if';
ELSE: 'else';
FUNCTION: 'function';
RETURN: 'return';
FOR: 'for';
FROM: 'from';
TO: 'to';
STEP: 'step';
WHILE: 'while';
BREAK: 'break';
CONTINUE: 'continue';

PRINT: 'print';
PRINTLN: 'println';
DEBUG: 'debug';
INPUT: 'input';
PLACE: 'place';
SEND: 'send';
RECEIVED: 'received';
AS: 'as';
BIN: 'BIN';
HEX: 'HEX';

// Literale
BOOL_VAL: 'T' | 'F';

POW_OP:   '**';
LPAREN:   '(';
RPAREN:   ')';
LBRACE:   '{';
RBRACE:   '}';
LBRACK:   '[';
RBRACK:   ']';
COMMA:    ',';
SEMI:     ';';
COLON:    ':';
DOT:      '.';
QUESTION: '?';
BANG:     '!';
ARROW:    '->';
ASSIGN:   '=';
HAT:      '^';

STRING     : '"' (~["\r\n])* '"' ;

NUMBER: HEX_NUMBER | BIN_NUMBER | DEC_NUMBER;
fragment HEX_NUMBER: '0x' [0-9a-fA-F]+;
fragment BIN_NUMBER: '0b' [01]+;
fragment DEC_NUMBER: [0-9]+;



ID: [\p{L}_][\p{L}\p{N}_]*;

// Ignorowane
WS: [ \t\r\n]+ -> skip;
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;