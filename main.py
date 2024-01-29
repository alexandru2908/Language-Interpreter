# from .Lexer import Lexer
from .Lexer import Lexer

from sys import argv

spec =[("NIMIC",r"\(\)"),("SPACE",r"\ "),("DESCHISA",r"\("),("INCHISA",r"\)"),("LAMBDA","lambda"),("PLUS",r"\+"),("CONCAT",r"\++"),("LINE","\n"),
       ("LITERA","[a-z]"),(":",r"\:"),("TAB","\t"),("NUM","[1-9][0-9]*")]


def print_for_okop_0(num_list1):
    s=""
    s = s+"( "
    niv_current = 0
    for i in range(len(num_list1)):
        if num_list1[i][1]-1 > niv_current:
            for j in range(niv_current, num_list1[i][1]-1):
                s = s + "( "
            niv_current = num_list1[i][1]-1
            if num_list1[i][0] == 100:
                s= s + "() "
                continue 
            s = s + str(num_list1[i][0]) + " "
            
        elif num_list1[i][1]-1 == niv_current:
            if num_list1[i][0] == 100:
                s= s + "() "
                continue
            s = s + str(num_list1[i][0]) + " "
            
        elif niv_current > num_list1[i][1]-1:                   

            if num_list1[i][1] -1 < 0 and ( abs(num_list1[i-1][1] ) != abs(num_list1[i][1]) ):
                s= s + "( "+ str(num_list1[i][0])+" ) "
                niv_current = abs(num_list1[i][1]) -2
                continue

            if num_list1[i][1] -1 < 0:
                if num_list1[i][0] == 100:
                    s= s + "() ) "
                    niv_current -= 1
                    continue
                niv_current -= 1
                s = s + str(num_list1[i][0]) + " ) "
                continue
            
            for j in range(niv_current, num_list1[i][1]-1,-1):
                s = s + ") "
        
            niv_current = num_list1[i][1]-1
            
    for i in range(- (num_list1[-1][1])-1):
        s = s + ") "
    print(s[:-1])
    pass


def print_concat(num_list1):

    print(  "(",end=" ")

    for i in range(len(num_list1)):
        
        for j in range(num_list1[i][1]-1):
            print("(",end=" ")
            
        if num_list1[i][0] == 100:
            if num_list1[i][1] != 0:
                print("()",end=" ")
            continue
    
        if num_list1[i][1] >= 0:  
            print(num_list1[i][0],end=" ")

        if num_list1[i][1] < 0 and ( abs(num_list1[i-1][1]) == abs(num_list1[i][1]) ):
            print(num_list1[i][0],end=" ")
        if num_list1[i][1] < 0 and ( abs(num_list1[i-1][1]) != abs(num_list1[i][1]) ):
            print("( "+ str(num_list1[i][0])+" )",end=" ")
              
    for i in range(- (num_list1[-1][1])-1):
        print(")",end=" ")
    print(")")
    

def return_suma(i,lexer):

    num_list,pos=compute_numbers(lexer[i:])
    ok=0
    suma=0
    for j in range(len(num_list)):
        if num_list[j][0] !=100:
            ok=1
            break
    if ok==1:
        for j in range(len(num_list)):
            suma += num_list[j][0]
    return suma    
            

def compute_numbers(lexer):
    
    index_list = [0]
    i=0
    l=[]
    while((len(index_list) > 0) and (i < len(lexer))):
        if lexer[i][0] == "DESCHISA":
            index_list.append(index_list[-1]+1)
            
        elif lexer[i][0] == "INCHISA":
            index_list.pop()
            if (l[-1][1] > 0):
                l[-1] = (l[-1][0], -l[-1][1]) 
                
        elif lexer[i][0] == "NUM":
            l.append((int(lexer[i][1]),index_list[-1]))
            
        elif lexer[i][0] == "NIMIC":
            l.append((100,index_list[-1]))
        i+=1
    return l,i

def manage_concat(lexer,i):
    num_list,pos=compute_numbers(lexer[i:])
    
    for j in range(len(num_list)):
        if(num_list[j][1] < 0):
              num_list[j] = (num_list[j][0],num_list[j][1]+1)
        else:
            num_list[j] = (num_list[j][0],num_list[j][1]-1)
            
    print_concat(num_list)
    
