import sys
import time

# --------------------------------------------------------
# Get the filename as an input parameter
# --------------------------------------------------------
inputfiledir = 'C:\\Users\\Ian\\Dropbox\\Python\\umzi\\data'
inputfiledir+='\\'
inputfilename = r''
inputfilename+=inputfiledir
inputfilename+='mpaskevicius'
inputfilename+='.txt'

# --------------------------------------------------------
# Open the input file
# --------------------------------------------------------
fin = open(inputfilename, 'r')

# --------------------------------------------------------
# Initialise all the variables
# --------------------------------------------------------
vChapter = 0
vChapterTxt = ''
vError = 0
vLine = 0
vOutput = ''
vPage = 0
vRev = ''
vShowBiblio = None

# --------------------------------------------------------
# Print output headings
# --------------------------------------------------------
vOutput = 'Chapter | Page | Line | Reference'
print (vOutput)

# --------------------------------------------------------
# Loop through each line in the file
# --------------------------------------------------------
while 1:
    line=fin.readline() # check for EOF
    if not line: break
    
    # Count the lines
    vLine+=1
    
    # Extract the page number if present
    if line.count('Page ') > 0 and line.count(' of ') > 0: 
        vPage = line[5:line.find(' of ')]
        continue
    
    # If Reference section is reached then output the references
    if line[0:12] == '@@References':
        vShowBiblio = True;
#        print ('--------------------------------------------------')
#        print ('References')
#        print ('==================================================')
        continue
    
    if vShowBiblio:
        vOutput = line
#        print (vOutput, end='')
        continue
    
    # TODO See if the line contains an opening bracket but no closing bracket (i.e a broken reference)
    if line.count(' (') > 0 and line.count(')') == 0:
        vError+=1
        print (vLine, line)
        continue

    # Look for start of abstract
    if line[0:10] == '@@Abstract':
        vChapterTxt='ABSTRACT'
        
    # Look for chapter headings
    elif line[0:2] == '@@':
        vChapter+=1
        vChapterTxt='CH'+str(vChapter)

    # If no opening bracket then there is no reference
    if line.count('(') == 0: continue

    # Replace "; " with ")(" 
    s = line.replace("; ",")(")

    # Loop through the characters and process each reference in brackets
    while not s.count('(') == 0:
        s = s[s.find('(')+1:]
        vRef = s[0:s.find(')')]

        # Ignore if reference starts with: Figure
        if vRef[0:7] == ('Figure '): continue

        # Skip if reference starts with: Figure
        if vRef[0:9] == ('Appendix '): continue

        # Ignore if reference starts with: Interviewee
        if vRef[0:12] == ('Interviewee '): continue

        # Ignore if the year doesn't start with 1 or 2
        if vRef.count(', 1') == 0 and vRef.count(', 2') == 0: continue

        ## TODO Ignore if there is not one comma only
        if not vRef.count(',') == 1: continue
   
        # We have a reference!
        # Strip out the page number if there is one
        if vRef.count(':') > 0:
            vRef = vRef[0:vRef.find(':')]

        # Output the Line Number | Reference | Chapter
        vOutput = vChapterTxt+'|'+vPage+'|'+str(vLine)+'|'+vRef
        print (vOutput)

    # End while

# End while

# Print chapter count
#print ('--------------------------------------------------')
#print ('There are',str(vChapter),'chapters in this dissertation')
#print ('==================================================')

# Print error count
if vError > 0:
    print ('##################################################')
    print ('There are',str(vError),'ERROR LINES. Please fix!')
    print ('##################################################')
    
# --------------------------------------------------------
# Close the input file
# --------------------------------------------------------
fin.close()
