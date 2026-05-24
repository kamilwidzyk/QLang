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
constAssign: ID sizeVar* '=' expr;
constDecl: CONST (varType constAssign (',' constAssign)* | ID);


// -------------------- UŻYCIE ZMIENNYCH --------------------
// Zmienne umożliwiają tworzenie tablic o dowolnie wielu wymiarach
// obs x[5][10] -> 5 wartości po 10 bitów
// num a[10][10] -> 10 tablic po 10 wartości
//
reference: '@' ID;

// Możliwe typy zmiennych: state(stan kwantowy), obs(obserwacja), num(liczba), text
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
index
    : '[' expr DOTDOT expr ']'             /** Zakres indeksów [a..b] inclusive..exclusive */
    | '[' '[' expr (',' expr)* ']' ']'     /** Lista indeksów [[a, b, c]] */
    | '[' expr ']'                         /** Indeks obliczony z dowolnego wyrażenia */
    ;
var: ID index*;                      /** Użycie zmiennej z możliwym indeksem */

sizeGetter: '#' ID;                  /** Pobranie rozmiaru zmiennej/listy argumentów */

// -------------------- INSTRUKCJE --------------------
statement
    : constDecl ';'        # constDeclaration
    | varDecl ';'          # varDeclaration
    | receiveDecl ';'      # receiveDeclaration
    | sendStmt ';'         # sendStatement
    | gateStmt ';'         # gateStatement
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

// Deklaracja zmiennej OBS, NUM, TEXT lub STATE
// Przypisanie może być tylko przy niektórych deklaracjach
varDecl: varType varAssign (',' varAssign)*;

// -------------------- PRZYPISANIE --------------------

assignStmt: var '=' expr;

// -------------------- FUNKCJE --------------------

// Deklaracja funkcji
functionDecl: FUNCTION ID '(' paramList ')' block;

// Lista parametrów funkcji
paramList
    : param (',' param)* (',' multipleParam)?
    | multipleParam
    | /* empty */
    ;
param: varType varParamDefault;
// Parametr wielokrotny przyjmujący dowolną liczbę argumentów,
// dostępny potem w funkcji jako tablica o nazwie ID
multipleParam: '...' ID;

// Wywołanie funkcji
functionCallStmt:  ID '(' argList? ')';
argList: arg (',' arg)*;
arg: namedArg | expr;
namedArg: ID '=' expr;



// -------------------- KONTROLA PRZEPŁYWU --------------------

ifStmt: IF '(' expr ')' (block | statement) ((ELSE_IF | ELIF) '(' expr ')' (block | statement))* (ELSE (block | statement))?;
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
    : expr DOTDOT expr
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
    | (MEASURE | MEASUREX) var           # MeasureExpr
    | 'reset' var                        # ResetExpr
    | NUM '(' argList? ')'               # NumCastExpr
    | ID '(' argList? ')'                # FuncCallExpr
    | ID index*                           # VarExpr
    | INT_NUMBER                         # IntNumExpr
    | NUMBER                             # NumExpr
    | BOOL_VAL                           # BoolExpr
    | NULL                               # NullExpr
    | STRING                             # StrExpr
    | '(' expr ')'                       # ParenExpr
    | '^' ('^')* var                     # ParentExpr
    | expr '?' expr ':' expr             # ShortIfExpr
    ;




// Do zrobienia: operator ^ID (parent)
//
// ^a (parent::a)
// ^^a (parent::parent::a)


// Do zrobienia: biblioteka standardowa(to chyba będzie lepsze, bo będzie można zobaczyć implementację) lub funkcje wbudowane