def compute_lambda(lexer,parametru_lambda_mare):
    ct=0
    if lexer[len(lexer)-1][0] == "NUM":
        aplicatie = lexer[-1]
        inceput_aplicatie = len(lexer)-1   
    elif lexer[len(lexer)-1][0] == "INCHISA":
        for k in range(len(lexer)-1,-1,-1):
            if lexer[k][0] == "DESCHISA":
                aplicatie = lexer[k:]
                inceput_aplicatie = k
                break

    elif lexer[len(lexer)-1][0] == "LITERA":
        k = len(lexer)-2
        while( k >= 0 ):
            if lexer[k][0] == ":":
                k -= 3
            else:
                break
        aplicatie = lexer[k+1:]
        inceput_aplicatie = k+1 

    for i in range(len(lexer)):
        if lexer[i][0] == ":":
            break

    expresie = lexer[i+1:inceput_aplicatie]

    j = 0
    while (True):
        if expresie[j][1] == parametru_lambda_mare[1]:   
            k=j
            ok=0
            
            if expresie[j-1][0] == ":" and expresie[j-2][1] == parametru_lambda_mare[1]:
                ok=1

            if expresie[j-1][0] == "LAMBDA":
                ok=1
            if ok == 1:
                j += 1
                if j > len(expresie)-1:
                    break
                continue
            
            inainte=expresie[:j]
            dupa=expresie[j+1:]
            if type(aplicatie) == tuple:
                expresie=inainte
                expresie.append(aplicatie)
                expresie=expresie+dupa
            else:
                expresie=inainte+aplicatie+dupa
                j += len(aplicatie)-1
        if j < len(expresie)-1:
            j+=1
        else:
            break
    #ret expr 
    return expresie
            
def main():
    if len(argv) != 2:
        return 0
    
    filename = argv[1]
    s=""
    f = open(filename,"r")
    lines = f.readlines()
    f.close()
    for i in lines:
        s += i
    l = Lexer(spec).lex(s)
    s=""
    lexer = []
    for i in l:
        if not (i[0] == "LINE" or i[0] == "TAB" or i[0] == "SPACE"):
            lexer.append(i)
            s = s + i[1]
    i=0        
    ok_op=0
    num_list1=[]
    
    #se face decat pt lambda aici
    while(i < len(lexer)-1):
        if lexer[i][0] == "DESCHISA" and lexer[i+1][0] == "LAMBDA":
            
            ct = 0
            for j in range(i+1,len(lexer)):
                if lexer[j][0] == "DESCHISA":
                    ct += 1
                if lexer[j][0] == "INCHISA":
                    ct -= 1
                if ct < 0:
                    break
                
            expresie = compute_lambda(lexer[i+1:j],lexer[i+2])
            inainte = lexer[:i]
            dupa = lexer[j+1:]
            lexer = inainte + expresie + dupa
            i=0
            continue
        i+=1
    
    i = 0
    while(i < len(lexer)-1):
        if lexer[i][0] == "DESCHISA" and (lexer[i+1][0] == "NUM" or lexer[i+1][0] == "NIMIC") and ok_op != 1:
            j = i - 1
            ok_op = 0
            
            while(j >= 0 and lexer[j][0] == "DESCHISA"):
                j -= 1
            num_list,pos = compute_numbers(lexer[j+1:])
            i = pos + i
            num_list1 = num_list
        else:
            if lexer[i][0] == "DESCHISA" and lexer[i+1][0] == "PLUS":                
                print(return_suma(i+2,lexer))
                ok_op=1
                break
            if lexer[i][0] == "DESCHISA" and lexer[i+1][0] == "CONCAT":
                manage_concat(lexer,i+2)                
                ok_op=1
        i+=1
            
    if ok_op==0:
        if len(num_list1) == 0:
            print(lexer[0][1])
        else:
            print_for_okop_0(num_list1)
    else:
        if len(num_list1) == 0:
            print("",end="")
        
        
    

if __name__ == '__main__':
    main()
