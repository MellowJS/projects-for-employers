# import everything
import os
from tkinter import * 
from tkinter import filedialog as fd
from tkinter import messagebox
import csv
from collections import OrderedDict
import tkinter
from typing import final




# importing webbrowser python module
import webbrowser

root = Tk() # set root variable to Tk()
root.title("Welcome") # set title of root to "Full Program"
global r


labelWelcomeRoot = Label(root, text="Welcome to my Software Development Project", pady=14) # assign label
labelWelcomeRoot.pack() # pack the label to root
buttonQuit = Button(root, text="Exit Program", command=root.destroy) # assign button() widget to buttonQuit variable, put it in root, set text and set the command to root.quit, so the program closes when you press this
buttonQuit.pack()

#class to create instance to make windows from
class Window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)


#Assigning URL to be opened
def openHelp(strURL):
#Open url in default browser
    webbrowser.open(strURL, new=2)


# Search Program Code
# set some globals and the most important bit the data document path to put in the file from the dialogue box.
def window1():
    global dataFilePath # make a global variable 'dataFilePath'
    global searchFieldValues # make a global variable 'searchFieldValues'
    global linesList
    dataFilePath = "" # put empty string in dataFilePath.
    searchFieldValues = [] # put empty list in dataFilePath. 
    

    def delimiterDeterminer(): # this function determines delimiter
        delimiter = '' # first set delimiter variable to empty string
        sniffer = csv.Sniffer() # then set the sniffer variable to csv.Sniffer() method

        with open(dataFilePath, 'r') as f: # open the csv file
            dialect = sniffer.sniff(f.readline(), [',', ';', '-', '\t', '|']) # look for each of these delimiters in the file.readline
            f.seek(0) # set the seek count to 0 meaning go back to the beginning of the file
            data = csv.reader(f, dialect) # set data variable to the csv.reader() method, which takes in the file as f, and the dialect variable
            delimiter = dialect.delimiter # set the delimiter variable to the dialect.delimiter which finds the delimiter
            f.close() # close the file that was opened
        return delimiter # returns the delimiter so you can use it in other functions


    def lineGetter(choice): # this function gets the list of lines that you want from the csv after taking in a string as a choice in the parameter 'choice'. I made this so it was easier to handle the file and have access to teh headers and the rest of the file. this makes it easier to work with any file.
        global linesList # set linesList as a global
        linesList = [] # put empty list in linesList 
        linesList2 = [] # put empty list in linesList
        splitList = [] # put empty list in linesList

        with open(dataFilePath, "r") as f: # open the csv file and use csv.reader module to skip the initial space in each header if there are any.
            #linesList = f.readlines()
            reader = csv.reader(f, skipinitialspace=True, delimiter=delimiterDeterminer())
            for row in reader: # and then use a for list to append to the linesList.
                linesList.append(row)
        f.close()

        if choice == "firstLine": # this if statement returns the firstRow which is the headers of the CSV if you pass the string "firstLine" into the choice parameter
            firstLine = linesList[0] # append the 0th index of the linesList into firstLine, this would be the row.
            return firstLine # return the first Line
        elif choice == "allLines": # this returns all the lines by returning linesList directly if you pass in 'allLines' as a string to the choice parameter
            return linesList
        elif choice == "withoutHeader": # this removes the header from the linesList and stores that in a variable if you pass in 'withoutHeader' into the choice parameter
            linesWithoutHeader = linesList # this puts the linesList into another varible lineswithoutHeader
            linesWithoutHeader.pop(0) # this pop(0) is a method which removes the first item of the lineswithoutHeader
            return linesWithoutHeader # this returns linesWithoutHeaderß
        else:
            print("Please enter argument in choice parameter: 'firstLine' or 'allLines' or 'withoutHeader'.") # prints error message instructing the user if nothing is passed in
    

    def createMainUI(): # define a function called createMainUI()
        global MainWindow # set a global variable called MainWindow
        
        MainWindow = Window(root) # assign Window(root) widget to MainWindow Variable
        MainWindow.title("Welcome to Search")# run title method to set title of the window to "welcome to search"
        
        #set two label widgets in variable welcomeInfo and welcomeInfo2, set text and then grid them to row 0 and row1, set columnspan to two so they take up two columns
        welcomeInfo = Label(MainWindow, text="Welcome to Search Program 2.0").grid(row=0, column=0, columnspan=2)
        welcomeInfo2 = Label(MainWindow, text="Please Open File to search through a file of your choice").grid(row=1, column=0, columnspan=2)
        # set two buttons, one to open file and one to continue by assigning buttons to the openFileButton variable and continueButton variable. These buttons go on the main window and they run command functions 1 called getFiledetails() with the filename passed into it and the other command function opens the searchFieldsUI window
        # so when you click these buttons the command functions run. the openFileButton uses a lambda which allows us to pass in an argument into the parameter where it wouldnt normally be able to
        openFileButton = Button(MainWindow, text="Open File", command=lambda: getFileDetails("fileName")).grid(row=2, column=0, columnspan=2)
        continueButton = Button(MainWindow, text="Continue", command=createSearchFieldsUI).grid(row=6, column=1)
        quitButton = Button(MainWindow, text="Quit", command=root.destroy).grid(row=6, column=0) # this button quits root, and shuts down the program.
        

    def createSearchFieldsUI(): # this defines a function called createSearchFieldsUI()
        global radioValue
        global r
        SearchFieldsWindow = Window(root) # assign window widget with it set to root and assign to the SearchFieldsWindow variable
        SearchFieldsWindow.title("Search Fields Window") # set title with .title() method which takes a string

        headerList = lineGetter("firstLine") # this is a function caleld lineGetter which gets the first line of the csv file in this case as i passed in 'firstLine' as an argument the inner workings of the function caused the linegetter to return different data based on an if statement logic. puts the first line of the csv file into headerList.
        itemList = lineGetter("withoutHeader")
        nestedDDList = createNestedListOfDropDownItems()
        # ADD DROPDOWNS
        r = IntVar()
        r.set(1)
        
        
        for i in range(len(headerList)): # a for loop that iterates over the indexes of headerlist
            searchFieldLabel = Label(SearchFieldsWindow, text=headerList[i].title()).grid(row=i, column=0) # sets a label to the left its textis the current iteration of headerlist. which is headerlist[i]
            searchField = Entry(SearchFieldsWindow, textvariable=StringVar()) # sets a entrybox to the right
            searchField.grid(row=i, column=1) # puts the entry box on the grid
            searchFieldValues.append(searchField) # puts the values from the searchfields into the searchField Values global variable
        radioButtonExact = Radiobutton(SearchFieldsWindow, text="Exact Match", variable=r, value=1, command=lambda: our_command).grid(row=len(headerList)+1, columnspan=2)
        radioButtonApproximate = Radiobutton(SearchFieldsWindow, text="Approximate Match", variable=r, value=2, command=lambda: our_command).grid(row=len(headerList)+2, columnspan=2)
        searchButton = Button(SearchFieldsWindow, text="SEARCH", command=createResultListUI).grid(row=len(headerList)+3, column=0, columnspan=2, padx=10, pady=10) 
        # the search button is placed with grid on after the entry box it takes the function commandListUI into the button command= so when you press it the command is run
        
    
    def createNestedListOfDropDownItems(): # this function sees if there are duplicates in that particular column if there are then true
        headerList = lineGetter("firstLine")
        itemList = lineGetter("withoutHeader")
        dictFromHeaders = dict.fromkeys(headerList, 0)
        itemListByIndex = []
        #dictFromHeaders[headerList[5]]
        noDupesList = []
        for i in range(len(headerList)): 
            itemListByIndex.append(list())# make as many empty lists as there are headers

        for i in range(len(itemListByIndex)): # go over itemlist by index
            for item in itemList: # for every row in itemList
                for x in range(len(item)): # go through indexes of item
                    if i == x:# test if the indexes are the same
                        itemListByIndex[i].append(item[x]) # append the item's column to the itemlist by indexes relevant empty list
        
        for item in itemListByIndex:
            noDupesList.append(list(dict.fromkeys(item))) # remove the duplicates with this line
        
        return noDupesList # returns a list of the items in itemlist in their ownlist after removing duplicates

        
        
    

    def createResultListUI():
        global radioValue
        global resultListBox # make global variable list box
        global searchResultWindow # make global the search result window so its accessible from other functions
        fieldToString = [] # put empty list inside the fieldToString variable I Will append later the search field Values to it and casefold it so its not case sensitive.
        itemList = lineGetter("withoutHeader") # this stores the return from lineGetter("withoutHeader") into the products list in this case we want the csv as a multi dimensional array without the headers in the first row
        resultList = [] # this stores and empty list where will append every matching result 
        searchResultWindow = Window(root) # this creates a instance of Window(root), basically makes a new window when the createResultListUI function is run
        searchResultWindow.title("Search result display window") # # sets the title
        resultListBox = Listbox(searchResultWindow) # sets the resultListBox variable with a list box
        resultListBox.config(width=100, height=28) # configures teh resultListBox with width and height of 100 and 28
        radioValue = r.get() # get radio value from radiobuttons
        exactMatches = [] # two lists one for exact matches and one for approx mat
        approxMatches = []

        for i in range(len(searchFieldValues)): # this for loop goes through the indexes of searchFieldValues and inserts the contents of searchFieldValues into field to string after getting the value from the StringVar() and then casefolding to remove case sensitivity
            fieldToString.insert(i, searchFieldValues[i].get().lower()) # insert a lowered version of the item in the searchFieldValues
        
        with open(dataFilePath, newline='',) as f: # open data file as f
            reader = csv.reader(f, skipinitialspace=True, delimiter=delimiterDeterminer()) #read opened file, f, into csv.reader and assign to reader variable

            for row in reader: # go over every row in reader
                exactMatch = True # set boolean, exactMatch, to True
                passes = True # set another boolean, passes, to True
                for i in range(len(fieldToString)): # go over a list of things you typed into the entries
                    inputVal = fieldToString[i] # put current iteration of fieldToString which is a searchterm into the inputVal while maintaining its index position
                    rowVal = row[i].lower() # set current iteration of the column of the row to rowVal but lower it before assignment
                    if inputVal == '' or inputVal == rowVal: # if the input value this current iteration is not an empty string or it is equal to the value in row that is in the same index
                        continue # continue to next iteration of loop
                    elif inputVal != '' and inputVal in rowVal: # if input value is not equal to empty string AND the inputVal is IN rowval ('in' is not the same as '==')
                        exactMatch = False # change the boolean to False if above condiition is met, the means that beyond this point in the loop it cannot be an exactMatch 
                    else:
                        exactMatch = False # if no conditions are met then both exact match and passes are False and we exit the inner loop naturally back to the ifstatments in the outer loop
                        passes = False
                if passes and exactMatch: # if both passes and exactMatch are equal to True
                    exactMatches.append(row) #then append to exactMatches list because it passed as an exact math 
                elif passes:
                    approxMatches.append(row) # however if it passes without exactMatch being true then it goes into approxMAtches list
                

        if radioValue == 1:
            for i in range(len(exactMatches)):
                resultListBox.insert(END, exactMatches[i])
        elif radioValue == 2:
            for i in range(len(approxMatches)):
                resultListBox.insert(END, approxMatches[i]) # go through the result list and put them into the result list box one by one using the loop to insert them at the END.

        resultListBox.grid(row=0, column=0, padx=40, pady=60) # place the listbox that holds results on the grid
        viewDetailButton = Button(searchResultWindow, text="View Information", command=viewDetail).grid(row=1, column=0, columnspan=2)# put a button under the resultListbox which is called view information and has teh command viewDetail

    def viewDetail(): # this is the function that runs when you press the view Information button on the window with the result list box  
        resultAnchorBox = [] # put empty list inside resultAnchorBox
        resultAnchor = resultListBox.get(ANCHOR) # get each anchor resultListBox to this variable resultAnchor
        firstRow = lineGetter("firstLine") # use the lineGetter() function to get the firstRow
        headingList = [] # put empty list inside headeringList

        for item in resultAnchor: # for every item in the resultAnchor which has the resultListbox anchors # append a string of the item in resultAnchor to the resultAnchorBox which is a list
            resultAnchorBox.append(str(item)) 
        

        for item in firstRow: # append each item in the firstRow of the CSV, the headers, to the headingList as a string.
            headingList.append(str(item))
        
        for i in range(len(resultAnchorBox)): # this for loop goes over the indexes of the resultAnchorBox and puts each result item next to the heading on each iteration as a label widget on the grid.
            selectedProductInfo = Label(searchResultWindow, text=f"{headingList[i]} : {resultAnchorBox[i]}", justify='left', anchor="w", font=('Courier', 17))
            selectedProductInfo.grid(row=i+2, column=0, columnspan=2)

    
            
    
    
    def getFileDetails(choice): # this function gets the details of the file based on the argument you pass into the choice parameter
        global dataFilePath # set a global dataFilePath
        theFile = fd.askopenfilename() # this gets the file path by opening a file dialog box and stores the path in the variable 'theFile'
        theFileType = theFile.split("/")[-1].split(".")[-1] # this is the FileType, the extension at the end of the file, we get this by splitting the path on every '/' and then getting the last item by using the index [-1] then splitting that last item on the dot and getting the last item from the list that was created by that split with [-1]
        theFileName = theFile.split("/")[-1].split(".")[0] # this is the FileName, the extension at the end of the file, we get this by splitting the path on every '/' and then getting the last item by using the index [-1] then splitting that last item on the dot and getting the first item from the list that was created by that split with [0]
        dataFilePath = theFile # put theFile path into datafilePath
        nameLabel1 = Label(MainWindow, text=f"File name: {theFileName}").grid(row=3, column=0, columnspan=2) # this makes a puts a Label with the file name as an fstring in the nameLabel1 Variable and grids it
        typeLabel1 = Label(MainWindow, text=f"File type: {theFileType}").grid(row=4, column=0, columnspan=2) # this makes a puts a Label with the file type as an fstring in the typeLabel1 Variable and grids it
        delimiterLabel = Label(MainWindow, text=f"The delimiter for this file is: {delimiterDeterminer()}") # this makes a variable delimiterLabel and puts the Label that has the text fstring that returns delimeterDeterminer() in the squiggly brackets so it prints the text then prints the type of delimiter the file is using
        delimiterLabel.grid(row=5, column=0, columnspan=2) # puts the delimiter label on the grid.

        if choice == "linesList": # returns linesList if you pass in choice 'linesList'
            return linesList
        elif choice == "fileName": # returns fileName if you pass in choice 'fileName'
            return theFileName
        elif choice == "fileType": # returns fileType if you pass in 'fileType'
            return theFileType    
        
    createMainUI() # runs the first main function which in turn runs all the other functions. some functions will run through button click events and others will run if they are called in the other functions
    # this concludes the code of my main program
        
