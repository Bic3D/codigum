# Codigum!
The first programming langage in latin! (please keep your eyes closed when if you read the source code)

Edit: actually not, it looks like it is the third, after Lusus and Lingua::Romana::Perligata.

It is pretty useless though.


## Documentatum
#### Roman digits and operations
All numbers must be written in roman digits, operations should be written with `minus` and `plus` (but `-` and `+` still work)

example: `IV plus I` (returns `V`)

#### Dicere
it can show a string or an integer (it can be a variable)

usage: `<argument 1> <argument 2>... dicere` (at least one argument)

example: `"ave" dicere`

#### Est
Defines a variable

usage: `<variable name> <content> est`

example: `numerum II est`

#### Repetare
Repeats a command a number of times, this number can be a variable

usage: `<arguments> <number of times> repetare`

example: `""ave" dicere II repetare`

#### Comments
Like normal comments, written with `#`

usage: `<stuff> #<comment>`

example: `I plus I dicere # outputs 1 + 1`