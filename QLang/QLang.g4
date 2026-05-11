grammar QLang;

// ==========================================
// LEXER RULES
// ==========================================

TEXT: 'text';

// ==========================================
// PARSER RULES
// ==========================================

program: topLevelItem* EOF;

/** Elementy najwyższego rzędu */
topLevelItem
    : placeDecl         /** Deklaracja Place */
    | functionDecl      /** Deklaracja funkcji w global Place */
    | statement         /** Dowolne wyrażenie w global Place */
    ;

/** Deklaracja miejsca - Place */
placeDecl: PLACE ID '{' placeMember* '}';

placeMember
    : functionDecl  /** Deklaracja funkcji w tym place */
    | statement     /** Dowolne wyrażenie w tym place */
    ;

/** Blok kodu */
block: '{' statement* '}';



// -------------------- STAŁE  --------------------

// Stała jest wartością, może być używana jak zmienna ale nie może być modyfikowana
constDecl: CONST ID '=' expr;


// -------------------- UŻYCIE ZMIENNYCH --------------------
// Zmienne umożliwiają tworzenie tablic o dowolnie wielu wymiarach
// obs x[5][10] -> 5 wartości po 10 bitów
// num a[10][10] -> 10 tablic po 10 wartości
//
reference: '@' ID;

// Możliwe typy zmiennych: obs i num, state(jeszcze nie zrobione)
varType: STATE | OBS | NUM | TEXT;

// Do deklaracji zmiennej z możliwym przypisaniem
sizeVar: '[' (expr | '?') ']';               /** Rozmiar mogący zawierać zmienną */
varAssign: ID sizeVar* ('=' expr)?;  /** Deklaracja zmiennej z możliwym rozmiarem i przypisaniem */

// Do deklaracji zmiennej z brakiem możliwości przypisania (np. w deklaracji stanu kwantowego)
varNoAssign: ID sizeVar*;            /** Deklaracja zmiennej z możliwym rozmiarem bez przypisania */

// Do parametrów funkcji przy deklaracji
varParam: ID ('[' INT_NUMBER ']')?;             /** Zapis zmiennej jako parametr funkcji w deklaracji z możliwym stałym rozmiarem */
varParamDefault: ID ('[' INT_NUMBER ']')* ('=' expr)?; /** Zapis zmiennej jako parametr funkcji w deklaracji z możliwym stałym rozmiarem i przypisaniem wartości domyślnej */

// Do użycia zmiennej w wyrażeniach
index: '[' expr ']';                 /** Indeks obliczony z dowolnego wyrażenia */
var: ID index*;                      /** Użycie zmiennej z możliwym indeksem */

sizeGetter: '#' ID;                  /** Pobranie rozmiaru zmiennej/listy argumentów */

// -------------------- INSTRUKCJE --------------------
statement
    : stateDecl ';'        # stateDeclaration
    | constDecl ';'        # constDeclaration
    | varDecl ';'          # varDeclaration
    | receiveDecl ';'      # receiveDeclaration
    | sendStmt ';'         # sendStatement
    | gateStmt ';'         # gateStatement
    | measureStmt ';'      # measureStatement
    | assignStmt ';'       # assignmentStatement
    | functionCallStmt ';' # functionCallStatement
    | ifStmt               # ifStatement
    | forStmt              # forStatement
    | whileStmt            # whileStatement
    | ioStmt ';'           # ioStatement
    | BREAK ';'            # breakStatement
    | CONTINUE ';'         # continueStatement
    | RETURN expr? ';'     # returnStatement
    | block                # blockStatement
    | expr ';'             # exprStatement 
    | equation ';'         # equationStatement
    | ';'                  # semicolonStatement
    ;

// maybe TODO: równania z obliczaniem zmiennej niewiadomej
// np. 5 + (2 + ?x?) * z === 20
// do zmiennej 'x' będzie przypisana wartość, która spełnia to równanie
equation: expr '===' expr;
varUnknown: '?' var '?';

// -------------------- DEKLARACJE --------------------

// Wielokrotna deklaracja stanu kwantowego lub stanu w superpozycji
stateDecl
: STATE varNoAssign (',' varNoAssign)*  # multipleStateDecl
| STATE ID '=' SUPERPOSED               # superposedStateDecl
;

// Deklaracja zmiennej OBS lub NUM, możliwia wielokrotna deklaracja z przypisaniem
// Przypisanie może być tylko przy niektórych deklaracjach
varDecl: varType varAssign (',' varAssign)*;

// -------------------- PRZYPISANIE --------------------

assignStmt: var '=' expr;

// -------------------- FUNKCJE --------------------

// Deklaracja funkcji
functionDecl: FUNCTION ID '(' paramList ')' block;

// Lista parametrów funkcji
paramList: param? (',' param)* multipleParam?;
param: varType varParamDefault;
// Parametr wielokrotny przyjmujący dowolną liczbę argumentów,
// dostępny potem w funkcji jako tablica o nazwie ID
multipleParam: ',' '...' ID;