# Calculator Program Code
def window2():
    def calcButtonClick(number): # this is a function that takes in the number you press and puts it in the window then puts the next one in the window
        current = calcEntry.get()
        calcEntry.delete(0, END)
        calcEntry.insert(0, str(current) + str(number))
        
    def calcButtonClear(): # this function clears the entry window
        calcEntry.delete(0, END)

    def calcButtonAdd(): # this function adds
        firstNumber = calcEntry.get()
        global f_num
        global math
        math = "addition"
        f_num = int(firstNumber)
        calcEntry.delete(0, END)

    def calcButtonEqual(): # this function equals everything depending on the operator used
        secondNumber = calcEntry.get()
        calcEntry.delete(0, END)

        if math == "addition":
            calcEntry.insert(0, f_num + int(secondNumber))
        if math == "subtraction":
            calcEntry.insert(0, f_num - int(secondNumber))
        if math == "multiplication":
            calcEntry.insert(0, f_num * int(secondNumber))
        if math == "division":
            calcEntry.insert(0, f_num / int(secondNumber))


    def calcButtonSubtract(): # this function subtracts
        firstNumber = calcEntry.get()
        global f_num
        global math
        math = "subtraction"
        f_num = int(firstNumber)
        calcEntry.delete(0, END)
    def calcButtonMultiply(): # this function multiplies
        firstNumber = calcEntry.get()
        global f_num
        global math
        math = "multiplication"
        f_num = int(firstNumber)
        calcEntry.delete(0, END)

    def calcButtonDivide(): # this function divides
        firstNumber = calcEntry.get()
        global f_num
        global math
        math = "division"
        f_num = int(firstNumber)
        calcEntry.delete(0, END)

    def makeCalculatorUI(): # this function creates the User Interface of the calculator
        global calcEntry # makes the display global and accessible by the other functions so it can be updated
        calculatorWindow = Window(root) # puts window widget to the calculator Window
        calculatorWindow.title("Welcome to Calculator")


        calcEntry = Entry(calculatorWindow, width=25, borderwidth=5) # this is calculator display
        # these are all buttons from 0 to 9 assigned to their variables button then the number
        # there are the other operator buttons like Clear, Equal, Add, Subtract, Multiply, Divide assigned to the correct button variable
        #  
        button1 = Button(calculatorWindow, text=1, padx=12, pady=6, command=lambda: calcButtonClick(1))
        button2 = Button(calculatorWindow, text=2, padx=12, pady=6, command=lambda: calcButtonClick(2))
        button3 = Button(calculatorWindow, text=3, padx=12, pady=6, command=lambda: calcButtonClick(3))

        button4 = Button(calculatorWindow, text=4, padx=12, pady=6, command=lambda: calcButtonClick(4))
        button5 = Button(calculatorWindow, text=5, padx=12, pady=6, command=lambda: calcButtonClick(5))
        button6 = Button(calculatorWindow, text=6, padx=12, pady=6, command=lambda: calcButtonClick(6))

        button7 = Button(calculatorWindow, text=7, padx=12, pady=6, command=lambda: calcButtonClick(7))
        button8 = Button(calculatorWindow, text=8, padx=12, pady=6, command=lambda: calcButtonClick(8))
        button9 = Button(calculatorWindow, text=9, padx=12, pady=6, command=lambda: calcButtonClick(9))
        button0 = Button(calculatorWindow, text=0, padx=12, pady=6, command=lambda: calcButtonClick(0))
        buttonClear = Button(calculatorWindow, text='C', padx=12, pady=6, command=calcButtonClear)
        buttonEquals = Button(calculatorWindow, text='=', padx=12, pady=6, command=calcButtonEqual)

        buttonPlus = Button(calculatorWindow, text='+', padx=12, pady=6, command=calcButtonAdd)
        buttonMinus = Button(calculatorWindow, text='-', padx=12, pady=6, command=calcButtonSubtract)
        buttonMultiply = Button(calculatorWindow, text='x', padx=12, pady=6, command=calcButtonMultiply)
        buttonDivide = Button(calculatorWindow, text='/', padx=12, pady=6, command=calcButtonDivide)

        # this code below here just grids the above lines in their positions on the window.
        calcEntry.grid(row=0, column=0, padx=10, pady=10, columnspan=4)


        button1.grid(row=3, column=0, padx=1, pady=1)
        button2.grid(row=3, column=1, padx=1, pady=1)
        button3.grid(row=3, column=2, padx=1, pady=1)
        buttonPlus.grid(row=3, column=3, padx=1, pady=1)

        button4.grid(row=2, column=0, padx=1, pady=1)
        button5.grid(row=2, column=1, padx=1, pady=1)
        button6.grid(row=2, column=2, padx=1, pady=1)
        buttonMinus.grid(row=2, column=3, padx=1, pady=1)

        button7.grid(row=1, column=0, padx=1, pady=1)
        button8.grid(row=1, column=1, padx=1, pady=1)
        button9.grid(row=1, column=2, padx=1, pady=1)
        buttonMultiply.grid(row=1, column=3, padx=1, pady=1)

        button0.grid(row=4, column=0, padx=1, pady=1)
        buttonClear.grid(row=4, column=1, padx=1, pady=1)
        buttonEquals.grid(row=4, column=2, padx=1, pady=1)
        buttonDivide.grid(row=4, column=3, padx=1, pady=1)
    
    
    


            


    makeCalculatorUI() # this is the function call








