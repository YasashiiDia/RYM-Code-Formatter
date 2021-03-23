import sys
import os
import re

sourceFile = sys.argv[1]
sourceName, sourceExtension = os.path.splitext(sourceFile)
targetFile = sourceName + "-formatted.txt"

if sourceExtension != ".py":
    print("Filetype not supported.")
    exit()

# Indentation size in number of white spaces
isize = 4
if len(sys.argv) > 2:
    isize = int(sys.argv[2])
    assert(isize > 0 and isize < 9)

sourceFile = open(sourceFile,"r")
targetFile = open(targetFile,"w")

# Python formatting
import keyword
pykeys = keyword.kwlist
pykeys.remove('or')
pykeys.remove('in')
def python_syntax_highlight(line, color):
    for key in pykeys:
        line = re.sub(key,"[color " + color + "]" + key + "[/color]",line)
    line = re.sub(' in '," [color " + color + "]in[/color] ",line)
    line = re.sub(' or '," [color " + color + "]or[/color] ",line)
    return line

###########################
##  Main formatting loop ##
###########################

level = 0 # Indentation level
prev_level = 0

for i, line in enumerate(sourceFile):
    
    indent = (len(line) - len(line.lstrip()))/isize
    #line = python_syntax_highlight(line, "purple")
    
    if indent.is_integer() and indent > level:
        level, prev_level = indent, level
        #print(i+1,indent,level,"up")
        line = "[blockquote]" + line.lstrip()
        
    elif indent.is_integer() and indent < level:
        level, prev_level = indent, level
        #print(i+1,indent,level,"down")
        line = ''.join(["[/blockquote]" for i in range(int(prev_level-level))]) + line.lstrip()

    if not line.strip():
        line.lstrip()
    targetFile.write(line) 


sourceFile.close()
targetFile.close()
