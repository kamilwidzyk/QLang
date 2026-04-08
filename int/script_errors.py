from dataclasses import dataclass
import colorama
from typing import Any, Self, List

from .logger import log, WARNING, SC_ER, DEBUG
"""
Type of errors:
  > DEEP ERROR: This might not be related to your program, but to the interpreter.
                Or might be a very strange syntax error.
  > SYNTAX ERROR: You know what this is
  > RUNTIME ERROR: Not allowed operation/Other problem
"""

"""
Tu będzie bardziej posprzątane jak będzie pewność, że wszystko wyświetla się poprawnie
"""
# TODO: Clean up this class and divide the showError into shorter methods
# TODO: Maybe add syntax highlighting(keywords, comments)

class ScriptErrors:
    lines: List[str] = [] # QLang code split to lines


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

        def has_end(self) -> bool:
            """
            Returns True if end Point is specified
            """
            return self.end.col != None and self.end.line != None and \
                   self.end.col != -1 and self.end.line != -1
        
        def has_start(self) -> bool:
            """
            Returns True if start Point is specified
            """
            return self.start.col != None and self.start.line != None and \
                   self.start.col != -1 and self.start.line != -1

        def is_single_line(self) -> bool:
            """
            Returns true is Position spans over a single line
            """
            return not self.has_end() or self.start.line == self.end.line
        
        
        def is_defined(self) -> bool:
            """
            Returns true if at least a start point is specified
            """
            return self.has_start()
        
        def start_line(self) -> int:
            """
            Returns starting line number
            """
            return self.start.line
        
        def end_line(self) -> int:
            """
            Returns ending line number
            """
            return self.end.line if self.has_end() else self.start_line()
        
        def start_col(self) -> int:
            """
            Returns starting column number
            """
            return self.start.col
        
        def end_col(self) -> int:
            """
            Returns ending column number
            """
            return self.end.col if self.has_end() else self.start_col()

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

            

            # start and end is known
            if (line is not None) and (column is not None) and \
               (end_line is not None) and (end_column is not None):
                if(line > end_line):
                    line, end_line = end_line, line
                if(column > end_column):
                    column, end_column = end_column, column
                return cls(start_line=line, start_col=column, end_line=end_line, end_col=end_column)
            elif (line is not None) and (column is not None) and (width is not None): # start and width known
                return cls(start_line=line, start_col=column, width=width)
            elif (line is not None) and (column is not None): # only start known -> start = end
                if(line > end_line):
                    line, end_line = end_line, line
                if(column > end_column):
                    column, end_column = end_column, column
                return cls(start_line=line, start_col=column, end_line=line, end_col=column)
            else: # unknown
                return cls(start_line=-1, start_col=-1, end_line=-1, end_col=-1)
        
            

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
        self.lines = script.split('\n')

    def showError(self, pos: Position, error_type: str, title: str, msg: str):
        """
        This is the function that will get called when some error during the script execution occurs

        Box-drawing characters from: https://en.wikipedia.org/wiki/Box-drawing_characters

        Parameters:
            pos (Position): Where in the original script it happend
            error_type (str): Type of the shows error(sytax/runtime/deep)
            title (str): Short title
            msg (str): Message to show
        """
        log(SC_ER, DEBUG, f"Error parameters: start_line={pos.start.line} start_col={pos.start.col} end_line={pos.end.line} end_col={pos.end.col} msg={msg}")

        # Width is calculated based on the min of:
        #   - type + title
        #   - msg
        #   - length of script lines
        # Error provides 3 lines up and 3 lines down of script context(if possible)
        # UNKNOWN position is displayed as 'Can't find it, look for it yourself'
        # Box is red, background is default, type is yellow, msg is bright white(padding L and R 3char)
        # Script context is normal white
        # If only line number known, highligh whole line as red background and black text
        # else highlight the specified range 
        # line numbers are cyan/blue (width is calculated auto, min 3 chars, align right)
        """
        ┏━━━━━━━━━━━━...━━━━━━━━━━━━━┓
        ┃     <type>: <title>        ┃ (Text is centered, padding 3)
        ┡━━━━━━━━━━━━...━━━━━━━━━━━━━┩
        │   <msg>                    │ (Text is centered, padding 3)
        ├───┬────────...─────────────┤
        │  1│                        │	
        │  2│	                     │
        │  3│	                     │
        │  4│	                     │
        │  5│	                     │
        │  6│	                     │
        │  7│	                     │
        ╰───┴────────────────────────╯
        """

        # minimal widths of each section
        type_title_width = 3 + len(error_type) + 2 + len(title) + 3
        msg_width = 3 + len(msg) + 3
        context_width = None # this will be calculated later

        # This will be displayed when position is undefined/unknown
        UNKNOWN_MESSAGE = "Can't find it, look for it yourself"

        position_known = True

        context_lines = [] # array of lines of code as strings
        line_number_start = None # number of first displayed line
        line_number_end = None # number of last displayed line
        line_number_width = None # width of line number column
        CONTEXT_SIZE_UP = 3 # how much lines to show above error(const)
        CONTEXT_SIZE_DOWN = 3 # how much lines to show below error(const)


        if pos.is_defined():
            # Position is defined, script context can be displayed
            line_number_start = max(
                pos.start_line() - CONTEXT_SIZE_UP, 1
            )
            line_number_end = min(
                pos.end_line() + CONTEXT_SIZE_DOWN, len(self.lines)
            )
            context_lines = self.lines[line_number_start-1 : line_number_end]

            # Calculate context section width (including line number width)
            text_width = len(max(context_lines, key=len)) if context_lines else 0
            line_number_width = max(
                len(str(line_number_start)), len(str(line_number_end)), 3
            )
            context_width = line_number_width + 1 + text_width + 1

        else:
            # Position is unknown, can't display the script context
            position_known = False
            context_width = 1 + len(UNKNOWN_MESSAGE) + 1

        window_width = max(type_title_width, msg_width, context_width)

        style_red_border =  colorama.Style.BRIGHT + colorama.Fore.RED + colorama.Back.RESET
        style_type = colorama.Style.BRIGHT + colorama.Fore.YELLOW + colorama.Back.RESET
        style_white_bright = colorama.Style.BRIGHT + colorama.Fore.WHITE + colorama.Back.RESET
        style_white_normal = colorama.Style.NORMAL + colorama.Fore.WHITE + colorama.Back.RESET
        style_line_number = colorama.Style.NORMAL + colorama.Fore.CYAN + colorama.Back.RESET
        style_highlight = colorama.Style.BRIGHT + colorama.Fore.BLACK + colorama.Back.YELLOW


        type_margin_left = (window_width - type_title_width) // 2
        type_margin_right = window_width - type_title_width - type_margin_left

        msg_margin_left = (window_width - msg_width) // 2
        msg_margin_right = window_width - msg_width - msg_margin_left

        print()
        print(style_red_border + "┏" + "━" * window_width + "┓")
        print("┃   " + " "*type_margin_left + style_type + error_type + 
              style_white_bright + ": " + title +  style_red_border + " "*type_margin_right + "   ┃")
        print(style_red_border + "┡" + "━" * window_width + "┩")
        print("│   " + " "*msg_margin_left + style_white_normal + msg + " "*msg_margin_right + 
              style_red_border + "   │")
        
        if position_known:
            print("├" + "─"*line_number_width + "┬" + "─"*(window_width-line_number_width-1) + "┤")

            for i in range(len(context_lines)):
                line_number = line_number_start + i
                line_number_margin_left = line_number_width - len(str(line_number))

                current_line = context_lines[i]
                highlight_start = None # None = no highlight at this line
                highlight_end = None # None = highlight to the end of this line

                if pos.is_single_line() and line_number == pos.start_line():
                    highlight_start = pos.start_col()
                    highlight_end = pos.end_col()
                elif not pos.is_single_line() and \
                     (line_number >= pos.start_line() and line_number <= pos.end_line()):
                    
                    if line_number == pos.start_line():
                        # This is the first line of highlight, start at specified col
                        # and highlight to the end of this line
                        highlight_start = pos.start_col()
                        highlight_end = None
                    elif line_number == pos.end_line():
                        # This is the last line of highlight, start and the beginning
                        # and highlight to the specified col
                        highlight_start = 0
                        highlight_end = pos.end_col()
                    else:
                        # This is a line in the middle
                        # highlight the whole line
                        highlight_start = 0
                        highlight_end = None

                line_normal_left = ""
                line_highlight = ""
                line_normal_right = ""

                if highlight_start != None:
                    line_normal_left = current_line[:highlight_start]
                    if highlight_end != None:
                        line_highlight = current_line[highlight_start:highlight_end]
                        line_normal_right = current_line[highlight_end:]
                    else:
                        line_highlight = current_line[highlight_start:]
                else:
                    line_normal_left = current_line

                    

                context_margin_right = window_width - line_number_width - 1 - len(context_lines[i]) - 1
                line_with_highlight = style_white_normal + line_normal_left + \
                                      style_highlight + line_highlight + \
                                      style_white_normal + line_normal_right


                print(style_red_border + "│" + " "*line_number_margin_left + style_line_number +
                      str(line_number) + style_red_border + "│" + line_with_highlight + " "*context_margin_right + style_red_border +" │")

            print("╰" + "─"*line_number_width + "┴" + "─"*(window_width-line_number_width-1) + "╯")

        else:
            unknown_margin_left = (window_width - context_width) // 2
            unknown_margin_right = window_width - context_width - unknown_margin_left

            print("├" + "─"*window_width + "┤")
            print("│ " + " "*unknown_margin_left + style_white_normal + UNKNOWN_MESSAGE + 
                  " "*unknown_margin_right + style_red_border + " │")
            print("╰" + "─"*window_width + "╯")
        


