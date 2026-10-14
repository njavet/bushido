# Bushido Command Language Specification

**Status:** Draft\
**Language:** Bushido Command Language (BCL)\
**Purpose:** A compact textual language for logging, querying, and
analyzing Bushido data.

## 1. Design Principles

BCL is a line-oriented command language. Each statement consists of
exactly one command followed by command-specific arguments and, where
supported, options, flags, and free-form text.

The first lexical token always identifies the command.

Unit types such as `running`, `lifting`, `work`, and `journal` are
commands in their own right. BCL therefore does not require a generic
`log` prefix.

``` text
running 1730 2400 5.2
lifting 1810 squat 120 5 5
journal 2230 # Thoughts about today.
find lifting squat weight>=120
```

The language is intended to be independent of any particular client. A
Textual, Elm, Telegram, Rust, or other client may submit the same BCL
statement to Citadel for parsing and execution.

## 2. Top-Level Grammar

The grammar below uses EBNF notation.

``` ebnf
statement       = command-name, command-body ;

command-body    = { whitespace, element },
                  [ whitespace, comment ] ;

element         = argument
                | option
                | flag ;

comment         = "#", [ whitespace ], free-text ;
```

This top-level grammar describes the lexical shape of a statement.
Individual commands define which arguments, options, flags, and comments
are valid and in which order.

A more semantic definition is:

``` ebnf
statement       = unit-command
                | query-command
                | analysis-command
                | mutation-command
                | system-command ;
```

## 3. Lexical Elements

### 3.1 Command Name

``` ebnf
command-name    = identifier ;
identifier      = letter, { letter | digit | "_" | "-" } ;
```

The command name is always the first token of a statement.

Examples:

``` text
running
lifting
journal
find
stats
progress
```

Command names are reserved at the top level.

### 3.2 Arguments

Arguments are positional values whose interpretation is defined by the
selected command.

``` ebnf
argument        = bare-value ;
```

Examples:

``` text
running 1730 2400 5.2
        ^^^^ ^^^^ ^^^
        positional arguments
```

BCL does not assign universal semantics to positional arguments. The
`running` parser, for example, may interpret them differently from the
`lifting` parser.

### 3.3 Options

Options represent named structured values.

Canonical form:

``` ebnf
option          = option-name, whitespace, option-value ;

option-name     = "--", identifier ;
option-value    = bare-value ;
```

Examples:

``` text
--avghr 151
--maxhr 174
--year 2026
--months 6
```

An option has a name and a value.

``` text
--avghr 151
   │      │
   │      └── value
   └───────── name
```

Command-specific grammars determine which options are legal.

### 3.4 Flags

Flags represent boolean properties and do not take a value.

``` ebnf
flag            = "--", identifier ;
```

Examples:

``` text
--indoor
--private
--verbose
```

Whether a `--name` token is an option or flag is determined by the
grammar of the active command.

### 3.5 Comment / Free-Form Text

A hash character introduces free-form text:

``` ebnf
comment         = "#", [ whitespace ], free-text ;
free-text       = ? all characters until end of line ? ;
```

Once `#` is encountered, the remainder of the line is not parsed as
structured BCL syntax.

Example:

``` text
running 1730 2400 5.2 --avghr 151 # hard run -- but felt good
                                         │
                                         └── opaque free-form text
```

Therefore tokens such as `--`, numbers, punctuation, or words appearing
after `#` have no syntactic meaning to the structured command parser.

The interpretation of the free-form text is command-specific. For most
unit commands it is an annotation. For `journal`, it may constitute the
primary content of the unit.

Comments are not universally valid. Each command declares whether
free-form text is accepted.

## 4. Command Categories

### 4.1 Unit Commands

Unit commands create Bushido units.

Conceptually:

``` ebnf
unit-command    = unit-name,
                  unit-arguments,
                  { option | flag },
                  [ comment ] ;
```

Current or expected unit commands include:

``` text
running
swimming
rope
lifting
strength
cali
kyokushin
wimhof
work
journal
```

Each unit command owns its own argument grammar.

Example:

``` text
running 1730 2400 5.2 --avghr 151 --maxhr 174 # easy run
```

Conceptually:

``` text
running
│
├── arguments
│   ├── 1730
│   ├── 2400
│   └── 5.2
│
├── options
│   ├── --avghr 151
│   └── --maxhr 174
│
└── comment
    └── easy run
```

The exact grammar of each unit is specified independently.

### 4.2 Journal Command

