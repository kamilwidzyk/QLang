from dataclasses import dataclass
from logger import log, WARNING, SC_ER, DEBUG
import colorama
from typing import Any, Self

class ScriptErrors:
    script: str = None # QLang code


    @dataclass
    class Position:
        """
        Represents an area in a text file as two points
        """
        

        @dataclass
        class Point:
            """
            Represents one point in a text file as (line, column)
            """
            line: int = None
            col: int = None

        start = Point()
        end = Point()

        def __init__(
                self, start_line: int = None, start_col: int = None, 
                end_line: int = None, end_col: int = None,
                start_point: Point = None, end_point = None,
                width: int = None):
            """
            Inits position by passing:
            A start point: as start_point or start_line and start_col
            An end point: as end_point, end_line and end_col, or width
                        
            Parameters:
                start_line (int): Line number at the start (inclusive)
                start_col (int): Column number at the start (incluside)
                end_line (int): Line number at the end (exclusive)
                end_col (int): Column number at the end (exclusive)
                start_point (Point): Start line and col given as Point
                end_point (Point): End line and col given as Point
                width (int): amount of characters to the right from the start
            """            
            if start_point is None:
                if start_line is None or start_col is None:
                    log(SC_ER, WARNING, "Position initialized with no start point specified!")
                    return
                self.start.line = start_line
                self.start.col = start_col
            else:
                self.start = start_point

            if end_point is None:
                if width is None:
                    if end_line is None or end_col is None:
                        log(SC_ER, WARNING, "Position initialized with no end point specified!")
                        return
                    
                    self.end.line = end_line
                    self.end.col = end_col
                else:
                    if self.start.line is None or self.start.col is None:
                        return # no need to log again, there was a warning before for this
                    self.end.line = self.start.line
                    self.end.col = self.start.col + width
            else:
                self.end = end_point

        @classmethod
        def extract(cls, node: Any) -> Self:
            """
            Tries to extract position from a given node

            Possible combinations of specified fields:
            1. line, column, endLine, endColumn
            2. line, column, text
            3. line, column -> ends will be set with the same values
            None of the above: returns a position with all values set to -1
            """
            line = None
            column = None
            end_line = None
            end_column = None
            width = None

            if "line" in node:
                line = node["line"]
            if "column" in node:
                column = node["column"]
            if "endLine" in node:
                end_line = node["endLine"]
            if "endColumn" in node:
                end_column = node["endColumn"]
            if "text" in node:
                width = len(node["text"])


            if (line is not None) and (column is not None) and \
               (end_line is not None) and (end_column is not None):
                return cls(start_line=line, start_col=column, end_line=end_line, end_col=end_column)
            elif (line is not None) and (column is not None) and (width is not None):
                return cls(start_line=line, start_col=column, width=width)
            elif (line is not None) and (column is not None):
                return cls(start_line=line, start_col=column, end_line=line, end_column=column)
            else:
                return cls(start_line=-1, start_col=-1, end_line=-1, end_column=-1)
        
            

        def width(self) -> int:
            """
            Calculate the text width

            Returns:
                int: number of columns
            """
            return self.end.col - self.start.col
        

        def height(self) -> int:
            """
            Calculate the text height

            Returns:
                int: number of lines
            """
            return self.end.line - self.start.line + 1

    UNKNOWN_POSITION = Position(-1, -1, -1, -1)

        

    def __init__(self, script: str):
        """
        Stores the script content in this class for displaying the code error message with the code context

        Parameters:
            script (str): Content of QLang script file
        """
        self.script = script

    def showError(self, pos: Position, msg: str):
        """
        This is the function that will get called when some error during the script execution occurs

        Parameters:
            pos (Position): Where in the original script it happend
            msg (str): Message to show
        """
        log(SC_ER, DEBUG, f"Error parameters: start_line={pos.start.line} start_col={pos.start.line} end_line={pos.end.line} end_col={pos.end.col} msg={msg}")


        # TODO: Make it actually include few lines of nearby code as context and mark the actual position of the error
        print(colorama.Style.RESET_ALL + "\n\n\n ---------- RUNTIME ERROR ----------")
        print("Start line: ", pos.start.line)
        print("Start col: ", pos.start.col)
        print("End line: ", pos.end.line)
        print("End col: ", pos.end.col)
        print("Message: ", msg)
        print("----------------------------------------------------")