# Covid Program Code
def window3():
    # This function makes the main window and sets welcome label and continue and quit buttons to it.
    def covidMainWindowUI():

        covidDiagnosisWindow = Window(root)
        covidDiagnosisWindow.title("Welcome to Diagnoser of Covid")

        covidMainPageLabel = Label(covidDiagnosisWindow, text="Welcome to the covid diagnosis tool.\nPlease press continue button to continue to next page or quit button to quit").grid(row=0, column=0, columnspan=2)


        covidContinueButton = Button(covidDiagnosisWindow, text="Continue", command=covidQuestionPage).grid(row=10, column=1)
        covidQuitButton = Button(covidDiagnosisWindow, text="Quit", command=root.destroy).grid(row=10, column=0)

    
    # This function makes the Question window using window(root). adds title and a label asking to tick all symptoms fromt the list
    def covidQuestionPage():
        global covidQuestionList
        global goDoctor
        global varList
        global covidQuestionWindow

        covidQuestionWindow = Window(root)
        covidQuestionWindow.title('Answer all these questions by checking/ticking all that apply')
        covidQuestionsPageLabel = Label(covidQuestionWindow, text="Please tick all symptoms that you have from list").grid(row=0, column=0)
        #make empty varlist to store the checkbox data in a list
        varList = []
        

        totalQuestionsTrue = 0
        goDoctor = False

        #these is the nested list of questions which can be updated by any developer working with a health professional to include more symptoms to check.
        # the inner lists have one question and one 0 which means it hasnt been ticked yet, when it gets ticked it becomes a 1
        covidQuestionList = [
            ['Do you have a cough?', 0],
            ['Do you have a sore throat?', 0],
            ['Do you have a fever?', 0],
            ['Do you have pain?', 0]
        ]

        # this for loop inserts tkinter intvars into empty varList at every iteration of loop
        # also makes a checkbutton for every question in the covidQuestionList[i][0]
        # the second for loop puts each item from varList after iterating over it into the index 1 of the question q in covid questionlist.
        for i in range(len(covidQuestionList)):
            varList.insert(i, IntVar())
            covidCheckButton = Checkbutton(covidQuestionWindow, text=f"{covidQuestionList[i][0]}", variable=varList[i], onvalue=1, offvalue=0)
            covidCheckButton.grid(row=i+1, column=0)
        for item in varList:
            for q in covidQuestionList:
                q[1] = item

        
        # this is the button that runs the function showCovidDiagnosis()
        covidDiagnoseButton = Button(covidQuestionWindow, text="Show diagnosis", command=showCovidDiagnosis)
        covidDiagnoseButton.grid(row=40, column=0)
        

        # this function shows after you press the covid diagnosis button, it counts the ticked checkboxes.
    def showCovidDiagnosis():
        #making global variables so its accessible outside this particular function
        global covidQuestionList
        global varList
        global goDoctor
        # set a symtom count variable.
        # set a empty list to take in all the 0, and 1s to sum later.
        covidSymptomCount = 0
        listToSum = []

        # 1 this for loop was meant to go over each question with each 1 or 0, to see if its a 1 or a zero then it was meant to add one to the covidSymptom count BUT i used another way
        for q in covidQuestionList:
            if q[1].get() == 1:
                covidSymptomCount += 1
            elif q[1].get() == 0:
                continue

        # 2 this is the other way that works better, it goes through varlist then appends each item after getting them from each intvar() which is stored in that item.
        # then makes the covid symptom count equal to the sum of everything in that list.
        for i in varList:
            listToSum.append(i.get())
        covidSymptomCount = sum(listToSum)


        # this is the diagnosis message and the diagnosis message changes based on how many boxes you checked, right now its set to some messages but these numbers and messages can be changed as you increase the question list and the developer and health care professional should work together to decide the best diagnoses messages and symtopm counts
        if covidSymptomCount == 0:
            covidMsg = 'You should stay at home but you dont have any symptoms of covid'
            goDoctor == False
        elif covidSymptomCount < 3:
            covidMsg = 'You should see a doctor if your symptoms get worse'
        elif covidSymptomCount >= 3:
            covidMsg = 'You should see a doctor ASAP'
            goDoctor == True

        #this is the diagnosis string placed on the screen using a tkinter Label
        diagLabel = Label(covidQuestionWindow, text=f"You have {covidSymptomCount} Covid Symptoms. {covidMsg}")
        diagLabel.grid(row=10, column=0)
            
    covidMainWindowUI()    # function call