// Do zrobienia: Konwersja typów
// nie odgapiamy operatorów (int) (float) itp
//
// ================= Obcinanie/zaokrąglanie/podłoga/sufit =======================
//
// num x = cut(2.5, 0); // cut obcina to co po przecinku, drugi argument opcjonalnie jak dla round
// num x = round(2.5, 2); // matematycznie poprawne zaokrąglenie, drugi argument opcjonalnie:
//                                                                      > 0: liczba miejsc po przecinku
//                                                                      = 0: zaokrąglenie do całości (domyślna wartość)
//                                                                      < 0: zaokrągle do dziesiątek(1), do setek(2) ...
// num x = floor(2.5, 0); // matematyczna podłoga, drugi argument opcjonalnie jak dla round
// num x = ceil(2.5, 0); // matematyczny sufit, drugi argument opcjonalnie jak dla round
//
// ================= Konwersję num/obs->str załatwia formatowanie '%' =================
// 
// ==================== Konwersja int->float w num: =======================
//
// Użycie operacji z floatem po drugiej stronie: x*1.0
// lub operator: x.0 
//
// ======================== Konwersja str->inne ==============================
//
// Operator: <format string> ~ <data string>
// Zwraca: listę z wartościami w kolejności jakimi zostały zapisane w format stringu
// <format string> może być regexem zapisanym w /regex/, wtedy zwracana lista zawiera przechwycone grupy
//
// text fmt = "x: %d, y: %f"; // format danych
// text data = "x: 10, y: 5.5"; // dane do wczytania
// list parsed = fmt ~ dane; 
// print(parsed); // [10, 5.5];











// Proponowane: struktury
//
// Deklaracja(możliwe domyślne wartości):
//
// pack Name { 
//      num x = 10; 
//      text t = "abc";
//      num y;
// }
// Deklaracja będzie wewnętrznie funkcją:
// function Name(num x = 10, text t = "abc", num y){
//      return [x: x, t: t, y: y]; // packa będzie listą z dowolnymi typami
// }
// 
// Inicjalizacja (typ pack będzie listą, która pozwala na dowolne typy elementów i pozwala na przypisanie nazw do indeksów):
//               (lub bardzie prawdopodobnie: lista będzie pozwalać na dowolne typy i nazwy, a pack będzie rozszerzeniem listy 
//                który będzie trzymał dodatkowe informacje - nazwa pack, blokada zmiany liczby/typu/rozmiaru elementów)
// 
// pack pack1 = Name(); // inicjalizacja z domyślnymi wartościami
// pack pack2 = Name(5, "123", 0); // inicjalizacja w kolejności deklaracji w strukturze
// pack pack3 = Name(x=5, t="123", y=0); // inicjalizacja w dowolnej kolejności nazwanymi argumentami
//
// Dostęp możliwy po indeksach(kolejność jak w deklaracji) albo po nazwach, przypisanie tak samo
//
// print(pack1[0]); // 5
// print(pack1|x); // 5 (nie wiem czy to jest najlepszy operator do tego)
// 

// Proponowane: opóźnienia
//
// wait(<number> <unit>);
//
// <unit> = s | ms | min | seconds | second | minute | minutes | hour | hours ....
//

//
// Dla list z nazwami(których jeszcze nie ma):
// list a = [x: 0, y: 1, z: 2, a: 3, b: 4];
// list b = a[["x", "y", "z"]];
// print(b); // [x: 0, y: 1, z: 2]
// list c = a["x".."a"]; // elementy są wycinane w kolejności deklaracji!, zaczynając od "x" bierzemy elementy aż do "a"(ale bez "a")
// print(c); // [x: 0, y: 1, z: 2]


// Proponowane: wykonanie funkcji w tle
// Klasa variable dostaje nowy parametr is_ready
//  
// num x = background(bg1) długie_obliczenia(y); // is_ready = false, funkcja działa w innym wątku
//                                             w momencie zakończenia funkcji, zwracana wartość jest przypisywana do x, i is_ready = true
//
// <<< tutaj dzieje się coś innego >>>
// 
// if(ready x){ ... } // warunek jest spełniony jeśli funkcja w tle się zakończyła
// waitfor(x); // blokuje do momentu zakończenia się funkcji w tle
// interrupt bg1; // przerwanie wykonania funkcji w tle używając id background
//
// Przypisanie/odczyt zmiennej gdy is_ready = false, kończy się błędem
//
// wywołana funkcja nie może mieć dostępu do aktualnych wartości z miejsca wywołania, ewentualnie snapshot z momentu wywołania
//

