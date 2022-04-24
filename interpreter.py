"""This class implements a BASIC interpreter that
presents a prompt to the user. The user may input
program statements, list them and run the program.
The program may also be saved to disk and loaded
again.

"""

from basictoken import BASICToken as Token
from lexer import Lexer
from program import Program
from sys import stderr


def main():

    banner = (
        """
+-------------------------------------+
           ,ggg,  
          dP""8I  
         dP   88       __   __
        dP    88     _|  |_|__|_
       ,8'    88    | |  | |  | |
       d88888888    |_|  |_|__|_|
 __   ,8"     88     _|__|_|  |_ 
dP"  ,8P      Y8    | |  | |  | |
Yb,_,dP       `8b,  |_|__|_|  |_|
 "Y8P"         `Y8    |__| |__|
+-------------------------------------+
"The Flintstones programming language."
        """)

    print(banner)

    lexer = Lexer()
    program = Program()

    # Continuously accept user input and act on it until
    # the user enters 'EXIT'
    while True:

        stmt = input('> ')

        try:
            tokenlist = lexer.tokenize(stmt)

            # Execute commands directly, otherwise
            # add program statements to the stored
            # BASIC program

            if len(tokenlist) > 0:

                # Exit the interpreter
                if tokenlist[0].category == Token.EXIT:
                    break

                # Add a new program statement, beginning
                # a line number
                elif tokenlist[0].category == Token.UNSIGNEDINT\
                    and len(tokenlist) > 1:
                    program.add_stmt(tokenlist)

                # Delete a statement from the program
                elif tokenlist[0].category == Token.UNSIGNEDINT \
                        and len(tokenlist) == 1:
                    program.delete_statement(int(tokenlist[0].lexeme))

                # Execute the program
                elif tokenlist[0].category == Token.RUN:
                    try:
                        program.execute()

                    except KeyboardInterrupt:
                        print("Program terminated")

                # List the program
                elif tokenlist[0].category == Token.LIST:
                    if len(tokenlist) == 2:
                        program.list(int(tokenlist[1].lexeme),int(tokenlist[1].lexeme))
                    elif len(tokenlist) == 3:
                        # if we have 3 tokens, it might be LIST x y for a range
                        # or LIST -y or list x- for a start to y, or x to end
                        if tokenlist[1].lexeme == "-":
                            program.list(None, int(tokenlist[2].lexeme))
                        elif tokenlist[2].lexeme == "-":
                            program.list(int(tokenlist[1].lexeme), None)
                        else:
                            program.list(int(tokenlist[1].lexeme),int(tokenlist[2].lexeme))
                    elif len(tokenlist) == 4:
                        # if we have 4, assume LIST x-y or some other
                        # delimiter for a range
                        program.list(int(tokenlist[1].lexeme),int(tokenlist[3].lexeme))
                    else:
                        program.list()

                # Save the program to disk
                elif tokenlist[0].category == Token.SAVE:
                    program.save(tokenlist[1].lexeme)
                    print("Program written to file")

                # Load the program from disk
                elif tokenlist[0].category == Token.LOAD:
                    program.load(tokenlist[1].lexeme)
                    print("Program read from file")

                # Delete the program from memory
                elif tokenlist[0].category == Token.NEW:
                    program.delete()

                # Unrecognised input
                else:
                    print("Unrecognised input", file=stderr)
                    for token in tokenlist:
                        token.print_lexeme()
                    print(flush=True)

        # Trap all exceptions so that interpreter
        # keeps running
        except Exception as e:
            print(e, file=stderr, flush=True)


if __name__ == "__main__":
    main()
