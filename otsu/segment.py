
def FUNOBJ_PC(T,K,H,L): # 4 AE

    t=[-1]+list(np.array(T)-1)+[L-1] # 2 AI, 4 O, 1 AE
    
    Q=0 # 1 AE
    for i in range(K): # 1 AI, K (1 AE, 1 C)
        Q+=H[t[i]+1,t[i+1]] # K ( 6 AI, 3 O, 1 AE)
           
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
        for i in range(K-1): # 1 AI, 1 O, K-1 (1 AE, 1 C)
            f.append(i) # 1 AI
 
        init_time=time.time()-bg # 1 AE, 1 AI, 1 O   
        
        bg=time.time() # 1 AE
        itera=0 # 1 AE
        a=L-K+2 # 2 AI, 2 O, 1 AE
        
        if K==2: # 1 AI, 1 C
            for f[0] in range(0,a): # 1 AI, 255 - K+2 (1 AE, 1 C)
                itera+=1 # 255 - K+2 (1 AI, 1 AE, 1 O)
                Q=FUNOBJ_PC(f,K,H,L) # 255 - K+2( 4 AI, 1 AE)
#                 print('calculo com thresholds',f,Q)
                if Q>Qmax: # 255 - K+2( 2 AI, 1 C)
                    Qmax=Q # 1 AI, 1 AE
                    fMax=f.copy() # 1 AE

        elif K==3: # 1 AI, 1 C
            b=a+1 # 1 AI, 1 O, 1 AE
            for f[0] in range(0,a): # 1 AI, 255 - K+2 (1 AE, 1 C)
                e=f[0]+1 # 255 - K+2( 1 AI, 1 O, 1 AE)
                for f[1] in range(e,b): # 2 AI, 255 - K+3 (1 AE, 1 C)
                    itera+=1 # 255 - K+3 (1 AI, 1 AE, 1 O)
                    Q=FUNOBJ_PC(f,K,H,L) # 255 - K+3 (4 AI, 1 AE)
#                     print('calculo com thresholds',f,Q)
                    if Q>Qmax: # 255 - K+3 (2 AI, 1 C)
                        Qmax=Q # 1 AI, 1 AE
                        fMax=f.copy() # 1 AE

        elif K==4: # 1 AI, 1 C
            b=a+1 # 1 AI, 1 O, 1 AE
            d=b+1 # 1 AI, 1 O, 1 AE
            for f[0] in range(0,a): # 1 AI, 255 - K+2 (1 AE, 1 C, 1 O)
                e=f[0]+1 # 255 - K+3 (1 AI, 1 O, 1 AE)
                for f[1] in range(e,b): # 2 AI, 255 - K+3 (1 AE, 1 C, 1 O)
                    g=f[1]+1 # 255 - K+3 (1 AI, 1 O, 1 AE)
                    for f[2] in range(g,d): # 2 AI, 255 - K+4 (1 AE, 1 C, 1 O)
                        itera+=1 # 255 - K+4 (1 AI, 1 AE, 1 O)
                        Q=FUNOBJ_PC(f,K,H,L) # 255 - K+4 (4 AI, 1 AE)
                        if Q>Qmax: # 255 - K+4 (2 AI, 1 C)
                            Qmax=Q # 1 AI, 1 AE
                            fMax=f.copy() # 1 AE

        elif K==5: # 1 AI, 1 C
            b=a+1 # 1 AI, 1 O, 1 AE
            d=b+1 # 1 AI, 1 O, 1 AE
            h=d+1 # 1 AI, 1 O, 1 AE
            for f[0] in range(0,a): # 1 AI, 255 - K+2(1 AE, 1 O, 1 C)
                e=f[0]+1 # 255 - K+2 1 AI, 1 O, 1 AE
                for f[1] in range(e,b): # 2 AI,255 - K+3 (1 AE, 1 C, 1 O)
                    g=f[1]+1 # 255 - K+3 (1 AI, 1 O, 1 AE)
                    for f[2] in range(g,d): # 2 AI, 255 - K+4 (1 AI, 1 O, 1 C)
                        l=f[2]+1 # 255 - K+4 (1 AI, 1 O, 1 AE)
                        for f[3] in range(l,h): # 2 AI, 255 - K+5 (1 AE, 1 O, 1 C)
                            itera+=1 # 255 - K+5 (1 AI, 1 O, 1 AE)
                            Q=FUNOBJ_PC(f,K,H,L) # 255 - K+5 (4 AI, 1 AE)
                            if Q>Qmax: # 255 - K+5 (2 AI, 1 C)
                                Qmax=Q # 1 AI, 1 AE
                                fMax=f.copy() # 1 AE

        elif K==6: # 1 AI, 1 C
            b=a+1 # 1 AI, 1 O, 1 AE
            d=b+1 # 1 AI, 1 O, 1 AE
            h=d+1 # 1 AI, 1 O, 1 AE
            q=h+1 # 1 AI, 1 O, 1 AE
            for f[0] in range(0,a): # 1 AI, 255 - K+2(1 AE, 1 O, 1 C)
                e=f[0]+1 # 255 - K+2 (1 AI, 1 O, 1 AE)
                for f[1] in range(e,b): # 2 AI, 255 - K+3 (1 AE, 1 C, 1 O)
                    g=f[1]+1 # 255 - K+3 (1 AI, 1 O, 1 AE)
                    for f[2] in range(g,d): # 2 AI, 255 - K+4 (1 AI, 1 O, 1 C)
                        l=f[2]+1 # 255 - K+4 (1 AI, 1 O, 1 AE)
                        for f[3] in range(l,h):  # 2 AI, 255 - K+5 (1 AE, 1 O, 1 C)
                            s=f[3]+1 # 255 - K+5 (1 AI, 1 O, 1 AE)
                            for f[4] in range(s,q): # 2 AI, 255 - K+6 (1 AE, 1 O, 1 C)
                                itera+=1 # 255 - K+6 (1 AI, 1 AE, 1 O)
                                Q=FUNOBJ_PC(f,K,H,L) # 255 - K+6 (4 AI, AE)
                                if Q>Qmax: # 255 - K+6 (2 AI, 1 C)
                                    Qmax=Q # 1 AI, 1 AE
                                    fMax=f.copy() # 1 AE

        iter_time=(time.time()-bg) # 1 AE, 1 AI, 1 O
                            
    return init_time, iter_time, itera, fMax