def our_command(): # this is a dummy function that doesnt do anything its to use for testing button click events.
    pass







my_menu = Menu(root) # create menu
root.config(menu=my_menu) # configure menu

# about message for message box
aboutMessage = """
    Version: 2.00
"""


#Create a menu item

program_menu = Menu(my_menu) # assign menu widget to program menu variable
my_menu.add_cascade(label="Programs", menu=program_menu)# add program menu to cascade 
program_menu.add_command(label="Search Program", command=window1) # add three commands to program menu, these commands are the functions for each search
program_menu.add_command(label="Calculator", command=window2)
program_menu.add_command(label="Covid Diagnoser", command=window3)

#Create an help Menu Item

help_menu = Menu(my_menu) # add Menu widget to help menu variable which connects opens a pdf in the broswer from the link provided in the openHelp function's paramter as an argument.
my_menu.add_cascade(label="Help", menu=help_menu) # adds help menu cascade to the main manu which is called my menu
help_menu.add_command(label="Help page", command=lambda: messagebox.showinfo("Software", aboutMessage))# this menu item has a command that opens the broswer and loads the given address

#Create an about Menu Item

about_menu = Menu(my_menu) # add menu widget to about menu variable
my_menu.add_cascade(label="About", menu=about_menu) # adds about menu to the cascade
about_menu.add_command(label="About", command=lambda: messagebox.showinfo("Software", aboutMessage)) # the about menu adds comand which requiores a lambda and in the comand is teh messagebox and it shows my 'company name' and about message

# creating exit menu item

exit_menu = Menu(my_menu) # add menu widget to exit menu variable
my_menu.add_cascade(label="Exit Menu", menu=exit_menu) # add to cascade
exit_menu.add_command(label="Close", command=root.destroy) # root.quit in the command makes the window quit




root.mainloop()


