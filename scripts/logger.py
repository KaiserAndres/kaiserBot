'''
    Title: Logger
    Author: Andrés Villagra de la Fuente
    Creation date: 15:51 05/01/2016 (GMT-3)
    Last edit: 15:51 05/01/2016 (GMT-3)
    Version: 0.1

    Description:
        This is a loggin library for irc log making. This script will output a 
    .log file. *.log is an HTML document of a conversation formated with css.
'''

def Make_Nake():

def Write_Log_Line(name, colour, text):

def Load_Colours():
    '''
        This function opens the user.colours file which contains the user name
    and a hex colour in this format:
        "<NAME> : <COLOUR>\n"
        This goes through the file line by line and separates the name and
    colour.

        Returns:
            Dictionary with the user names and the hex colours for each
    '''

    Colour_File = open("user.colours", "r")
    doc = Colour_File.readlines()
    Colour_Hex_Values = {}

    for user in doc:
        name = ''
        colour = ''
        Name_End = False
        for character in user:
            if character != '' and not Name_End:
                name = name + character
            if character == '' and not Name_End:
                Name_End = True
            if character != '' and Name_End and character != '\n'
                colour = colour + character
        Colour_Hex_Values[name] = colour

    return Colour_Hex_Values        

def Add_Colour(user, HEX_Colour):
    



