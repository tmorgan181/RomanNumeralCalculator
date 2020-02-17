#TRENTON MORGAN
#CS 2200
#HW 1
#09/05/19

#This program performs the addition and subtraction of values represented with
#Roman numerals. It takes in the specified number of inputs (between 2 and 10
#inclusive)in the form of valid Roman numerals, then directly calculates the
#result and outputs it in the correct form.


#UTILITIES#
#---------#

#List of valid Roman numerals, sorted in order highest to lowest value.
romanNumerals = ['M','D','C','L','X','V','I']

#Dictionary of equivalences, used in expansion and compaction of values.
expansionTable = {"V" : "IIIII",
                  "X" : "VV",
                  "L" : "XXXXX",
                  "C" : "LL",
                  "D" : "CCCCC",
                  "M" : "DD"}

#Dictionary of subtractives, used in expansion and compaction of values.
subtractiveTable = {"IV" : "IIII",
                    "IX" : "VIIII",
                    "XL" : "XXXX",
                    "XC" : "LXXXX",
                    "CD" : "CCCC",
                    "CM" : "DCCCC"}

#Using regex, check that the input is a properly formatted Roman numeral.
import re                        #import regex module
def checkFormatting(num):
    goodFormatting = False
    #The expression below will match any valid Roman numeral, providing a basis
    #to verify the inputs against
    validExpression = "^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    #If the num matches the expression, the formatting is valid
    goodFormatting = re.match(validExpression, num)

    return goodFormatting

#Valid inputs consist of only Roman numerals, verified using the list
#romanNumerals defined above. They also must be formatted correctly, as checked
#by the checkFormatting() function. Returns the validity as a boolean value.
def checkValid(num):
    validInput = False
    while (not validInput):
        for char in num:
            if char in romanNumerals:
                validInput = True
            else:
                validInput = False
                break

        #After checking that all characters in the input are Roman numerals,
        #check that the number is formatted correctly
        if validInput:
            validInput = checkFormatting(num)

        return validInput

#Directly adds two Roman numeral values and returns the result in the correct
#format.
def romanAdd(first, second):
    #First we must replace any subtractives with their expansions
    for subtractive in subtractiveTable.keys():
        first = first.replace(subtractive, subtractiveTable[subtractive])
        second = second.replace(subtractive, subtractiveTable[subtractive])

    #Next, concatenate the two strings of numerals
    combined = first + second

    #Next, we sort the numerals in descending value order (defined in the list
    #romanNumerals above)
    result = "" 
    for numeral in romanNumerals:
        for char in combined:
            if char == numeral:
                result += char
    
    #Last, we compact any values that can be using the expansionTable and insert
    #subtractives where needed using the subtractiveTable
    for compactor in expansionTable.keys():
        result = result.replace(expansionTable[compactor], compactor)
    for subtractive in subtractiveTable.keys():
        result = result.replace(subtractiveTable[subtractive], subtractive)

    return result

#Directly subtracts second from first and returns the result.
def romanSubtract(first, second):
    #First we replace subtractives with their expanded value
    for subtractive in subtractiveTable.keys():
        first = first.replace(subtractive, subtractiveTable[subtractive])
        second = second.replace(subtractive, subtractiveTable[subtractive])

    #Next, eliminate any common symbols
    for char in second:
        if char in first:
            #Replace one instance of the symbol with an empty string
            first = first.replace(char, '', 1)
            #Do the same for the second input
            second = second.replace(char, '', 1)

    #If there are characters left over, we borrow to complete the difference
    if len(second) == 0:
        result = first
        return result
    else:
        #Replace all numerals in the inputs with I
        for numeral in romanNumerals[:6]:
            first = first.replace(numeral, expansionTable[numeral])
            second = second.replace(numeral, expansionTable[numeral])

        #Eliminate common symbols
        for char in second:
            if char in first:
                first = first.replace(char, '', 1)
                second = second.replace(char, '', 1)

    #The remainder of the first input is the result
    result = first

    #Lastly, compact the result
    for compactor in expansionTable.keys():
        result = result.replace(expansionTable[compactor], compactor)
    for subtractive in subtractiveTable.keys():
        result = result.replace(subtractiveTable[subtractive], subtractive)

    return result


#DRIVER#
#------#

#The number of inputs is specified by the user (2-10 terms).
numAllowed = False
while (not numAllowed):
    numInputs = input("Enter the number of terms: ")

    #Ensure numInputs consists of only integer digits
    if numInputs.isdigit():
        numInputs = int(numInputs)
    else:
        numInputs = 0

    #Check numInputs between 2 and 10    
    if numInputs >= 2 and numInputs <= 10:
        numAllowed = True
    else:
        print("Invalid number of terms. Must be between 2 and 10 inclusive.")

terms = []          #List of terms
operators = []      #List of operators, + or - only

#Get an input for each term, as well as an operator to go between each term. All
#operations are performed on the terms in the order they are given.
for i in range(numInputs):
    validInput = False
    while (not validInput):
        num = input("Enter the term: ")
        if not checkValid(num):
            print("Invalid input. Please try again.")
        else:
            validInput = True
            terms.append(num)

    #After all inputs except the last, a valid operator (+ or -) is required
    if i < numInputs - 1:
        validOperator = False
        while (not validOperator):
            operator = input("Enter operation type: ")
            if operator == '+' or operator == '-':
                validOperator = True
                operators.append(operator)
            else:
                print("Invalid operator. Please try again.")

#With valid inputs, perform the operations designated by their list, going
#first to last.
print("Performing calculation...")
numTerms = len(terms)
for i in range(numTerms - 1):
    #Get first two terms and an operator
    first = terms.pop(0)
    second = terms.pop(0)
    operator = operators.pop(0)

    #Add if +, subtract if -
    if operator == '+':
        result = romanAdd(first, second)
    else:
        result = romanSubtract(first, second)

    #Re-insert the result in the list so it will be used in the next operation
    terms.insert(0, result)

finalResult = terms[0]
print("Final result:")
print(finalResult)

