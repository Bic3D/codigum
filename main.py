
text = open("test.um", "r").read()

print("\n*********************\n\n\t>> CODIGUM <<\n\t versium 0.1\n")
print("-> Output:")

actions = ["dicere", "saluete", "inputum", "est"]
variables = {}


def intToRoman(num):
    prefix = ""
    if num < 0:
        prefix = "-"
        num = num * -1

    lookup = [
        (1000, 'M'),
        (900, 'CM'),
        (500, 'D'),
        (400, 'CD'),
        (100, 'C'),
        (90, 'XC'),
        (50, 'L'),
        (40, 'XL'),
        (10, 'X'),
        (9, 'IX'),
        (5, 'V'),
        (4, 'IV'),
        (1, 'I'),
    ]
    res = ''
    for (n, roman) in lookup:
        (d, num) = divmod(num, n)
        res += roman * d

    return prefix + res


def romanToInt(s):
    coeff = 1
    if s[0] == "-":
        coeff = -1
        s = s[1:]

    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500,
             'M': 1000, 'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
    i = 0
    num = 0
    while i < len(s):
        if i+1 < len(s) and s[i:i+2] in roman:
            num += roman[s[i:i+2]]
            i += 2
        else:
            # print(i)
            num += roman[s[i]]
        i += 1
    return num*coeff


def getLEX(word):
    for i in actions:
        if word == i:
            return ("ACTION", word)
    # print('-{0}-'.format(word))
    if checknumber(word):
        return ("INT", romanToInt(word))
    if word == "plus":
        return ("OPERATION", "+")
    if word == "minus":
        return ("OPERATION", "-")
    else:
        return("VAR", word)


def checknumber(word):
    if all(c in ['X', 'I', 'V', 'M', 'L', 'C', 'D'] for c in word):
        return True


def fixjv(char):
    if char == 'j':
        return 'i'
    elif char == 'v':
        return 'u'
    else:
        return char


def lex(text):
    result = []
    current = ""
    string = False

    for char in text:
        if char == " " and string == False:
            if current != "":
                result.append(getLEX(current))
                current = ""
            else:
                current = ""

        elif char == '"':
            if string == True:
                string = False
                result.append(("STRING", current))
                current = ""
            else:
                string = True

        elif char == "\n":
            if current != "":
                result.append(getLEX(current))
                current = ""
            result.append(("NEWLINE", ""))

        elif char == "+" or char == "-":
            result.append(("OPERATION", char))

        else:
            current += fixjv(char)

    if current != "":
        result.append(getLEX(current))
    # print(result)
    return result


# print(lex(text))

def dicere(arguments):
    output = ""

    for i in range(len(arguments)):
        if arguments[i][0] == "STRING":
            output += arguments[i][1] + " "

        if arguments[i][0] == "OPERATION":
            n1 = int(arguments[i-1][1])
            n2 = int(arguments[i+1][1])

            if arguments[i][1] == "+":
                output += intToRoman(n1 + n2)
            elif arguments[i][1] == "-":
                output += intToRoman(n1 - n2)

        elif arguments[i][0] == "INT":
            if arguments[i-1][0] != "OPERATION" and arguments[i+1][0] != "OPERATION":
                output += str(arguments[i][1])

    if output[-1] == " ":
        output = output[:-1]

    return output + "\n"


def action(arguments, action):
    if action == "dicere":
        return dicere(arguments)

    elif action == "saluete":
        return "Hellum Worldum!"
    elif action == "est":
        variables[arguments[0][1]] = arguments[1][1]

        return ""

    else:
        print("The "+action+" command is not defined yet :(")
        return ""


def parse(tokens):
    output = ""
    lines = []
    currentline = []
    for i in range(len(tokens)):
        if tokens[i][0] == "NEWLINE":
            if currentline != []:
                lines.append(currentline)
                currentline = []
        else:
            currentline.append(tokens[i])
    if currentline != []:
        lines.append(currentline)

    # print(lines)

    for line in lines:
        previousT = []
        n = 0
        op = 0

        for i in range(len(line)):
            if line[i][0] == "OPERATION":
                op += 1
            elif line[i][0] == "VAR":
                if (line[-1][0] == "ACTION" and line[-1][1] == "est") == False:
                    vtype = type(variables[line[i][1]])
                    if vtype is str:
                        line[i] = "STRING", variables[line[i][1]]
                    elif vtype is int:
                        line[i] = "INT", variables[line[i][1]]

        for j in range(op-1):
            done = False
            for i in range(len(line)):
                if done == False:
                    if line[i][0] == "OPERATION":
                        n1 = int(line[i-1][1])
                        n2 = int(line[i+1][1])

                        res = 0
                        if line[i][1] == "+":
                            res = n1 + n2
                        elif line[i][1] == "-":
                            res = n1 - n2

                        line[i] = ("INT", res)
                        line.remove(line[i-1])
                        line.remove(line[i])
                        done = True

        for token in line:
            if token[0] == "ACTION":
                output += action(previousT, token[1])
            else:
                previousT.append(token)
            n += 1

    return output


print(parse(lex(text)))
# print(variables)