`journal` is a unit command whose primary purpose is storing free-form
human text.

Proposed grammar:

``` ebnf
journal-command = "journal",
                  [ whitespace, time ],
                  whitespace, comment ;
```

Examples:

``` text
journal # Today was productive.
journal 2230 # Today was productive.
```

The text after `#` is the journal payload rather than merely an optional
annotation.

This preserves the same lexical boundary used by other unit commands
while allowing journal entries to contain arbitrary prose.

### 4.3 Query Commands

Query commands retrieve existing Bushido data without creating a unit.

Example family:

``` ebnf
query-command   = find-command
                | last-command ;

find-command    = "find",
                  whitespace,
                  query-expression,
                  { whitespace, option | flag } ;
```

Examples:

``` text
find lifting squat weight>=120
find lifting squat reps=5 sets=5
last running
```

A query expression may later receive its own formal subgrammar.

Comments are not accepted by default for query commands.

### 4.4 Analysis Commands

Analysis commands derive information from existing data.

``` ebnf
analysis-command = stats-command
                 | progress-command ;

stats-command    = "stats",
                   whitespace,
                   analysis-target,
                   { whitespace, option | flag } ;

progress-command = "progress",
                   whitespace,
                   analysis-target,
                   { whitespace, option | flag } ;
```

Examples:

``` text
stats running --year 2026
progress squat --months 6
```

Analysis commands may return scalar values, aggregates, time series, or
other structured results.

### 4.5 Mutation Commands

Mutation commands modify existing data rather than creating a new unit.

Possible future commands include:

``` text
delete
edit
tag
```

Their grammars are intentionally left unspecified until required.

### 4.6 System Commands

System commands affect the client/server interaction or expose
system-level functionality rather than Bushido domain records.

Possible examples include:

``` text
help
whoami
```

Client-only navigation commands should be distinguished from server-side
BCL commands if they are ever introduced.

## 5. Command-Specific Grammar

The top-level grammar deliberately does not attempt to define all
commands through one universal sequence of positional tokens.

Instead:

``` text
statement
    │
    ├── identify command
    │
    └── delegate remaining input
            │
            ├── running grammar
            ├── lifting grammar
            ├── journal grammar
            ├── find grammar
            ├── stats grammar
            └── ...
```

Formally:

``` ebnf
statement       = running-command
                | lifting-command
                | journal-command
                | find-command
                | stats-command
                | progress-command
                | ... ;
```

This permits commands to evolve independently without weakening the type
system or introducing a universal unstructured argument list.

## 6. Parsing Model

Parsing occurs in stages.

### Stage 1 --- Free-Text Separation

If the command supports free-form text, split structured syntax from the
first `#`.

``` text
running 1730 2400 5.2 --avghr 151 # easy run
└────────────────────────────────┘   └──────┘
         structured input              text
```

The free-form portion is preserved verbatim except for defined
whitespace normalization.

### Stage 2 --- Command Identification

Read the first structured token.

``` text
running 1730 2400 5.2
^^^^^^^
command
```

Unknown command names are syntax errors.

### Stage 3 --- Command-Specific Parsing

The remaining structured input is delegated to the parser registered for
the command.

Conceptually:

``` python
COMMANDS = {
    "running": parse_running,
    "lifting": parse_lifting,
    "journal": parse_journal,
    "find": parse_find,
    "stats": parse_stats,
    "progress": parse_progress,
}
```

This mapping is illustrative rather than part of the language
specification.

### Stage 4 --- Semantic Validation

After syntactic parsing, values are validated according to domain rules.

For example, syntax may successfully identify:

``` text
--avghr 151
```

while semantic validation determines whether `151` is valid for that
field.

Parsing and domain validation are therefore separate operations.

### Stage 5 --- Execution

A successfully parsed command is converted into a typed command
representation and dispatched to the corresponding application/domain
operation.

``` text
source line
    ↓
lexer/parser
    ↓
typed command
    ↓
semantic validation
    ↓
application operation
    ↓
typed result
```

## 7. Whitespace

Whitespace separates structured lexical elements.

``` ebnf
whitespace      = whitespace-char, { whitespace-char } ;
whitespace-char = " " | "\t" ;
```

Leading and trailing structured whitespace should be ignored.

Multiple whitespace characters between structured tokens are equivalent
to a single separator unless a command-specific grammar explicitly
states otherwise.

Whitespace after `#` belongs to free-form text and is governed by the
comment normalization rules.

## 8. End of Statement

