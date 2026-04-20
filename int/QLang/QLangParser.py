# Generated from ../QLang/QLang.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,80,495,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,1,0,5,0,64,8,0,10,0,12,0,
        67,9,0,1,0,1,0,1,1,1,1,1,1,3,1,74,8,1,1,2,1,2,1,2,1,2,5,2,80,8,2,
        10,2,12,2,83,9,2,1,2,1,2,1,3,1,3,3,3,89,8,3,1,4,1,4,1,4,1,4,3,4,
        95,8,4,1,4,1,4,1,4,1,5,1,5,1,5,5,5,103,8,5,10,5,12,5,106,9,5,1,6,
        1,6,1,6,1,6,1,6,3,6,113,8,6,1,7,1,7,5,7,117,8,7,10,7,12,7,120,9,
        7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,
        8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,163,8,8,1,8,1,8,1,8,3,
        8,168,8,8,1,9,1,9,1,9,1,9,5,9,174,8,9,10,9,12,9,177,9,9,1,9,1,9,
        1,9,1,9,3,9,183,8,9,1,10,1,10,1,10,1,10,1,10,3,10,190,8,10,1,11,
        1,11,1,11,1,11,5,11,196,8,11,10,11,12,11,199,9,11,1,11,1,11,1,11,
        1,11,1,11,1,11,3,11,207,8,11,1,11,1,11,3,11,211,8,11,1,12,1,12,1,
        12,1,12,1,12,3,12,218,8,12,1,13,1,13,1,13,1,13,1,13,1,13,3,13,226,
        8,13,1,13,1,13,3,13,230,8,13,1,14,1,14,1,14,1,14,1,14,1,14,3,14,
        238,8,14,1,14,1,14,5,14,242,8,14,10,14,12,14,245,9,14,1,15,1,15,
        1,15,1,15,3,15,251,8,15,1,16,1,16,1,16,1,16,1,16,1,16,3,16,259,8,
        16,1,16,1,16,1,16,1,16,3,16,265,8,16,1,17,1,17,1,17,1,17,1,17,1,
        17,3,17,273,8,17,1,17,1,17,1,17,1,17,1,17,1,17,3,17,281,8,17,1,17,
        1,17,1,17,1,17,1,17,1,17,3,17,289,8,17,1,17,1,17,1,17,1,17,1,17,
        1,17,3,17,297,8,17,1,17,1,17,1,17,1,17,1,17,3,17,304,8,17,3,17,306,
        8,17,1,18,1,18,1,19,1,19,1,20,1,20,1,20,1,20,1,20,3,20,317,8,20,
        1,20,1,20,1,20,1,20,1,20,1,20,1,20,3,20,326,8,20,1,21,1,21,1,21,
        1,21,1,21,3,21,333,8,21,1,21,1,21,1,21,1,22,1,22,1,22,3,22,341,8,
        22,1,22,1,22,1,23,1,23,1,23,1,23,1,23,1,23,1,23,3,23,352,8,23,1,
        24,1,24,1,24,1,24,1,24,1,24,1,24,1,24,3,24,362,8,24,1,24,1,24,1,
        25,1,25,1,25,1,25,1,25,1,25,1,26,1,26,1,26,1,26,1,26,3,26,377,8,
        26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,3,26,386,8,26,3,26,388,8,26,
        1,26,1,26,1,26,1,26,1,26,1,26,1,26,1,26,3,26,398,8,26,1,26,1,26,
        1,26,1,26,1,26,1,26,1,26,1,26,3,26,408,8,26,1,26,1,26,3,26,412,8,
        26,1,26,1,26,3,26,416,8,26,1,26,3,26,419,8,26,1,27,1,27,1,27,1,27,
        1,27,1,27,1,27,1,27,1,27,1,27,1,27,3,27,432,8,27,1,28,1,28,1,29,
        1,29,1,29,5,29,439,8,29,10,29,12,29,442,9,29,1,30,1,30,1,30,1,30,
        1,30,1,30,3,30,450,8,30,1,30,1,30,1,30,1,30,1,30,1,30,3,30,458,8,
        30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,3,30,467,8,30,1,30,1,30,1,
        30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,30,1,
        30,1,30,1,30,1,30,1,30,1,30,5,30,490,8,30,10,30,12,30,493,9,30,1,
        30,0,1,60,31,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
        38,40,42,44,46,48,50,52,54,56,58,60,0,10,1,0,16,17,2,0,75,75,77,
        77,1,0,20,29,1,0,30,33,1,0,35,36,1,0,56,57,1,0,3,5,1,0,6,7,1,0,8,
        11,1,0,12,13,544,0,65,1,0,0,0,2,73,1,0,0,0,4,75,1,0,0,0,6,88,1,0,
        0,0,8,90,1,0,0,0,10,99,1,0,0,0,12,107,1,0,0,0,14,114,1,0,0,0,16,
        167,1,0,0,0,18,182,1,0,0,0,20,184,1,0,0,0,22,210,1,0,0,0,24,212,
        1,0,0,0,26,219,1,0,0,0,28,231,1,0,0,0,30,250,1,0,0,0,32,252,1,0,
        0,0,34,305,1,0,0,0,36,307,1,0,0,0,38,309,1,0,0,0,40,311,1,0,0,0,
        42,327,1,0,0,0,44,337,1,0,0,0,46,344,1,0,0,0,48,353,1,0,0,0,50,365,
        1,0,0,0,52,418,1,0,0,0,54,431,1,0,0,0,56,433,1,0,0,0,58,435,1,0,
        0,0,60,466,1,0,0,0,62,64,3,2,1,0,63,62,1,0,0,0,64,67,1,0,0,0,65,
        63,1,0,0,0,65,66,1,0,0,0,66,68,1,0,0,0,67,65,1,0,0,0,68,69,5,0,0,
        1,69,1,1,0,0,0,70,74,3,4,2,0,71,74,3,8,4,0,72,74,3,16,8,0,73,70,
        1,0,0,0,73,71,1,0,0,0,73,72,1,0,0,0,74,3,1,0,0,0,75,76,5,52,0,0,
        76,77,5,77,0,0,77,81,5,62,0,0,78,80,3,6,3,0,79,78,1,0,0,0,80,83,
        1,0,0,0,81,79,1,0,0,0,81,82,1,0,0,0,82,84,1,0,0,0,83,81,1,0,0,0,
        84,85,5,63,0,0,85,5,1,0,0,0,86,89,3,8,4,0,87,89,3,16,8,0,88,86,1,
        0,0,0,88,87,1,0,0,0,89,7,1,0,0,0,90,91,5,39,0,0,91,92,5,77,0,0,92,
        94,5,60,0,0,93,95,3,10,5,0,94,93,1,0,0,0,94,95,1,0,0,0,95,96,1,0,
        0,0,96,97,5,61,0,0,97,98,3,14,7,0,98,9,1,0,0,0,99,104,3,12,6,0,100,
        101,5,66,0,0,101,103,3,12,6,0,102,100,1,0,0,0,103,106,1,0,0,0,104,
        102,1,0,0,0,104,105,1,0,0,0,105,11,1,0,0,0,106,104,1,0,0,0,107,108,
        7,0,0,0,108,112,5,77,0,0,109,110,5,64,0,0,110,111,5,76,0,0,111,113,
        5,65,0,0,112,109,1,0,0,0,112,113,1,0,0,0,113,13,1,0,0,0,114,118,
        5,62,0,0,115,117,3,16,8,0,116,115,1,0,0,0,117,120,1,0,0,0,118,116,
        1,0,0,0,118,119,1,0,0,0,119,121,1,0,0,0,120,118,1,0,0,0,121,122,
        5,63,0,0,122,15,1,0,0,0,123,124,3,18,9,0,124,125,5,67,0,0,125,168,
        1,0,0,0,126,127,3,22,11,0,127,128,5,67,0,0,128,168,1,0,0,0,129,130,
        3,26,13,0,130,131,5,67,0,0,131,168,1,0,0,0,132,133,3,28,14,0,133,
        134,5,67,0,0,134,168,1,0,0,0,135,136,3,32,16,0,136,137,5,67,0,0,
        137,168,1,0,0,0,138,139,3,34,17,0,139,140,5,67,0,0,140,168,1,0,0,
        0,141,142,3,40,20,0,142,143,5,67,0,0,143,168,1,0,0,0,144,145,3,42,
        21,0,145,146,5,67,0,0,146,168,1,0,0,0,147,148,3,44,22,0,148,149,
        5,67,0,0,149,168,1,0,0,0,150,168,3,46,23,0,151,168,3,48,24,0,152,
        168,3,50,25,0,153,154,3,52,26,0,154,155,5,67,0,0,155,168,1,0,0,0,
        156,157,5,46,0,0,157,168,5,67,0,0,158,159,5,47,0,0,159,168,5,67,
        0,0,160,162,5,40,0,0,161,163,3,60,30,0,162,161,1,0,0,0,162,163,1,
        0,0,0,163,164,1,0,0,0,164,168,5,67,0,0,165,168,3,14,7,0,166,168,
        5,67,0,0,167,123,1,0,0,0,167,126,1,0,0,0,167,129,1,0,0,0,167,132,
        1,0,0,0,167,135,1,0,0,0,167,138,1,0,0,0,167,141,1,0,0,0,167,144,
        1,0,0,0,167,147,1,0,0,0,167,150,1,0,0,0,167,151,1,0,0,0,167,152,
        1,0,0,0,167,153,1,0,0,0,167,156,1,0,0,0,167,158,1,0,0,0,167,160,
        1,0,0,0,167,165,1,0,0,0,167,166,1,0,0,0,168,17,1,0,0,0,169,170,5,
        16,0,0,170,175,3,20,10,0,171,172,5,66,0,0,172,174,3,20,10,0,173,
        171,1,0,0,0,174,177,1,0,0,0,175,173,1,0,0,0,175,176,1,0,0,0,176,
        183,1,0,0,0,177,175,1,0,0,0,178,179,5,16,0,0,179,180,5,77,0,0,180,
        181,5,73,0,0,181,183,5,18,0,0,182,169,1,0,0,0,182,178,1,0,0,0,183,
        19,1,0,0,0,184,189,5,77,0,0,185,186,5,64,0,0,186,187,3,60,30,0,187,
        188,5,65,0,0,188,190,1,0,0,0,189,185,1,0,0,0,189,190,1,0,0,0,190,
        21,1,0,0,0,191,192,5,17,0,0,192,197,3,24,12,0,193,194,5,66,0,0,194,
        196,3,24,12,0,195,193,1,0,0,0,196,199,1,0,0,0,197,195,1,0,0,0,197,
        198,1,0,0,0,198,211,1,0,0,0,199,197,1,0,0,0,200,201,5,17,0,0,201,
        206,5,77,0,0,202,203,5,64,0,0,203,204,3,60,30,0,204,205,5,65,0,0,
        205,207,1,0,0,0,206,202,1,0,0,0,206,207,1,0,0,0,207,208,1,0,0,0,
        208,209,5,73,0,0,209,211,3,60,30,0,210,191,1,0,0,0,210,200,1,0,0,
        0,211,23,1,0,0,0,212,217,5,77,0,0,213,214,5,64,0,0,214,215,3,60,
        30,0,215,216,5,65,0,0,216,218,1,0,0,0,217,213,1,0,0,0,217,218,1,
        0,0,0,218,25,1,0,0,0,219,220,5,19,0,0,220,225,5,77,0,0,221,222,5,
        64,0,0,222,223,3,60,30,0,223,224,5,65,0,0,224,226,1,0,0,0,225,221,
        1,0,0,0,225,226,1,0,0,0,226,229,1,0,0,0,227,228,5,73,0,0,228,230,
        3,60,30,0,229,227,1,0,0,0,229,230,1,0,0,0,230,27,1,0,0,0,231,232,
        7,0,0,0,232,237,5,77,0,0,233,234,5,64,0,0,234,235,3,60,30,0,235,
        236,5,65,0,0,236,238,1,0,0,0,237,233,1,0,0,0,237,238,1,0,0,0,238,
        239,1,0,0,0,239,243,5,54,0,0,240,242,3,30,15,0,241,240,1,0,0,0,242,
        245,1,0,0,0,243,241,1,0,0,0,243,244,1,0,0,0,244,29,1,0,0,0,245,243,
        1,0,0,0,246,247,5,42,0,0,247,251,7,1,0,0,248,249,5,55,0,0,249,251,
        5,75,0,0,250,246,1,0,0,0,250,248,1,0,0,0,251,31,1,0,0,0,252,253,
        5,53,0,0,253,258,5,77,0,0,254,255,5,64,0,0,255,256,3,60,30,0,256,
        257,5,65,0,0,257,259,1,0,0,0,258,254,1,0,0,0,258,259,1,0,0,0,259,
        260,1,0,0,0,260,261,5,43,0,0,261,264,7,1,0,0,262,263,5,55,0,0,263,
        265,5,75,0,0,264,262,1,0,0,0,264,265,1,0,0,0,265,33,1,0,0,0,266,
        267,3,36,18,0,267,272,5,77,0,0,268,269,5,64,0,0,269,270,3,60,30,
        0,270,271,5,65,0,0,271,273,1,0,0,0,272,268,1,0,0,0,272,273,1,0,0,
        0,273,306,1,0,0,0,274,275,3,38,19,0,275,280,5,77,0,0,276,277,5,64,
        0,0,277,278,3,60,30,0,278,279,5,65,0,0,279,281,1,0,0,0,280,276,1,
        0,0,0,280,281,1,0,0,0,281,282,1,0,0,0,282,283,5,72,0,0,283,288,5,
        77,0,0,284,285,5,64,0,0,285,286,3,60,30,0,286,287,5,65,0,0,287,289,
        1,0,0,0,288,284,1,0,0,0,288,289,1,0,0,0,289,306,1,0,0,0,290,291,
        5,34,0,0,291,296,5,77,0,0,292,293,5,64,0,0,293,294,3,60,30,0,294,
        295,5,65,0,0,295,297,1,0,0,0,296,292,1,0,0,0,296,297,1,0,0,0,297,
        298,1,0,0,0,298,303,5,77,0,0,299,300,5,64,0,0,300,301,3,60,30,0,
        301,302,5,65,0,0,302,304,1,0,0,0,303,299,1,0,0,0,303,304,1,0,0,0,
        304,306,1,0,0,0,305,266,1,0,0,0,305,274,1,0,0,0,305,290,1,0,0,0,
        306,35,1,0,0,0,307,308,7,2,0,0,308,37,1,0,0,0,309,310,7,3,0,0,310,
        39,1,0,0,0,311,316,5,77,0,0,312,313,5,64,0,0,313,314,3,60,30,0,314,
        315,5,65,0,0,315,317,1,0,0,0,316,312,1,0,0,0,316,317,1,0,0,0,317,
        318,1,0,0,0,318,319,5,73,0,0,319,320,7,4,0,0,320,325,5,77,0,0,321,
        322,5,64,0,0,322,323,3,60,30,0,323,324,5,65,0,0,324,326,1,0,0,0,
        325,321,1,0,0,0,325,326,1,0,0,0,326,41,1,0,0,0,327,332,5,77,0,0,
        328,329,5,64,0,0,329,330,3,60,30,0,330,331,5,65,0,0,331,333,1,0,
        0,0,332,328,1,0,0,0,332,333,1,0,0,0,333,334,1,0,0,0,334,335,5,73,
        0,0,335,336,3,60,30,0,336,43,1,0,0,0,337,338,5,77,0,0,338,340,5,
        60,0,0,339,341,3,58,29,0,340,339,1,0,0,0,340,341,1,0,0,0,341,342,
        1,0,0,0,342,343,5,61,0,0,343,45,1,0,0,0,344,345,5,37,0,0,345,346,
        5,60,0,0,346,347,3,60,30,0,347,348,5,61,0,0,348,351,3,14,7,0,349,
        350,5,38,0,0,350,352,3,14,7,0,351,349,1,0,0,0,351,352,1,0,0,0,352,
        47,1,0,0,0,353,354,5,41,0,0,354,355,5,77,0,0,355,356,5,42,0,0,356,
        357,3,60,30,0,357,358,5,43,0,0,358,361,3,60,30,0,359,360,5,44,0,
        0,360,362,3,60,30,0,361,359,1,0,0,0,361,362,1,0,0,0,362,363,1,0,
        0,0,363,364,3,14,7,0,364,49,1,0,0,0,365,366,5,45,0,0,366,367,5,60,
        0,0,367,368,3,60,30,0,368,369,5,61,0,0,369,370,3,14,7,0,370,51,1,
        0,0,0,371,372,5,48,0,0,372,373,5,60,0,0,373,376,3,60,30,0,374,375,
        5,66,0,0,375,377,3,56,28,0,376,374,1,0,0,0,376,377,1,0,0,0,377,378,
        1,0,0,0,378,379,5,61,0,0,379,419,1,0,0,0,380,381,5,49,0,0,381,387,
        5,60,0,0,382,385,3,60,30,0,383,384,5,66,0,0,384,386,3,56,28,0,385,
        383,1,0,0,0,385,386,1,0,0,0,386,388,1,0,0,0,387,382,1,0,0,0,387,
        388,1,0,0,0,388,389,1,0,0,0,389,419,5,61,0,0,390,391,5,50,0,0,391,
        392,5,60,0,0,392,397,5,77,0,0,393,394,5,64,0,0,394,395,3,60,30,0,
        395,396,5,65,0,0,396,398,1,0,0,0,397,393,1,0,0,0,397,398,1,0,0,0,
        398,399,1,0,0,0,399,419,5,61,0,0,400,401,5,51,0,0,401,402,5,60,0,
        0,402,407,5,77,0,0,403,404,5,64,0,0,404,405,3,60,30,0,405,406,5,
        65,0,0,406,408,1,0,0,0,407,403,1,0,0,0,407,408,1,0,0,0,408,411,1,
        0,0,0,409,410,5,66,0,0,410,412,3,56,28,0,411,409,1,0,0,0,411,412,
        1,0,0,0,412,415,1,0,0,0,413,414,5,66,0,0,414,416,3,54,27,0,415,413,
        1,0,0,0,415,416,1,0,0,0,416,417,1,0,0,0,417,419,5,61,0,0,418,371,
        1,0,0,0,418,380,1,0,0,0,418,390,1,0,0,0,418,400,1,0,0,0,419,53,1,
        0,0,0,420,421,3,60,30,0,421,422,5,1,0,0,422,423,3,60,30,0,423,432,
        1,0,0,0,424,425,5,2,0,0,425,426,5,60,0,0,426,427,3,60,30,0,427,428,
        5,66,0,0,428,429,3,60,30,0,429,430,5,61,0,0,430,432,1,0,0,0,431,
        420,1,0,0,0,431,424,1,0,0,0,432,55,1,0,0,0,433,434,7,5,0,0,434,57,
        1,0,0,0,435,440,3,60,30,0,436,437,5,66,0,0,437,439,3,60,30,0,438,
        436,1,0,0,0,439,442,1,0,0,0,440,438,1,0,0,0,440,441,1,0,0,0,441,
        59,1,0,0,0,442,440,1,0,0,0,443,444,6,30,-1,0,444,445,5,71,0,0,445,
        467,3,60,30,14,446,447,5,77,0,0,447,449,5,60,0,0,448,450,3,58,29,
        0,449,448,1,0,0,0,449,450,1,0,0,0,450,451,1,0,0,0,451,467,5,61,0,
        0,452,457,5,77,0,0,453,454,5,64,0,0,454,455,3,60,30,0,455,456,5,
        65,0,0,456,458,1,0,0,0,457,453,1,0,0,0,457,458,1,0,0,0,458,467,1,
        0,0,0,459,467,5,76,0,0,460,467,5,58,0,0,461,467,5,75,0,0,462,463,
        5,60,0,0,463,464,3,60,30,0,464,465,5,61,0,0,465,467,1,0,0,0,466,
        443,1,0,0,0,466,446,1,0,0,0,466,452,1,0,0,0,466,459,1,0,0,0,466,
        460,1,0,0,0,466,461,1,0,0,0,466,462,1,0,0,0,467,491,1,0,0,0,468,
        469,10,13,0,0,469,470,5,59,0,0,470,490,3,60,30,14,471,472,10,12,
        0,0,472,473,7,6,0,0,473,490,3,60,30,13,474,475,10,11,0,0,475,476,
        7,7,0,0,476,490,3,60,30,12,477,478,10,10,0,0,478,479,7,8,0,0,479,
        490,3,60,30,11,480,481,10,9,0,0,481,482,7,9,0,0,482,490,3,60,30,
        10,483,484,10,8,0,0,484,485,5,14,0,0,485,490,3,60,30,9,486,487,10,
        7,0,0,487,488,5,15,0,0,488,490,3,60,30,8,489,468,1,0,0,0,489,471,
        1,0,0,0,489,474,1,0,0,0,489,477,1,0,0,0,489,480,1,0,0,0,489,483,
        1,0,0,0,489,486,1,0,0,0,490,493,1,0,0,0,491,489,1,0,0,0,491,492,
        1,0,0,0,492,61,1,0,0,0,493,491,1,0,0,0,51,65,73,81,88,94,104,112,
        118,162,167,175,182,189,197,206,210,217,225,229,237,243,250,258,
        264,272,280,288,296,303,305,316,325,332,340,351,361,376,385,387,
        397,407,411,415,418,431,440,449,457,466,489,491
    ]