// Proponowne: typ dowolny zmiennej ustalany na podstawie pierwszej przypisanej wartości
//  
//  any x = 0; // zmienna staje się 'num'
//  any x = " "; // zmienna staje się 'text'
//  any x = [1, 2, 3]; // zmienna staje się 'list' tej wielkości jakiej jest przypisana lista
//
// Będzie to przydatne przy odbieraniu pakietów, których zawartość może nie być zawsze taka sama lub funkcja zwracających różne typy wartości
// Any będzie też można użyć w parametrach funkcji, np:
// 
// function add(any a, any b){ return a + b; }

// Proponowane: dodanie zawartości z pliku/'import' kodu
//
// <<<"sciezka_do_pliku">>> 
// <<<""sciezka_do_pliku"">> // podwójne apostrofy
//
// wyrażenie będzie dosłownie zastąpione zawartością pliku niezależnie gdzie zostanie to użyte(umożliwia wykonanie kodu z pliku)
// wersja z podwójnymi apostrofami:
//      - ładuje dane z pliku i zapisuje je jako stringa
//      - zamienia " na \" i inne espace chary
//      - nie pozwala na wyjście ze stringa i wykonanie kodu z pliku
//      - program musi sam wydobyć dane z tego stringa
//
// Ładowanie listy z pliku:
// Zawartość pliku 'lista.ql': [1, 2, 3, 4, 5] 
// Załadowanie do zmiennej:
//      list x = <<<"lista.txt">>>;
//
// Import funkcji
// Zawartość pliku 'func.ql': function add(any x, any y){ return x + y; }
// <<<"func.txt">>>
// num x = add(5, 10);
//
// Import stringa z pliku:
// Zawartość pliku 'str.txt': ala ma kota
// text t = <<<""str.txt"">>>;
//
// Import kawałków kodu:
// Zawartość pliku 'printXY.ql': println("x: %d, y: %d", x, y);
// num x = foo();
// num y = bar();
// <<<"printXY.ql">>>
//
// Rozszerzenie pliku nie ma znaczenia ale dla danych
// tekstowych ładowanych jako string ma być inne niż .ql
// a dla plików ładowanych jako kod QLang ma być .ql


// --- KOMUNIKACJA ---
//
// Wysłanie:
//
// send <zmienna/wartość> to <place> as <packet_name>; // argumenty <place> i <packet_name> są opcjonalne
// 
// Sprawdzanie dostępności w buforze odbioru
// 
// if (available <typ> from <place> named <packet_name>){ // <typ> <place> <packet_name> są opcjonalne, możliwy(chyba) będzie regex do filtrowania
//      <typ> x = receive <typ> from <place> named <packet_name>; // to będzie blokować do momentu odbioru pasującego pakietu
// }
//
// argumenty available i receive są opcjonalnymi filtrami, ich niepodanie spowoduje odbiór pierwszego odebranego pakietu
// (nie ma możliwości odebrania przez place1 pakietów przeznaczonych dla place2)
// (pakiety wysłane bez podania odbiorcy mogą być odebrane przez każdego - nie jest to broadcast, pakiet wysłany jest jeden)

// To niżej będzie pozmieniane
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
    : singleQubitGate var
    | multiQubitGate var '->' var
    | SWAP var var
    ;

singleQubitGate: H | SUPERPOSE | S | SHIFT | X | NOT | Y | DUAL_NOT | Z | PHASE_NOT;
multiQubitGate: CNOT | ENTANGLE | CZ | ENTANGLE_PHASE;


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
DOTDOT:   '..';
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
fragment FLOAT_NUMBER: [0-9]+ '.' [0-9]+ ([eE] [+-]? [0-9]+)?
| '.' [0-9]+ ([eE] [+-]? [0-9]+)?
| [0-9]+ [eE] [+-]? [0-9]+
;
fragment HEX_NUMBER: '0x' [0-9a-fA-F]+;
fragment BIN_NUMBER: '0b' [01]+;
fragment DEC_NUMBER: [0-9]+;




ID: [\p{L}_][\p{L}\p{N}_]*;

// Ignorowane
WS: [ \t\r\n]+ -> channel(HIDDEN);
LINE_COMMENT: '//' ~[\r\n]* -> channel(HIDDEN);
BLOCK_COMMENT: '/*' .*? '*/' -> channel(HIDDEN);