BCL is line-oriented.

``` ebnf
input           = statement, end-of-line ;
```

A newline terminates a statement.

One submitted command line therefore represents exactly one BCL
statement.

Multi-line commands are not currently part of the language.

## 9. Error Classes

An implementation should distinguish at least the following failure
categories.

### Unknown Command

``` text
foobar 123
```

`foobar` is not registered as a BCL command.

### Syntax Error

The command exists, but the input does not conform to its grammar.

``` text
running ???
```

### Unknown Option or Flag

``` text
running 1730 2400 5.2 --does-not-exist
```

### Missing Required Argument

A command does not contain all mandatory positional arguments.

### Invalid Value

The syntax is valid, but a parsed value violates semantic/domain
constraints.

### Unsupported Comment

A `#` free-text section is supplied to a command that does not accept
one.

For example, if `find` does not support comments:

``` text
find lifting squat # foo
```

is invalid rather than silently discarding the text.

## 10. Result Semantics

BCL defines commands, not presentation.

A command may produce different categories of typed results, for
example:

``` text
unit command       → created unit
find               → record set
stats              → aggregate/KPI
progress           → time series
mutation command   → mutation result
```

The language does not prescribe whether a client renders those results
as a notification, table, tree, graph, or another UI element.

Presentation remains a client concern.

## 11. Client/Server Boundary

Citadel owns the BCL grammar and semantics.

Clients submit source statements rather than implementing the domain
parser independently.

Conceptually:

``` text
Textual ───┐
Elm ───────┤
Rust ──────┼── BCL source line ──> Citadel ──> parser ──> domain
Telegram ──┘
```

This ensures that:

``` text
find lifting squat weight>=120
```

has the same meaning regardless of the client from which it was
submitted.

Clients may implement non-authoritative autocomplete or syntax
highlighting, but Citadel remains the source of truth for parsing and
validation.

## 12. Extension Rules

New functionality should normally be introduced by adding either:

1.  a new command;
2.  a new option or flag to an existing command; or
3.  a backwards-compatible extension to a command-specific argument
    grammar.

A new command must not change the interpretation of an existing valid
statement.

Options and flags should be command-scoped unless their semantics are
genuinely universal.

Free-form text should remain behind the `#` boundary and should not
acquire structured syntax.

## 13. Examples

### Unit Logging

``` text
running 1730 2400 5.2
running 1730 2400 5.2 --avghr 151
running 1730 2400 5.2 --avghr 151 --maxhr 174 # hard finish

lifting 1810 squat 120 5 5
lifting 1810 squat 120 5 5 # good form

work 0900 1200 bushido # command language implementation
wimhof 0715
```

### Journaling

``` text
journal # Good day.
journal 2230 # Finished the parser design. Need to simplify querying tomorrow.
```

### Queries

``` text
find lifting
find lifting squat
find lifting squat weight>=120
find lifting squat weight>=120 reps=5
last running
```

### Analysis

``` text
stats running
stats running --year 2026
progress squat
progress squat --months 6
```

## 14. Compact Grammar Summary

``` ebnf
input             = statement, end-of-line ;

statement         = unit-command
                  | query-command
                  | analysis-command
                  | mutation-command
                  | system-command ;

unit-command      = unit-name,
                    unit-arguments,
                    { whitespace, option | flag },
                    [ whitespace, comment ] ;

journal-command   = "journal",
                    [ whitespace, time ],
                    whitespace, comment ;

query-command     = find-command
                  | last-command
                  | ... ;

analysis-command  = stats-command
                  | progress-command
                  | ... ;

option            = "--", identifier, whitespace, option-value ;
flag              = "--", identifier ;

comment           = "#", [ whitespace ], free-text ;

identifier        = letter, { letter | digit | "_" | "-" } ;

free-text         = ? all characters until end of line ? ;
end-of-line       = ? newline or end of submitted input ? ;
```

## 15. Core Invariants

The following invariants define the intended character of BCL:

1.  The first token always identifies the command.
2.  Unit names are commands; no generic `log` prefix is required.
3.  Each command owns its argument grammar.
4.  Structured named values use options.
5.  Boolean switches use flags.
6.  `#` creates a hard boundary between structured syntax and free-form
    human text.
7.  Free-form text is interpreted only by commands that explicitly
    support it.
8.  Citadel is authoritative for parsing and semantics.
9.  Clients may assist input but do not redefine the language.
10. Command results are typed data; their visual representation is a
    client concern.