class QLangParser ( Parser ):

    grammarFileName = "QLang.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'..'", "'range'", "'*'", "'/'", "'%'", 
                     "'+'", "'-'", "'<'", "'>'", "'<='", "'>='", "'=='", 
                     "'!='", "'&&'", "'||'", "'state'", "'obs'", "'superposed'", 
                     "'num'", "'H'", "'superpose'", "'S'", "'shift'", "'X'", 
                     "'not'", "'Y'", "'dual_not'", "'Z'", "'phase_not'", 
                     "'CNOT'", "'entangle'", "'CZ'", "'entangle_phase'", 
                     "'swap'", "'measure'", "'measureX'", "'if'", "'else'", 
                     "'function'", "'return'", "'for'", "'from'", "'to'", 
                     "'step'", "'while'", "'break'", "'continue'", "'print'", 
                     "'println'", "'debug'", "'input'", "'place'", "'send'", 
                     "'received'", "'as'", "'BIN'", "'HEX'", "<INVALID>", 
                     "'**'", "'('", "')'", "'{'", "'}'", "'['", "']'", "','", 
                     "';'", "':'", "'.'", "'?'", "'!'", "'->'", "'='", "'^'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "STATE", "OBS", "SUPERPOSED", "NUM", "H", "SUPERPOSE", 
                      "S", "SHIFT", "X", "NOT", "Y", "DUAL_NOT", "Z", "PHASE_NOT", 
                      "CNOT", "ENTANGLE", "CZ", "ENTANGLE_PHASE", "SWAP", 
                      "MEASURE", "MEASUREX", "IF", "ELSE", "FUNCTION", "RETURN", 
                      "FOR", "FROM", "TO", "STEP", "WHILE", "BREAK", "CONTINUE", 
                      "PRINT", "PRINTLN", "DEBUG", "INPUT", "PLACE", "SEND", 
                      "RECEIVED", "AS", "BIN", "HEX", "BOOL_VAL", "POW_OP", 
                      "LPAREN", "RPAREN", "LBRACE", "RBRACE", "LBRACK", 
                      "RBRACK", "COMMA", "SEMI", "COLON", "DOT", "QUESTION", 
                      "BANG", "ARROW", "ASSIGN", "HAT", "STRING", "NUMBER", 
                      "ID", "WS", "LINE_COMMENT", "BLOCK_COMMENT" ]

    RULE_program = 0
    RULE_topLevelItem = 1
    RULE_placeDecl = 2
    RULE_placeMember = 3
    RULE_functionDecl = 4
    RULE_paramList = 5
    RULE_param = 6
    RULE_block = 7
    RULE_statement = 8
    RULE_stateDecl = 9
    RULE_stateDef = 10
    RULE_obsDecl = 11
    RULE_obsDef = 12
    RULE_numDecl = 13
    RULE_receiveDecl = 14
    RULE_receiveOpt = 15
    RULE_sendStmt = 16
    RULE_gateStmt = 17
    RULE_singleQubitGate = 18
    RULE_multiQubitGate = 19
    RULE_measureStmt = 20
    RULE_assignStmt = 21
    RULE_functionCallStmt = 22
    RULE_ifStmt = 23
    RULE_forStmt = 24
    RULE_whileStmt = 25
    RULE_ioStmt = 26
    RULE_constraint = 27
    RULE_format = 28
    RULE_argList = 29
    RULE_expr = 30

    ruleNames =  [ "program", "topLevelItem", "placeDecl", "placeMember", 
                   "functionDecl", "paramList", "param", "block", "statement", 
                   "stateDecl", "stateDef", "obsDecl", "obsDef", "numDecl", 
                   "receiveDecl", "receiveOpt", "sendStmt", "gateStmt", 
                   "singleQubitGate", "multiQubitGate", "measureStmt", "assignStmt", 
                   "functionCallStmt", "ifStmt", "forStmt", "whileStmt", 
                   "ioStmt", "constraint", "format", "argList", "expr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    T__13=14
    T__14=15
    STATE=16
    OBS=17
    SUPERPOSED=18
    NUM=19
    H=20
    SUPERPOSE=21
    S=22
    SHIFT=23
    X=24
    NOT=25
    Y=26
    DUAL_NOT=27
    Z=28
    PHASE_NOT=29
    CNOT=30
    ENTANGLE=31
    CZ=32
    ENTANGLE_PHASE=33
    SWAP=34
    MEASURE=35
    MEASUREX=36
    IF=37
    ELSE=38
    FUNCTION=39
    RETURN=40
    FOR=41
    FROM=42
    TO=43
    STEP=44
    WHILE=45
    BREAK=46
    CONTINUE=47
    PRINT=48
    PRINTLN=49
    DEBUG=50
    INPUT=51
    PLACE=52
    SEND=53
    RECEIVED=54
    AS=55
    BIN=56
    HEX=57
    BOOL_VAL=58
    POW_OP=59
    LPAREN=60
    RPAREN=61
    LBRACE=62
    RBRACE=63
    LBRACK=64
    RBRACK=65
    COMMA=66
    SEMI=67
    COLON=68
    DOT=69
    QUESTION=70
    BANG=71
    ARROW=72
    ASSIGN=73
    HAT=74
    STRING=75
    NUMBER=76
    ID=77
    WS=78
    LINE_COMMENT=79
    BLOCK_COMMENT=80

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(QLangParser.EOF, 0)

        def topLevelItem(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.TopLevelItemContext)
            else:
                return self.getTypedRuleContext(QLangParser.TopLevelItemContext,i)


        def getRuleIndex(self):
            return QLangParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = QLangParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 16)) & ~0x3f) == 0 and ((1 << (_la - 16)) & 2308165452173934587) != 0):
                self.state = 62
                self.topLevelItem()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 68
            self.match(QLangParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TopLevelItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def placeDecl(self):
            return self.getTypedRuleContext(QLangParser.PlaceDeclContext,0)


        def functionDecl(self):
            return self.getTypedRuleContext(QLangParser.FunctionDeclContext,0)


        def statement(self):
            return self.getTypedRuleContext(QLangParser.StatementContext,0)


        def getRuleIndex(self):
            return QLangParser.RULE_topLevelItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTopLevelItem" ):
                listener.enterTopLevelItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTopLevelItem" ):
                listener.exitTopLevelItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTopLevelItem" ):
                return visitor.visitTopLevelItem(self)
            else:
                return visitor.visitChildren(self)




    def topLevelItem(self):

        localctx = QLangParser.TopLevelItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_topLevelItem)
        try:
            self.state = 73
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [52]:
                self.enterOuterAlt(localctx, 1)
                self.state = 70
                self.placeDecl()
                pass
            elif token in [39]:
                self.enterOuterAlt(localctx, 2)
                self.state = 71
                self.functionDecl()
                pass
            elif token in [16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 37, 40, 41, 45, 46, 47, 48, 49, 50, 51, 53, 62, 67, 77]:
                self.enterOuterAlt(localctx, 3)
                self.state = 72
                self.statement()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PlaceDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLACE(self):
            return self.getToken(QLangParser.PLACE, 0)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def LBRACE(self):
            return self.getToken(QLangParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(QLangParser.RBRACE, 0)

        def placeMember(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.PlaceMemberContext)
            else:
                return self.getTypedRuleContext(QLangParser.PlaceMemberContext,i)


        def getRuleIndex(self):
            return QLangParser.RULE_placeDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlaceDecl" ):
                listener.enterPlaceDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlaceDecl" ):
                listener.exitPlaceDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPlaceDecl" ):
                return visitor.visitPlaceDecl(self)
            else:
                return visitor.visitChildren(self)




    def placeDecl(self):

        localctx = QLangParser.PlaceDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_placeDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 75
            self.match(QLangParser.PLACE)
            self.state = 76
            self.match(QLangParser.ID)
            self.state = 77
            self.match(QLangParser.LBRACE)
            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 16)) & ~0x3f) == 0 and ((1 << (_la - 16)) & 2308165383454457851) != 0):
                self.state = 78
                self.placeMember()
                self.state = 83
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 84
            self.match(QLangParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PlaceMemberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionDecl(self):
            return self.getTypedRuleContext(QLangParser.FunctionDeclContext,0)


        def statement(self):
            return self.getTypedRuleContext(QLangParser.StatementContext,0)


        def getRuleIndex(self):
            return QLangParser.RULE_placeMember

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlaceMember" ):
                listener.enterPlaceMember(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlaceMember" ):
                listener.exitPlaceMember(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPlaceMember" ):
                return visitor.visitPlaceMember(self)
            else:
                return visitor.visitChildren(self)




    def placeMember(self):

        localctx = QLangParser.PlaceMemberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_placeMember)
        try:
            self.state = 88
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [39]:
                self.enterOuterAlt(localctx, 1)
                self.state = 86
                self.functionDecl()
                pass
            elif token in [16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 37, 40, 41, 45, 46, 47, 48, 49, 50, 51, 53, 62, 67, 77]:
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.statement()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FUNCTION(self):
            return self.getToken(QLangParser.FUNCTION, 0)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def LPAREN(self):
            return self.getToken(QLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(QLangParser.RPAREN, 0)

        def block(self):
            return self.getTypedRuleContext(QLangParser.BlockContext,0)


        def paramList(self):
            return self.getTypedRuleContext(QLangParser.ParamListContext,0)


        def getRuleIndex(self):
            return QLangParser.RULE_functionDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionDecl" ):
                listener.enterFunctionDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionDecl" ):
                listener.exitFunctionDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDecl" ):
                return visitor.visitFunctionDecl(self)
            else:
                return visitor.visitChildren(self)




    def functionDecl(self):

        localctx = QLangParser.FunctionDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_functionDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 90
            self.match(QLangParser.FUNCTION)
            self.state = 91
            self.match(QLangParser.ID)
            self.state = 92
            self.match(QLangParser.LPAREN)
            self.state = 94
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16 or _la==17:
                self.state = 93
                self.paramList()


            self.state = 96
            self.match(QLangParser.RPAREN)
            self.state = 97
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ParamContext)
            else:
                return self.getTypedRuleContext(QLangParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.COMMA)
            else:
                return self.getToken(QLangParser.COMMA, i)

        def getRuleIndex(self):
            return QLangParser.RULE_paramList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = QLangParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.param()
            self.state = 104
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==66:
                self.state = 100
                self.match(QLangParser.COMMA)
                self.state = 101
                self.param()
                self.state = 106
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def STATE(self):
            return self.getToken(QLangParser.STATE, 0)

        def OBS(self):
            return self.getToken(QLangParser.OBS, 0)

        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)

        def NUMBER(self):
            return self.getToken(QLangParser.NUMBER, 0)

        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam" ):
                listener.enterParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam" ):
                listener.exitParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = QLangParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_param)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 107
            _la = self._input.LA(1)
            if not(_la==16 or _la==17):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 108
            self.match(QLangParser.ID)
            self.state = 112
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 109
                self.match(QLangParser.LBRACK)
                self.state = 110
                self.match(QLangParser.NUMBER)
                self.state = 111
                self.match(QLangParser.RBRACK)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(QLangParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(QLangParser.RBRACE, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.StatementContext)
            else:
                return self.getTypedRuleContext(QLangParser.StatementContext,i)


        def getRuleIndex(self):
            return QLangParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = QLangParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self.match(QLangParser.LBRACE)
            self.state = 118
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while ((((_la - 16)) & ~0x3f) == 0 and ((1 << (_la - 16)) & 2308165383446069243) != 0):
                self.state = 115
                self.statement()
                self.state = 120
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 121
            self.match(QLangParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return QLangParser.RULE_statement

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class BlockStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def block(self):
            return self.getTypedRuleContext(QLangParser.BlockContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlockStatement" ):
                listener.enterBlockStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlockStatement" ):
                listener.exitBlockStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlockStatement" ):
                return visitor.visitBlockStatement(self)
            else:
                return visitor.visitChildren(self)


    class AssignmentStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def assignStmt(self):
            return self.getTypedRuleContext(QLangParser.AssignStmtContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignmentStatement" ):
                listener.enterAssignmentStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignmentStatement" ):
                listener.exitAssignmentStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentStatement" ):
                return visitor.visitAssignmentStatement(self)
            else:
                return visitor.visitChildren(self)


    class NumDeclarationContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def numDecl(self):
            return self.getTypedRuleContext(QLangParser.NumDeclContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumDeclaration" ):
                listener.enterNumDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumDeclaration" ):
                listener.exitNumDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumDeclaration" ):
                return visitor.visitNumDeclaration(self)
            else:
                return visitor.visitChildren(self)


    class IoStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ioStmt(self):
            return self.getTypedRuleContext(QLangParser.IoStmtContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIoStatement" ):
                listener.enterIoStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIoStatement" ):
                listener.exitIoStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIoStatement" ):
                return visitor.visitIoStatement(self)
            else:
                return visitor.visitChildren(self)


    class ForStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def forStmt(self):
            return self.getTypedRuleContext(QLangParser.ForStmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStatement" ):
                listener.enterForStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStatement" ):
                listener.exitForStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStatement" ):
                return visitor.visitForStatement(self)
            else:
                return visitor.visitChildren(self)


    class BreakStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BREAK(self):
            return self.getToken(QLangParser.BREAK, 0)
        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreakStatement" ):
                listener.enterBreakStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreakStatement" ):
                listener.exitBreakStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBreakStatement" ):
                return visitor.visitBreakStatement(self)
            else:
                return visitor.visitChildren(self)


    class IfStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ifStmt(self):
            return self.getTypedRuleContext(QLangParser.IfStmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)


    class ReturnStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def RETURN(self):
            return self.getToken(QLangParser.RETURN, 0)
        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)
        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStatement" ):
                listener.enterReturnStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStatement" ):
                listener.exitReturnStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStatement" ):
                return visitor.visitReturnStatement(self)
            else:
                return visitor.visitChildren(self)


    class MeasureStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def measureStmt(self):
            return self.getTypedRuleContext(QLangParser.MeasureStmtContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMeasureStatement" ):
                listener.enterMeasureStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMeasureStatement" ):
                listener.exitMeasureStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMeasureStatement" ):
                return visitor.visitMeasureStatement(self)
            else:
                return visitor.visitChildren(self)


    class GateStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def gateStmt(self):
            return self.getTypedRuleContext(QLangParser.GateStmtContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGateStatement" ):
                listener.enterGateStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGateStatement" ):
                listener.exitGateStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGateStatement" ):
                return visitor.visitGateStatement(self)
            else:
                return visitor.visitChildren(self)


    class WhileStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def whileStmt(self):
            return self.getTypedRuleContext(QLangParser.WhileStmtContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStatement" ):
                listener.enterWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStatement" ):
                listener.exitWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStatement" ):
                return visitor.visitWhileStatement(self)
            else:
                return visitor.visitChildren(self)


    class SemicolonStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSemicolonStatement" ):
                listener.enterSemicolonStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSemicolonStatement" ):
                listener.exitSemicolonStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSemicolonStatement" ):
                return visitor.visitSemicolonStatement(self)
            else:
                return visitor.visitChildren(self)


    class SendStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def sendStmt(self):
            return self.getTypedRuleContext(QLangParser.SendStmtContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSendStatement" ):
                listener.enterSendStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSendStatement" ):
                listener.exitSendStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSendStatement" ):
                return visitor.visitSendStatement(self)
            else:
                return visitor.visitChildren(self)


    class FunctionCallStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def functionCallStmt(self):
            return self.getTypedRuleContext(QLangParser.FunctionCallStmtContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCallStatement" ):
                listener.enterFunctionCallStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCallStatement" ):
                listener.exitFunctionCallStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallStatement" ):
                return visitor.visitFunctionCallStatement(self)
            else:
                return visitor.visitChildren(self)


    class ContinueStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CONTINUE(self):
            return self.getToken(QLangParser.CONTINUE, 0)
        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinueStatement" ):
                listener.enterContinueStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinueStatement" ):
                listener.exitContinueStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitContinueStatement" ):
                return visitor.visitContinueStatement(self)
            else:
                return visitor.visitChildren(self)


    class StateDeclarationContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def stateDecl(self):
            return self.getTypedRuleContext(QLangParser.StateDeclContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStateDeclaration" ):
                listener.enterStateDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStateDeclaration" ):
                listener.exitStateDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStateDeclaration" ):
                return visitor.visitStateDeclaration(self)
            else:
                return visitor.visitChildren(self)


    class ObsDeclarationContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def obsDecl(self):
            return self.getTypedRuleContext(QLangParser.ObsDeclContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObsDeclaration" ):
                listener.enterObsDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObsDeclaration" ):
                listener.exitObsDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObsDeclaration" ):
                return visitor.visitObsDeclaration(self)
            else:
                return visitor.visitChildren(self)


    class ReceiveDeclarationContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def receiveDecl(self):
            return self.getTypedRuleContext(QLangParser.ReceiveDeclContext,0)

        def SEMI(self):
            return self.getToken(QLangParser.SEMI, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReceiveDeclaration" ):
                listener.enterReceiveDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReceiveDeclaration" ):
                listener.exitReceiveDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReceiveDeclaration" ):
                return visitor.visitReceiveDeclaration(self)
            else:
                return visitor.visitChildren(self)



    def statement(self):

        localctx = QLangParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.state = 167
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                localctx = QLangParser.StateDeclarationContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 123
                self.stateDecl()
                self.state = 124
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 2:
                localctx = QLangParser.ObsDeclarationContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 126
                self.obsDecl()
                self.state = 127
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 3:
                localctx = QLangParser.NumDeclarationContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 129
                self.numDecl()
                self.state = 130
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 4:
                localctx = QLangParser.ReceiveDeclarationContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 132
                self.receiveDecl()
                self.state = 133
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 5:
                localctx = QLangParser.SendStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 135
                self.sendStmt()
                self.state = 136
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 6:
                localctx = QLangParser.GateStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 138
                self.gateStmt()
                self.state = 139
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 7:
                localctx = QLangParser.MeasureStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 141
                self.measureStmt()
                self.state = 142
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 8:
                localctx = QLangParser.AssignmentStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 144
                self.assignStmt()
                self.state = 145
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 9:
                localctx = QLangParser.FunctionCallStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 147
                self.functionCallStmt()
                self.state = 148
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 10:
                localctx = QLangParser.IfStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 150
                self.ifStmt()
                pass

            elif la_ == 11:
                localctx = QLangParser.ForStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 11)
                self.state = 151
                self.forStmt()
                pass

            elif la_ == 12:
                localctx = QLangParser.WhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 12)
                self.state = 152
                self.whileStmt()
                pass

            elif la_ == 13:
                localctx = QLangParser.IoStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 13)
                self.state = 153
                self.ioStmt()
                self.state = 154
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 14:
                localctx = QLangParser.BreakStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 14)
                self.state = 156
                self.match(QLangParser.BREAK)
                self.state = 157
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 15:
                localctx = QLangParser.ContinueStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 15)
                self.state = 158
                self.match(QLangParser.CONTINUE)
                self.state = 159
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 16:
                localctx = QLangParser.ReturnStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 16)
                self.state = 160
                self.match(QLangParser.RETURN)
                self.state = 162
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 58)) & ~0x3f) == 0 and ((1 << (_la - 58)) & 925701) != 0):
                    self.state = 161
                    self.expr(0)


                self.state = 164
                self.match(QLangParser.SEMI)
                pass

            elif la_ == 17:
                localctx = QLangParser.BlockStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 17)
                self.state = 165
                self.block()
                pass

            elif la_ == 18:
                localctx = QLangParser.SemicolonStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 18)
                self.state = 166
                self.match(QLangParser.SEMI)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StateDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STATE(self):
            return self.getToken(QLangParser.STATE, 0)

        def stateDef(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.StateDefContext)
            else:
                return self.getTypedRuleContext(QLangParser.StateDefContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.COMMA)
            else:
                return self.getToken(QLangParser.COMMA, i)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(QLangParser.ASSIGN, 0)

        def SUPERPOSED(self):
            return self.getToken(QLangParser.SUPERPOSED, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_stateDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStateDecl" ):
                listener.enterStateDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStateDecl" ):
                listener.exitStateDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStateDecl" ):
                return visitor.visitStateDecl(self)
            else:
                return visitor.visitChildren(self)




    def stateDecl(self):

        localctx = QLangParser.StateDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_stateDecl)
        self._la = 0 # Token type
        try:
            self.state = 182
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 169
                self.match(QLangParser.STATE)
                self.state = 170
                self.stateDef()
                self.state = 175
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==66:
                    self.state = 171
                    self.match(QLangParser.COMMA)
                    self.state = 172
                    self.stateDef()
                    self.state = 177
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 178
                self.match(QLangParser.STATE)
                self.state = 179
                self.match(QLangParser.ID)
                self.state = 180
                self.match(QLangParser.ASSIGN)
                self.state = 181
                self.match(QLangParser.SUPERPOSED)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StateDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)

        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)


        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_stateDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStateDef" ):
                listener.enterStateDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStateDef" ):
                listener.exitStateDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStateDef" ):
                return visitor.visitStateDef(self)
            else:
                return visitor.visitChildren(self)




    def stateDef(self):

        localctx = QLangParser.StateDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_stateDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 184
            self.match(QLangParser.ID)
            self.state = 189
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 185
                self.match(QLangParser.LBRACK)
                self.state = 186
                self.expr(0)
                self.state = 187
                self.match(QLangParser.RBRACK)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObsDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def OBS(self):
            return self.getToken(QLangParser.OBS, 0)

        def obsDef(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ObsDefContext)
            else:
                return self.getTypedRuleContext(QLangParser.ObsDefContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.COMMA)
            else:
                return self.getToken(QLangParser.COMMA, i)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(QLangParser.ASSIGN, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_obsDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObsDecl" ):
                listener.enterObsDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObsDecl" ):
                listener.exitObsDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObsDecl" ):
                return visitor.visitObsDecl(self)
            else:
                return visitor.visitChildren(self)




    def obsDecl(self):

        localctx = QLangParser.ObsDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_obsDecl)
        self._la = 0 # Token type
        try:
            self.state = 210
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 191
                self.match(QLangParser.OBS)
                self.state = 192
                self.obsDef()
                self.state = 197
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==66:
                    self.state = 193
                    self.match(QLangParser.COMMA)
                    self.state = 194
                    self.obsDef()
                    self.state = 199
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 200
                self.match(QLangParser.OBS)
                self.state = 201
                self.match(QLangParser.ID)
                self.state = 206
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==64:
                    self.state = 202
                    self.match(QLangParser.LBRACK)
                    self.state = 203
                    self.expr(0)
                    self.state = 204
                    self.match(QLangParser.RBRACK)


                self.state = 208
                self.match(QLangParser.ASSIGN)
                self.state = 209
                self.expr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObsDefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)

        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)


        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_obsDef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObsDef" ):
                listener.enterObsDef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObsDef" ):
                listener.exitObsDef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObsDef" ):
                return visitor.visitObsDef(self)
            else:
                return visitor.visitChildren(self)




    def obsDef(self):

        localctx = QLangParser.ObsDefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_obsDef)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.match(QLangParser.ID)
            self.state = 217
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 213
                self.match(QLangParser.LBRACK)
                self.state = 214
                self.expr(0)
                self.state = 215
                self.match(QLangParser.RBRACK)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUM(self):
            return self.getToken(QLangParser.NUM, 0)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def ASSIGN(self):
            return self.getToken(QLangParser.ASSIGN, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_numDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumDecl" ):
                listener.enterNumDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumDecl" ):
                listener.exitNumDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumDecl" ):
                return visitor.visitNumDecl(self)
            else:
                return visitor.visitChildren(self)




    def numDecl(self):

        localctx = QLangParser.NumDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_numDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 219
            self.match(QLangParser.NUM)
            self.state = 220
            self.match(QLangParser.ID)
            self.state = 225
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 221
                self.match(QLangParser.LBRACK)
                self.state = 222
                self.expr(0)
                self.state = 223
                self.match(QLangParser.RBRACK)


            self.state = 229
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==73:
                self.state = 227
                self.match(QLangParser.ASSIGN)
                self.state = 228
                self.expr(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReceiveDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def RECEIVED(self):
            return self.getToken(QLangParser.RECEIVED, 0)

        def STATE(self):
            return self.getToken(QLangParser.STATE, 0)

        def OBS(self):
            return self.getToken(QLangParser.OBS, 0)

        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)

        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)


        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def receiveOpt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ReceiveOptContext)
            else:
                return self.getTypedRuleContext(QLangParser.ReceiveOptContext,i)


        def getRuleIndex(self):
            return QLangParser.RULE_receiveDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReceiveDecl" ):
                listener.enterReceiveDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReceiveDecl" ):
                listener.exitReceiveDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReceiveDecl" ):
                return visitor.visitReceiveDecl(self)
            else:
                return visitor.visitChildren(self)




    def receiveDecl(self):

        localctx = QLangParser.ReceiveDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_receiveDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 231
            _la = self._input.LA(1)
            if not(_la==16 or _la==17):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 232
            self.match(QLangParser.ID)
            self.state = 237
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 233
                self.match(QLangParser.LBRACK)
                self.state = 234
                self.expr(0)
                self.state = 235
                self.match(QLangParser.RBRACK)


            self.state = 239
            self.match(QLangParser.RECEIVED)
            self.state = 243
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==42 or _la==55:
                self.state = 240
                self.receiveOpt()
                self.state = 245
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReceiveOptContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FROM(self):
            return self.getToken(QLangParser.FROM, 0)

        def STRING(self):
            return self.getToken(QLangParser.STRING, 0)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def AS(self):
            return self.getToken(QLangParser.AS, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_receiveOpt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReceiveOpt" ):
                listener.enterReceiveOpt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReceiveOpt" ):
                listener.exitReceiveOpt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReceiveOpt" ):
                return visitor.visitReceiveOpt(self)
            else:
                return visitor.visitChildren(self)




    def receiveOpt(self):

        localctx = QLangParser.ReceiveOptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_receiveOpt)
        self._la = 0 # Token type
        try:
            self.state = 250
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [42]:
                self.enterOuterAlt(localctx, 1)
                self.state = 246
                self.match(QLangParser.FROM)
                self.state = 247
                _la = self._input.LA(1)
                if not(_la==75 or _la==77):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass
            elif token in [55]:
                self.enterOuterAlt(localctx, 2)
                self.state = 248
                self.match(QLangParser.AS)
                self.state = 249
                self.match(QLangParser.STRING)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SendStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SEND(self):
            return self.getToken(QLangParser.SEND, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.ID)
            else:
                return self.getToken(QLangParser.ID, i)

        def TO(self):
            return self.getToken(QLangParser.TO, 0)

        def STRING(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.STRING)
            else:
                return self.getToken(QLangParser.STRING, i)

        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)

        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)


        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def AS(self):
            return self.getToken(QLangParser.AS, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_sendStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSendStmt" ):
                listener.enterSendStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSendStmt" ):
                listener.exitSendStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSendStmt" ):
                return visitor.visitSendStmt(self)
            else:
                return visitor.visitChildren(self)




    def sendStmt(self):

        localctx = QLangParser.SendStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_sendStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 252
            self.match(QLangParser.SEND)
            self.state = 253
            self.match(QLangParser.ID)
            self.state = 258
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 254
                self.match(QLangParser.LBRACK)
                self.state = 255
                self.expr(0)
                self.state = 256
                self.match(QLangParser.RBRACK)


            self.state = 260
            self.match(QLangParser.TO)
            self.state = 261
            _la = self._input.LA(1)
            if not(_la==75 or _la==77):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 264
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==55:
                self.state = 262
                self.match(QLangParser.AS)
                self.state = 263
                self.match(QLangParser.STRING)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GateStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def singleQubitGate(self):
            return self.getTypedRuleContext(QLangParser.SingleQubitGateContext,0)


        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.ID)
            else:
                return self.getToken(QLangParser.ID, i)

        def LBRACK(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.LBRACK)
            else:
                return self.getToken(QLangParser.LBRACK, i)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def RBRACK(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.RBRACK)
            else:
                return self.getToken(QLangParser.RBRACK, i)

        def multiQubitGate(self):
            return self.getTypedRuleContext(QLangParser.MultiQubitGateContext,0)


        def ARROW(self):
            return self.getToken(QLangParser.ARROW, 0)

        def SWAP(self):
            return self.getToken(QLangParser.SWAP, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_gateStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGateStmt" ):
                listener.enterGateStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGateStmt" ):
                listener.exitGateStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGateStmt" ):
                return visitor.visitGateStmt(self)
            else:
                return visitor.visitChildren(self)




    def gateStmt(self):

        localctx = QLangParser.GateStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_gateStmt)
        self._la = 0 # Token type
        try:
            self.state = 305
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]:
                self.enterOuterAlt(localctx, 1)
                self.state = 266
                self.singleQubitGate()
                self.state = 267
                self.match(QLangParser.ID)
                self.state = 272
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==64:
                    self.state = 268
                    self.match(QLangParser.LBRACK)
                    self.state = 269
                    self.expr(0)
                    self.state = 270
                    self.match(QLangParser.RBRACK)


                pass
            elif token in [30, 31, 32, 33]:
                self.enterOuterAlt(localctx, 2)
                self.state = 274
                self.multiQubitGate()
                self.state = 275
                self.match(QLangParser.ID)
                self.state = 280
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==64:
                    self.state = 276
                    self.match(QLangParser.LBRACK)
                    self.state = 277
                    self.expr(0)
                    self.state = 278
                    self.match(QLangParser.RBRACK)


                self.state = 282
                self.match(QLangParser.ARROW)
                self.state = 283
                self.match(QLangParser.ID)
                self.state = 288
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==64:
                    self.state = 284
                    self.match(QLangParser.LBRACK)
                    self.state = 285
                    self.expr(0)
                    self.state = 286
                    self.match(QLangParser.RBRACK)


                pass
            elif token in [34]:
                self.enterOuterAlt(localctx, 3)
                self.state = 290
                self.match(QLangParser.SWAP)
                self.state = 291
                self.match(QLangParser.ID)
                self.state = 296
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==64:
                    self.state = 292
                    self.match(QLangParser.LBRACK)
                    self.state = 293
                    self.expr(0)
                    self.state = 294
                    self.match(QLangParser.RBRACK)


                self.state = 298
                self.match(QLangParser.ID)
                self.state = 303
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==64:
                    self.state = 299
                    self.match(QLangParser.LBRACK)
                    self.state = 300
                    self.expr(0)
                    self.state = 301
                    self.match(QLangParser.RBRACK)


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SingleQubitGateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def H(self):
            return self.getToken(QLangParser.H, 0)

        def SUPERPOSE(self):
            return self.getToken(QLangParser.SUPERPOSE, 0)

        def S(self):
            return self.getToken(QLangParser.S, 0)

        def SHIFT(self):
            return self.getToken(QLangParser.SHIFT, 0)

        def X(self):
            return self.getToken(QLangParser.X, 0)

        def NOT(self):
            return self.getToken(QLangParser.NOT, 0)

        def Y(self):
            return self.getToken(QLangParser.Y, 0)

        def DUAL_NOT(self):
            return self.getToken(QLangParser.DUAL_NOT, 0)

        def Z(self):
            return self.getToken(QLangParser.Z, 0)

        def PHASE_NOT(self):
            return self.getToken(QLangParser.PHASE_NOT, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_singleQubitGate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSingleQubitGate" ):
                listener.enterSingleQubitGate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSingleQubitGate" ):
                listener.exitSingleQubitGate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSingleQubitGate" ):
                return visitor.visitSingleQubitGate(self)
            else:
                return visitor.visitChildren(self)




    def singleQubitGate(self):

        localctx = QLangParser.SingleQubitGateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_singleQubitGate)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 307
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1072693248) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiQubitGateContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CNOT(self):
            return self.getToken(QLangParser.CNOT, 0)

        def ENTANGLE(self):
            return self.getToken(QLangParser.ENTANGLE, 0)

        def CZ(self):
            return self.getToken(QLangParser.CZ, 0)

        def ENTANGLE_PHASE(self):
            return self.getToken(QLangParser.ENTANGLE_PHASE, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_multiQubitGate

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiQubitGate" ):
                listener.enterMultiQubitGate(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiQubitGate" ):
                listener.exitMultiQubitGate(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiQubitGate" ):
                return visitor.visitMultiQubitGate(self)
            else:
                return visitor.visitChildren(self)




    def multiQubitGate(self):

        localctx = QLangParser.MultiQubitGateContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_multiQubitGate)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 309
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 16106127360) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MeasureStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.ID)
            else:
                return self.getToken(QLangParser.ID, i)

        def ASSIGN(self):
            return self.getToken(QLangParser.ASSIGN, 0)

        def MEASURE(self):
            return self.getToken(QLangParser.MEASURE, 0)

        def MEASUREX(self):
            return self.getToken(QLangParser.MEASUREX, 0)

        def LBRACK(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.LBRACK)
            else:
                return self.getToken(QLangParser.LBRACK, i)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def RBRACK(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.RBRACK)
            else:
                return self.getToken(QLangParser.RBRACK, i)

        def getRuleIndex(self):
            return QLangParser.RULE_measureStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMeasureStmt" ):
                listener.enterMeasureStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMeasureStmt" ):
                listener.exitMeasureStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMeasureStmt" ):
                return visitor.visitMeasureStmt(self)
            else:
                return visitor.visitChildren(self)




    def measureStmt(self):

        localctx = QLangParser.MeasureStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_measureStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 311
            self.match(QLangParser.ID)
            self.state = 316
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 312
                self.match(QLangParser.LBRACK)
                self.state = 313
                self.expr(0)
                self.state = 314
                self.match(QLangParser.RBRACK)


            self.state = 318
            self.match(QLangParser.ASSIGN)
            self.state = 319
            _la = self._input.LA(1)
            if not(_la==35 or _la==36):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 320
            self.match(QLangParser.ID)
            self.state = 325
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 321
                self.match(QLangParser.LBRACK)
                self.state = 322
                self.expr(0)
                self.state = 323
                self.match(QLangParser.RBRACK)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(QLangParser.ASSIGN, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_assignStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignStmt" ):
                listener.enterAssignStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignStmt" ):
                listener.exitAssignStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignStmt" ):
                return visitor.visitAssignStmt(self)
            else:
                return visitor.visitChildren(self)




    def assignStmt(self):

        localctx = QLangParser.AssignStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_assignStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 327
            self.match(QLangParser.ID)
            self.state = 332
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==64:
                self.state = 328
                self.match(QLangParser.LBRACK)
                self.state = 329
                self.expr(0)
                self.state = 330
                self.match(QLangParser.RBRACK)


            self.state = 334
            self.match(QLangParser.ASSIGN)
            self.state = 335
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def LPAREN(self):
            return self.getToken(QLangParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(QLangParser.RPAREN, 0)

        def argList(self):
            return self.getTypedRuleContext(QLangParser.ArgListContext,0)


        def getRuleIndex(self):
            return QLangParser.RULE_functionCallStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCallStmt" ):
                listener.enterFunctionCallStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCallStmt" ):
                listener.exitFunctionCallStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallStmt" ):
                return visitor.visitFunctionCallStmt(self)
            else:
                return visitor.visitChildren(self)




    def functionCallStmt(self):

        localctx = QLangParser.FunctionCallStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_functionCallStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 337
            self.match(QLangParser.ID)
            self.state = 338
            self.match(QLangParser.LPAREN)
            self.state = 340
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((((_la - 58)) & ~0x3f) == 0 and ((1 << (_la - 58)) & 925701) != 0):
                self.state = 339
                self.argList()


            self.state = 342
            self.match(QLangParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(QLangParser.IF, 0)

        def LPAREN(self):
            return self.getToken(QLangParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(QLangParser.RPAREN, 0)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.BlockContext)
            else:
                return self.getTypedRuleContext(QLangParser.BlockContext,i)


        def ELSE(self):
            return self.getToken(QLangParser.ELSE, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = QLangParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 344
            self.match(QLangParser.IF)
            self.state = 345
            self.match(QLangParser.LPAREN)
            self.state = 346
            self.expr(0)
            self.state = 347
            self.match(QLangParser.RPAREN)
            self.state = 348
            self.block()
            self.state = 351
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==38:
                self.state = 349
                self.match(QLangParser.ELSE)
                self.state = 350
                self.block()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(QLangParser.FOR, 0)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def FROM(self):
            return self.getToken(QLangParser.FROM, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def TO(self):
            return self.getToken(QLangParser.TO, 0)

        def block(self):
            return self.getTypedRuleContext(QLangParser.BlockContext,0)


        def STEP(self):
            return self.getToken(QLangParser.STEP, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_forStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStmt" ):
                listener.enterForStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStmt" ):
                listener.exitForStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStmt" ):
                return visitor.visitForStmt(self)
            else:
                return visitor.visitChildren(self)




    def forStmt(self):

        localctx = QLangParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_forStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 353
            self.match(QLangParser.FOR)
            self.state = 354
            self.match(QLangParser.ID)
            self.state = 355
            self.match(QLangParser.FROM)
            self.state = 356
            self.expr(0)
            self.state = 357
            self.match(QLangParser.TO)
            self.state = 358
            self.expr(0)
            self.state = 361
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==44:
                self.state = 359
                self.match(QLangParser.STEP)
                self.state = 360
                self.expr(0)


            self.state = 363
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WhileStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(QLangParser.WHILE, 0)

        def LPAREN(self):
            return self.getToken(QLangParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(QLangParser.RPAREN, 0)

        def block(self):
            return self.getTypedRuleContext(QLangParser.BlockContext,0)


        def getRuleIndex(self):
            return QLangParser.RULE_whileStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStmt" ):
                listener.enterWhileStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStmt" ):
                listener.exitWhileStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStmt" ):
                return visitor.visitWhileStmt(self)
            else:
                return visitor.visitChildren(self)




    def whileStmt(self):

        localctx = QLangParser.WhileStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_whileStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 365
            self.match(QLangParser.WHILE)
            self.state = 366
            self.match(QLangParser.LPAREN)
            self.state = 367
            self.expr(0)
            self.state = 368
            self.match(QLangParser.RPAREN)
            self.state = 369
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IoStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PRINT(self):
            return self.getToken(QLangParser.PRINT, 0)

        def LPAREN(self):
            return self.getToken(QLangParser.LPAREN, 0)

        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)


        def RPAREN(self):
            return self.getToken(QLangParser.RPAREN, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.COMMA)
            else:
                return self.getToken(QLangParser.COMMA, i)

        def format_(self):
            return self.getTypedRuleContext(QLangParser.FormatContext,0)


        def PRINTLN(self):
            return self.getToken(QLangParser.PRINTLN, 0)

        def DEBUG(self):
            return self.getToken(QLangParser.DEBUG, 0)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)

        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)

        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def INPUT(self):
            return self.getToken(QLangParser.INPUT, 0)

        def constraint(self):
            return self.getTypedRuleContext(QLangParser.ConstraintContext,0)


        def getRuleIndex(self):
            return QLangParser.RULE_ioStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIoStmt" ):
                listener.enterIoStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIoStmt" ):
                listener.exitIoStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIoStmt" ):
                return visitor.visitIoStmt(self)
            else:
                return visitor.visitChildren(self)




    def ioStmt(self):

        localctx = QLangParser.IoStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_ioStmt)
        self._la = 0 # Token type
        try:
            self.state = 418
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [48]:
                self.enterOuterAlt(localctx, 1)
                self.state = 371
                self.match(QLangParser.PRINT)
                self.state = 372
                self.match(QLangParser.LPAREN)
                self.state = 373
                self.expr(0)
                self.state = 376
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==66:
                    self.state = 374
                    self.match(QLangParser.COMMA)
                    self.state = 375
                    self.format_()


                self.state = 378
                self.match(QLangParser.RPAREN)
                pass
            elif token in [49]:
                self.enterOuterAlt(localctx, 2)
                self.state = 380
                self.match(QLangParser.PRINTLN)
                self.state = 381
                self.match(QLangParser.LPAREN)
                self.state = 387
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 58)) & ~0x3f) == 0 and ((1 << (_la - 58)) & 925701) != 0):
                    self.state = 382
                    self.expr(0)
                    self.state = 385
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==66:
                        self.state = 383
                        self.match(QLangParser.COMMA)
                        self.state = 384
                        self.format_()




                self.state = 389
                self.match(QLangParser.RPAREN)
                pass
            elif token in [50]:
                self.enterOuterAlt(localctx, 3)
                self.state = 390
                self.match(QLangParser.DEBUG)
                self.state = 391
                self.match(QLangParser.LPAREN)
                self.state = 392
                self.match(QLangParser.ID)
                self.state = 397
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==64:
                    self.state = 393
                    self.match(QLangParser.LBRACK)
                    self.state = 394
                    self.expr(0)
                    self.state = 395
                    self.match(QLangParser.RBRACK)


                self.state = 399
                self.match(QLangParser.RPAREN)
                pass
            elif token in [51]:
                self.enterOuterAlt(localctx, 4)
                self.state = 400
                self.match(QLangParser.INPUT)
                self.state = 401
                self.match(QLangParser.LPAREN)
                self.state = 402
                self.match(QLangParser.ID)
                self.state = 407
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==64:
                    self.state = 403
                    self.match(QLangParser.LBRACK)
                    self.state = 404
                    self.expr(0)
                    self.state = 405
                    self.match(QLangParser.RBRACK)


                self.state = 411
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,41,self._ctx)
                if la_ == 1:
                    self.state = 409
                    self.match(QLangParser.COMMA)
                    self.state = 410
                    self.format_()


                self.state = 415
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==66:
                    self.state = 413
                    self.match(QLangParser.COMMA)
                    self.state = 414
                    self.constraint()


                self.state = 417
                self.match(QLangParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConstraintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def LPAREN(self):
            return self.getToken(QLangParser.LPAREN, 0)

        def COMMA(self):
            return self.getToken(QLangParser.COMMA, 0)

        def RPAREN(self):
            return self.getToken(QLangParser.RPAREN, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_constraint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterConstraint" ):
                listener.enterConstraint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitConstraint" ):
                listener.exitConstraint(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitConstraint" ):
                return visitor.visitConstraint(self)
            else:
                return visitor.visitChildren(self)




    def constraint(self):

        localctx = QLangParser.ConstraintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_constraint)
        try:
            self.state = 431
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [58, 60, 71, 75, 76, 77]:
                self.enterOuterAlt(localctx, 1)
                self.state = 420
                self.expr(0)
                self.state = 421
                self.match(QLangParser.T__0)
                self.state = 422
                self.expr(0)
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 424
                self.match(QLangParser.T__1)
                self.state = 425
                self.match(QLangParser.LPAREN)
                self.state = 426
                self.expr(0)
                self.state = 427
                self.match(QLangParser.COMMA)
                self.state = 428
                self.expr(0)
                self.state = 429
                self.match(QLangParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FormatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BIN(self):
            return self.getToken(QLangParser.BIN, 0)

        def HEX(self):
            return self.getToken(QLangParser.HEX, 0)

        def getRuleIndex(self):
            return QLangParser.RULE_format

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFormat" ):
                listener.enterFormat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFormat" ):
                listener.exitFormat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFormat" ):
                return visitor.visitFormat(self)
            else:
                return visitor.visitChildren(self)




    def format_(self):

        localctx = QLangParser.FormatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_format)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 433
            _la = self._input.LA(1)
            if not(_la==56 or _la==57):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(QLangParser.COMMA)
            else:
                return self.getToken(QLangParser.COMMA, i)

        def getRuleIndex(self):
            return QLangParser.RULE_argList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgList" ):
                listener.enterArgList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgList" ):
                listener.exitArgList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgList" ):
                return visitor.visitArgList(self)
            else:
                return visitor.visitChildren(self)




    def argList(self):

        localctx = QLangParser.ArgListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_argList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 435
            self.expr(0)
            self.state = 440
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==66:
                self.state = 436
                self.match(QLangParser.COMMA)
                self.state = 437
                self.expr(0)
                self.state = 442
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return QLangParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AndExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndExpr" ):
                listener.enterAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndExpr" ):
                listener.exitAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndExpr" ):
                return visitor.visitAndExpr(self)
            else:
                return visitor.visitChildren(self)


    class BoolExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BOOL_VAL(self):
            return self.getToken(QLangParser.BOOL_VAL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolExpr" ):
                listener.enterBoolExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolExpr" ):
                listener.exitBoolExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolExpr" ):
                return visitor.visitBoolExpr(self)
            else:
                return visitor.visitChildren(self)


    class RelExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelExpr" ):
                listener.enterRelExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelExpr" ):
                listener.exitRelExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelExpr" ):
                return visitor.visitRelExpr(self)
            else:
                return visitor.visitChildren(self)


    class PowExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)

        def POW_OP(self):
            return self.getToken(QLangParser.POW_OP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPowExpr" ):
                listener.enterPowExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPowExpr" ):
                listener.exitPowExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPowExpr" ):
                return visitor.visitPowExpr(self)
            else:
                return visitor.visitChildren(self)


    class OrExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrExpr" ):
                listener.enterOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrExpr" ):
                listener.exitOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrExpr" ):
                return visitor.visitOrExpr(self)
            else:
                return visitor.visitChildren(self)


    class NumExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(QLangParser.NUMBER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumExpr" ):
                listener.enterNumExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumExpr" ):
                listener.exitNumExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumExpr" ):
                return visitor.visitNumExpr(self)
            else:
                return visitor.visitChildren(self)


    class MulDivModExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMulDivModExpr" ):
                listener.enterMulDivModExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMulDivModExpr" ):
                listener.exitMulDivModExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMulDivModExpr" ):
                return visitor.visitMulDivModExpr(self)
            else:
                return visitor.visitChildren(self)


    class EqExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqExpr" ):
                listener.enterEqExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqExpr" ):
                listener.exitEqExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqExpr" ):
                return visitor.visitEqExpr(self)
            else:
                return visitor.visitChildren(self)


    class VarExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)
        def LBRACK(self):
            return self.getToken(QLangParser.LBRACK, 0)
        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)

        def RBRACK(self):
            return self.getToken(QLangParser.RBRACK, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVarExpr" ):
                listener.enterVarExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVarExpr" ):
                listener.exitVarExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVarExpr" ):
                return visitor.visitVarExpr(self)
            else:
                return visitor.visitChildren(self)


    class StrExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(QLangParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStrExpr" ):
                listener.enterStrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStrExpr" ):
                listener.exitStrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStrExpr" ):
                return visitor.visitStrExpr(self)
            else:
                return visitor.visitChildren(self)


    class NotExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BANG(self):
            return self.getToken(QLangParser.BANG, 0)
        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNotExpr" ):
                listener.enterNotExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNotExpr" ):
                listener.exitNotExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNotExpr" ):
                return visitor.visitNotExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(QLangParser.LPAREN, 0)
        def expr(self):
            return self.getTypedRuleContext(QLangParser.ExprContext,0)

        def RPAREN(self):
            return self.getToken(QLangParser.RPAREN, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)


    class AddSubExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QLangParser.ExprContext)
            else:
                return self.getTypedRuleContext(QLangParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAddSubExpr" ):
                listener.enterAddSubExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAddSubExpr" ):
                listener.exitAddSubExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAddSubExpr" ):
                return visitor.visitAddSubExpr(self)
            else:
                return visitor.visitChildren(self)


    class FuncCallExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QLangParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(QLangParser.ID, 0)
        def LPAREN(self):
            return self.getToken(QLangParser.LPAREN, 0)
        def RPAREN(self):
            return self.getToken(QLangParser.RPAREN, 0)
        def argList(self):
            return self.getTypedRuleContext(QLangParser.ArgListContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncCallExpr" ):
                listener.enterFuncCallExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncCallExpr" ):
                listener.exitFuncCallExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncCallExpr" ):
                return visitor.visitFuncCallExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = QLangParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 60
        self.enterRecursionRule(localctx, 60, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 466
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,48,self._ctx)
            if la_ == 1:
                localctx = QLangParser.NotExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 444
                self.match(QLangParser.BANG)
                self.state = 445
                self.expr(14)
                pass

            elif la_ == 2:
                localctx = QLangParser.FuncCallExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 446
                self.match(QLangParser.ID)
                self.state = 447
                self.match(QLangParser.LPAREN)
                self.state = 449
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 58)) & ~0x3f) == 0 and ((1 << (_la - 58)) & 925701) != 0):
                    self.state = 448
                    self.argList()


                self.state = 451
                self.match(QLangParser.RPAREN)
                pass

            elif la_ == 3:
                localctx = QLangParser.VarExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 452
                self.match(QLangParser.ID)
                self.state = 457
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,47,self._ctx)
                if la_ == 1:
                    self.state = 453
                    self.match(QLangParser.LBRACK)
                    self.state = 454
                    self.expr(0)
                    self.state = 455
                    self.match(QLangParser.RBRACK)


                pass

            elif la_ == 4:
                localctx = QLangParser.NumExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 459
                self.match(QLangParser.NUMBER)
                pass

            elif la_ == 5:
                localctx = QLangParser.BoolExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 460
                self.match(QLangParser.BOOL_VAL)
                pass

            elif la_ == 6:
                localctx = QLangParser.StrExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 461
                self.match(QLangParser.STRING)
                pass

            elif la_ == 7:
                localctx = QLangParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 462
                self.match(QLangParser.LPAREN)
                self.state = 463
                self.expr(0)
                self.state = 464
                self.match(QLangParser.RPAREN)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 491
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,50,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 489
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,49,self._ctx)
                    if la_ == 1:
                        localctx = QLangParser.PowExprContext(self, QLangParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 468
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 469
                        self.match(QLangParser.POW_OP)
                        self.state = 470
                        self.expr(14)
                        pass

                    elif la_ == 2:
                        localctx = QLangParser.MulDivModExprContext(self, QLangParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 471
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 472
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 56) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 473
                        self.expr(13)
                        pass

                    elif la_ == 3:
                        localctx = QLangParser.AddSubExprContext(self, QLangParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 474
                        if not self.precpred(self._ctx, 11):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 11)")
                        self.state = 475
                        _la = self._input.LA(1)
                        if not(_la==6 or _la==7):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 476
                        self.expr(12)
                        pass

                    elif la_ == 4:
                        localctx = QLangParser.RelExprContext(self, QLangParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 477
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 478
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3840) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 479
                        self.expr(11)
                        pass

                    elif la_ == 5:
                        localctx = QLangParser.EqExprContext(self, QLangParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 480
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 481
                        _la = self._input.LA(1)
                        if not(_la==12 or _la==13):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 482
                        self.expr(10)
                        pass

                    elif la_ == 6:
                        localctx = QLangParser.AndExprContext(self, QLangParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 483
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 484
                        self.match(QLangParser.T__13)
                        self.state = 485
                        self.expr(9)
                        pass

                    elif la_ == 7:
                        localctx = QLangParser.OrExprContext(self, QLangParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 486
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 487
                        self.match(QLangParser.T__14)
                        self.state = 488
                        self.expr(8)
                        pass

             
                self.state = 493
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,50,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[30] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 12)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 11)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 7)
         




