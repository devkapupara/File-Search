from pathlib import Path

def RfileSearch(pathlist):

    if len(pathlist) == 0:
        return []
    else:
        if pathlist[0].is_file():
            return [pathlist[0]] + RfileSearch(pathlist[1:])
        else:
            return RfileSearch(list(pathlist[0].iterdir())) + RfileSearch(pathlist[1:])

def getSearchOption():
    
    interest = input("Enter option: ").split()
    valid_input = ['N','E','<','>']
    
    if (interest[0] == 'T'):
        while(interest[0] == 'T' and len(interest) < 2):
            print("ERROR")
            interest = input("Enter again: ").split()
        nInterest = list(map(str, interest[1:])) 
        interest = [interest[0], ' '.join(nInterest)]
        
    elif (interest[0] != 'A' or interest[0] != 'T'):
        while (len(interest) != 2 or interest[0] not in valid_input):
            print("ERROR")
            interest = input("").split()
    
    return interest

def getPaths():
    
    pathTd = input("Enter option: ").split()
    
    while ((len(pathTd) != 2) or (not Path(pathTd[1]).exists())):
        print("ERROR")
        pathTd = input("Enter again: ").split()
        
    (mode, path) = (pathTd[0],Path(pathTd[1]))

    if mode == "D":
        files = list(path.iterdir())
    else:
        files = RfileSearch(list(path.iterdir()))
        files.sort(key = lambda x: str(x).count("/"))

    final_files = []
    
    for i in files:
        if str(i).split('/')[-1][0] != '.':
            final_files.append(i)
            
    return final_files

def requiredFiles(interest, files):

    output = []
    if interest[0] == 'A':
        for i in files:
            output.append(i)

    elif interest[0] == 'N':
        interest[1] = str(interest[1])
        for i in files:
            if i.name[:len(interest[1])] == interest[1]:
                      output.append(i)

    elif interest[0] == 'E':
        interest[1] = str(interest[1])
        if ('.' in interest[1]):
            interest[1] = interest[1].replace('.','')
        for i in files:
            if i.suffix[1:] == interest[1]:
                output.append(i)

    elif interest[0] == 'T':
        interest[1] = str(interest[1])
        
        for i in files:
            try:
                infile = i.open('r')
                for lines in infile:
                    if interest[1] in lines:
                        output.append(i)
            except:
                continue

    elif interest[0] == '>':
        try:
            value = int(interest[1])
            for i in files:
                if i.stat().st_size > value:
                    output.append(i)
        except ValueError:
            raise ValueError

    elif interest[0] == '<':
        try:
            value = int(interest[1])
            for i in files:
                if i.stat().st_size < value:
                    output.append(i)
        except ValueError:
            raise ValueError

    return output

def getAction():

    action = input("Enter option: ")
    while ((action != 'F') and (action != 'D') and (action != 'T')):
        print ("ERROR")
        action = input("Enter again: ")

    return action
        
def main():

    files = getPaths()

    for i in files:
        print (i)

    interest = getSearchOption()

    result = requiredFiles(interest, files)

    if len(result) != 0:
        for i in result:
            print(i)

        choice = getAction()

        if (choice == 'F'):
            for i in result:
                try:
                    infile = i.open('r')
                    print(infile.readline().strip())
                    infile.close()
                except:
                    print("NOT A TEXT")

        if (choice == 'D'):
            for i in result:
                infile = i.open('r')
                newP = Path(str(i) + '.dup')
                outfile = newP.open('w')
                for line in infile:
                    outfile.write(line)
                infile.close()
                outfile.close()

        if (choice == 'T'):
            for i in result:
                i.touch()

if __name__ == '__main__':
    main()
        
                    
    
        

    

    

            
                    
                
            

    
    
    
    
