
def BuildOTSUTables2(frq,L): # 2 AE
    
    H=np.zeros((L,L),dtype=float) # 2 AI, 1 AE
    
    C=frq[0] # 1 AI, 1 AE
    for i in range(1,L): # 1 AI, N (1 AE, 1 C)
        C+=(i+1)*frq[i] # 4 AI, 1 AE, 3 O

    for i in range(L): # 1 AI, N (1 AE, 1 C)
        p = frq[i] # 2 AI, 1 AE
        s = (i+1)*frq[i] # 3 AI, 1 AE, 2 O
        if p>0: # 1 AI, 1 C
            H[i,i]=p*(int(s/p)-C)**2 #  4 AI, 4 O, 1 AE
        for j in range(i+1,L): # 2 AI, 1 O, N (1 AE, 1 C)
            p+=frq[j] # 3 AI, 1 AE
            s+=(j+1)*frq[j] # 4 AI, 1 AE, 2 O
            if p>0: # 1 C
                H[i,j]=p*(int(s/p)-C)**2 # 4 AI, 4 O, 1 AE

    return H

def FUNOBJ_PC(T,K,H,L): # 4 AE

    t=[-1]+list(np.array(T)-1)+[L-1] # 2 AI, 4 O, 1 AE
    
    Q=0 # 1 AE
    for i in range(K): # 1 AI, N (1 AE, 1 C)
        Q+=H[t[i]+1,t[i+1]] # 6 AI, 3 O, 1 AE
           
    return Q

def segment(K,L,img): # 3 AE
         
    if K<2 or K>6: # 2 AI, 2 C
        print("K fora do intervalo 2-4")
        return []
    else:  
        
        bg=time.time() # 1 AE
        Qmax=0 # 1 AE
        fMax=[] # 1 AE

        # calcula histograma

        hist_max, p = histo(img,L) # 2 AI, 2 AE
        
        H=BuildOTSUTables2(p,L) # 2 AI, 1 AE
    
        f=[] # 1 AE
        for i in range(K-1): # 1 AI, 1 O, N (1 AE, 1 C)
            f.append(i) # 1 AI
 
        init_time=time.time()-bg # 1 AE, 1 AI, 1 O   
        
        bg=time.time() # 1 AE
        itera=0 # 1 AE
        a=L-K+2 # 2 AI, 2 O, 1 AE
        
        if K==2: # 1 AI, 1 C
            for f[0] in range(0,a): # 1 AI, N (1 AE, 1 C)
                itera+=1 # 1 AI, 1 AE, 1 O
                Q=FUNOBJ_PC(f,K,H,L) # 4 AI, 1 AE
#                 print('calculo com thresholds',f,Q)
                if Q>Qmax: # 2 AI, 1 C
                    Qmax=Q # 1 AI, 1 AE
                    fMax=f.copy() # 1 AE

        elif K==3: # 1 AI, 1 C
            b=a+1 # 1 AI, 1 O, 1 AE
            for f[0] in range(0,a): # 1 AI, N (1 AE, 1 C)
                e=f[0]+1 # 1 AI, 1 O, 1 AE
                for f[1] in range(e,b): # 2 AI, N (1 AE, 1 C)
                    itera+=1 # 1 AI, 1 AE, 1 O
                    Q=FUNOBJ_PC(f,K,H,L) # 4 AI, 1 AE
#                     print('calculo com thresholds',f,Q)
                    if Q>Qmax: # 2 AI, 1 C
                        Qmax=Q # 1 AI, 1 AE
                        fMax=f.copy() # 1 AE

        elif K==4: # 1 AI, 1 C
            b=a+1 # 1 AI, 1 O, 1 AE
            d=b+1 # 1 AI, 1 O, 1 AE
            for f[0] in range(0,a): # 1 AI, N (1 AE, 1 C, 1 O)
                e=f[0]+1 # 1 AI, 1 O, 1 AE
                for f[1] in range(e,b): # 2 AI, N (1 AE, 1 C, 1 O)
                    g=f[1]+1 # 1 AI, 1 O, 1 AE
                    for f[2] in range(g,d): # 2 AI, N (1 AE, 1 C, 1 O)
                        itera+=1 # 1 AI, 1 AE, 1 O
                        Q=FUNOBJ_PC(f,K,H,L) # 4 AI, 1 AE
                        if Q>Qmax: # 2 AI, 1 C
                            Qmax=Q # 1 AI, 1 AE
                            fMax=f.copy() # 1 AE

        elif K==5: # 1 AI, 1 C
            b=a+1 # 1 AI, 1 O, 1 AE
            d=b+1 # 1 AI, 1 O, 1 AE
            h=d+1 # 1 AI, 1 O, 1 AE
            for f[0] in range(0,a): # 1 AI, N (1 AE, 1 O, 1 C)
                e=f[0]+1 # 1 AI, 1 O, 1 AE
                for f[1] in range(e,b): # 2 AI, N (1 AE, 1 C, 1 O)
                    g=f[1]+1 # 1 AI, 1 O, 1 AE
                    for f[2] in range(g,d): # 2 AI, N (1 AI, 1 O, 1 C)
                        l=f[2]+1 # 1 AI, 1 O, 1 AE
                        for f[3] in range(l,h): # 2 AI, N (1 AE, 1 O, 1 C)
                            itera+=1 # 1 AI, 1 O, 1 AE
                            Q=FUNOBJ_PC(f,K,H,L) # 4 AI, 1 AE
                            if Q>Qmax: # 2 AI, 1 C
                                Qmax=Q # 1 AI, 1 AE
                                fMax=f.copy() # 1 AE

        elif K==6: # 1 AI, 1 C
            b=a+1 # 1 AI, 1 O, 1 AE
            d=b+1 # 1 AI, 1 O, 1 AE
            h=d+1 # 1 AI, 1 O, 1 AE
            q=h+1 # 1 AI, 1 O, 1 AE
            for f[0] in range(0,a): # 1 AI, N (1 AE, 1 O, 1 C)
                e=f[0]+1 # 1 AI, 1 O, 1 AE
                for f[1] in range(e,b): # 2 AI, N (1 AE, 1 C, 1 O)
                    g=f[1]+1 # 1 AI, 1 O, 1 AE
                    for f[2] in range(g,d): # 2 AI, N (1 AI, 1 O, 1 C)
                        l=f[2]+1 # 1 AI, 1 O, 1 AE
                        for f[3] in range(l,h):  # 2 AI, N (1 AE, 1 O, 1 C)
                            s=f[3]+1 # 1 AI, 1 O, 1 AE
                            for f[4] in range(s,q): # 2 AI, N (1 AE, 1 O, 1 C)
                                itera+=1 # 1 AI, 1 AE, 1 O
                                Q=FUNOBJ_PC(f,K,H,L) # 4 AI, AE
                                if Q>Qmax: # 2 AI, 1 C
                                    Qmax=Q # 1 AI, 1 AE
                                    fMax=f.copy() # 1 AE

        iter_time=(time.time()-bg) # 1 AE, 1 AI, 1 O
                            
    return init_time, iter_time, itera, fMax