// Wywołanie funkcji
functionCallStmt:  ID '(' argList? ')';
argList: arg (',' arg)*;
arg: namedArg | expr;
namedArg: ID '=' expr;



// -------------------- KONTROLA PRZEPŁYWU --------------------

ifStmt: IF '(' expr ')' block ((ELSE_IF | ELIF) '(' expr ')' block)* (ELSE block)?;
forStmt: FOR ID FROM expr TO expr (STEP expr)? block;
whileStmt: WHILE '(' expr ')' block;

// -------------------- WEJŚCIE / WYJŚCIE --------------------

// Te funkcje prawdopodobnie będą usunięte i sprawdzane nazwami podczas wywołania
// funkcji, lub przed startem programu zdefiniowane zostaną jako wbudowane funkcje

ioStmt
    : PRINT '(' (expr (',' expr)*)? ')'
    | PRINTLN '(' (expr (',' expr)*)? ')' // println() lub println(x) lub println(x, BIN) or printf style
    | DEBUG '(' (expr | reference) ')'
    | INPUT '(' ID ('[' expr ']')? (',' format)? (',' constraint)? ')'
    ;

// Zakres przyjmowanych wartości do input
constraint
    : expr '..' expr
    | 'range' '(' expr ',' expr ')'
    ;

format: BIN | HEX;


// --- WYRAŻENIA (Z PRIORYTETAMI) ---

expr
    : '!' expr                           # NotExpr
    | '-' expr                           # MinusExpr
    | '+' expr                           # PlusExpr
    | '++' expr                          # PreIncrementExpr
    | '--' expr                          # PreDecrementExpr
    | expr '++'                          # PostIncrementExpr
    | expr '--'                          # PostDecrementExpr
    | expr '=' expr                      # AssignmentExpr
    | expr '+=' expr                     # PlusEqExpr
    | expr '-=' expr                     # MinusEqExpr
    | expr '*=' expr                     # MulEqExpr
    | expr '/=' expr                     # DivEqExpr
    | expr '%=' expr                     # ModEqExpr
    | expr '**=' expr                    # PowEqExpr
    | expr '&=' expr                     # AndEqExpr
    | expr '|=' expr                     # OrEqExpr    
    | expr '**' expr                     # PowExpr
    | expr ('*' | '/' | '%') expr        # MulDivModExpr
    | expr ('+' | '-') expr              # AddSubExpr
    | expr ('<' | '>' | '<=' | '>=') expr# RelExpr
    | expr ('==' | '!=') expr            # EqExpr
    | expr '&&' expr                     # AndExpr
    | expr '||' expr                     # OrExpr
    | '$' expr                          # TypeExpr
    | list                               # ListExpr
    | varUnknown                         # VarUnknownExpr
    | sizeGetter                         # SizeGetterExpr
    | NUM '(' argList? ')'               # NumCastExpr
    | ID '(' argList? ')'                # FuncCallExpr
    | ID ('[' expr ']')*                 # VarExpr
    | INT_NUMBER                         # IntNumExpr
    | NUMBER                             # NumExpr
    | BOOL_VAL                           # BoolExpr
    | NULL                               # NullExpr
    | STRING                             # StrExpr
    | '(' expr ')'                       # ParenExpr
    | expr '?' expr ':' expr             # ShortIfExpr
    ;
























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


// -------------------- LISTA --------------------

list 
    : '[' ']'                  # emptyList
    | '[' expr (',' expr)* ']' # nonEmptyList
    ;


// ==========================================
// LEXER RULES
// ==========================================

// Słowa kluczowe
STATE: 'state';
OBS: 'obs';
SUPERPOSED: 'superposed';
NUM: 'num'; // Do float

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

CONST: 'const';

IF: 'if';
ELSE: 'else';
ELIF: 'elif';
ELSE_IF: 'else if';
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
NULL: 'NULL';

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

STRING     : '"' (~["\r\n])* '"' 
           | '\'' (~['])* '\''
           | '`' (~[`])* '`'
           ;

INT_NUMBER: HEX_NUMBER | BIN_NUMBER | DEC_NUMBER;
NUMBER: FLOAT_NUMBER | INT_NUMBER;
fragment FLOAT_NUMBER: [0-9]+ '.' [0-9]* ([eE] [+-]? [0-9]+)?
| '.' [0-9]+ ([eE] [+-]? [0-9]+)?
| [0-9]+ [eE] [+-]? [0-9]+
;
fragment HEX_NUMBER: '0x' [0-9a-fA-F]+;
fragment BIN_NUMBER: '0b' [01]+;
fragment DEC_NUMBER: [0-9]+;




ID: [\p{L}_][\p{L}\p{N}_]*;

// Ignorowane
WS: [ \t\r\n]+ -> channel(HIDDEN);
LINE_COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;
