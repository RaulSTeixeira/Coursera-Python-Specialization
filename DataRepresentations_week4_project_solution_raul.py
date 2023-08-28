# MADE BY RAUL TEIXEIRA - 2023


"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

IDENTICAL = -1

def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    lenght1 = len (line1)
    lenght2 = len (line2)    
            
    if lenght1 > lenght2:
        shorter_line = line2
        long_line = line1
    else:
        shorter_line = line1
        long_line = line2 
     
    
    if lenght1 == lenght2 and line1 in line2:
        index = IDENTICAL
        
    else:
        aux = 0
        index = 0
        for pos in range(0,len(shorter_line)):
            if shorter_line[pos] != long_line[pos] and (aux == 0):
                index = pos
                aux += 1
            elif (aux==0):
                index = pos + 1
                            
    return index


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    
    minimum_lengh = min (len(line1), len(line2))
        
    if "\n" in (line1 or line2):
        return ""
    elif idx > minimum_lengh or idx <0:
        return ""
    else:
        mid= "=" * idx + "^"
        output= [line1,"\n", mid, "\n", line2,"\n"] 
        return "".join(output)   
    
        
#print(singleline_diff_format("abcdef", "abc", -1))

def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    len1 = len(lines1)
    len2 = len(lines2)
    
    min_len = min(len1, len2)
    indices = range(0, min_len, 1)
        
    #print(len1,len2,indices)
    
    if (min_len == 0 and len1 == len2):
        output_diff = (IDENTICAL, IDENTICAL)
    elif (min_len == 0 and len1 != len2):
        output_diff = (0, 0)
    else:
        for indice in indices:
            if singleline_diff(lines1[indice],lines2[indice]) != IDENTICAL:
                output_diff = (indice, singleline_diff(lines1[indice],lines2[indice]))
                break
            if len1 != len2:
                output_diff = (min_len, 0)
            else:
                output_diff = (IDENTICAL, IDENTICAL)
            
    return output_diff

#print(multiline_diff(["abc","def"], ["abc","def"]))

def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    
    with open(filename,"rt",encoding='utf-8') as text_file:
        doc_text = text_file.readlines()
               
    #print(lst_text)
    
    text_file.close()
    
    output=[]
    for lines in doc_text:
        output.append(lines.rstrip())
    
    return output

#print(get_file_lines("text_file_example.txt"))

def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    file1_lines=[]
    file2_lines=[]
    
    file1_lines = get_file_lines(filename1)
    file2_lines = get_file_lines(filename2)
    
    #print(file1_lines,file2_lines)
    
    output1 = multiline_diff(file1_lines, file2_lines)
    #print (output1)
    
    if output1 == (-1,-1):
        return "No differences\n"
    else:
        line = output1[0]
        index = output1[1]
        #print(line)
        #print(index)
        output2 = singleline_diff_format(file1_lines[line], file2_lines[line], index)
        #print(output2)
        output_final = ["Line ",str(line),":","\n",output2] 
        return "".join(output_final)
    
    
print(file_diff_format("text_file1.txt", "text_file2.txt"))
    