
INPUT_PATH = 'D:/Users/diego/Google Drive/UNEB/ADocencia/EP/datasets/faces' # 1 AE
# 'D:/Users/diego/Google Drive/UNEB/ADocencia/EP/datasets/short_faces'
#'D:/Users/diego/Google Drive/NOTEBOOKS/IA WORKS/datasets/Concrete/Positive'
Files=os.listdir(INPUT_PATH) # 1 AI, 1 AE

nImg=len(Files) # 1 AI, 1 AE

X=[] # 1 AE
O=[] # 1 AE
ResX=[] # 1 AE
ResY=[] # 1 AE
n=[] # 1 AE

nImg=4 # 1 AE

for file in tqdm(Files[:nImg]): # 2 AI, N(1 AE + 1 C)
    
    path=os.path.join(INPUT_PATH, file) # 2 AI, 1 AE
    X.append([])
    O.append([])
    
    RX, RY, Img, OrigImg = image_loader(path,True,True) # 1 AI, 4 AE
    
    n.append(Img.shape[0])
    
    
    ResX.append(RX) # 1 AI
    ResY.append(RY) # 1 AI
    X[-1].append(Img) # 1 AI
    O[-1].append(OrigImg) # 1 AI


Y=[] # 1 AE
oI=[] # 1 AE

print("numero de imagens: ",nImg)
for i in range(nImg): # 1 AI, N (1 AE + 1 C)
    Y.append([])
    oI.append([])
    Y[-1]=X[i][0] # 2 AI
    oI[-1]=O[i][0] # 2 AI
    #debb
    #print(np.min(Y[-1]),":",np.max(Y[-1]))

ResX=[] # 1 AE
ResY=[] # 1 AE

my_color = [] # 1 AE
my_color.append('#%06X' % 0) # 1 O
my_color.append('#%06X' % 0xFFFFFF) # 1 O
for i in range(20): # N (1 AE + 1 C)
    my_color.append('#%06X' % randint(0, 0xFFFFFF)) # 1 O

L=256 # 1 AE

nexp=11 # 1 AE

Kmax=5 # 1 AE
    
# loop por imagens - test

for j in range(nImg): # 1 AI + 4(1 AE, 1 C)
    
    print("n   K   inTime (Std) itTime (Std) best_thresholds")
    x=ResX[j] # 4(1 AE, 1 AI)
    y=ResY[j] # 4(1 AE, 1 AI)
    N=x*y # 4(1 AE, 2 AI, 1 O)

    for K in range(2,Kmax+1): # 1 AI + 5(1 AE, 1 C)

        InTime=[] # 1 AE
        ItTime=[] # 1 AE

        for i in range(nexp): # 1 AI, 11(1 AE, 1 C)

            inittime,itertime, iterations, thresholds = segment(K,L,Y[j]) # 11(4 AI, 4 AE)

            InTime.append(inittime) # 11 AI
            ItTime.append(itertime) # 11 AI

        print(N,K,np.mean(InTime),'(',np.std(InTime),')',np.mean(ItTime),'(',np.std(ItTime),')',thresholds)

        # fill image

        f=[-1]+list(np.array(thresholds)-1)+[L-1] # 2 AI, 1 AE, 4 O

        # classificando pixels

        Mask=[] # 1 AE
        for i in range(N): # 1 AI, N (1 AE, 1 C)
            for k in range(K): # N (1 AI, K (1AE, 1C))
                if Y[j][i]>f[k] and Y[j][i]<=f[k+1]: # NK(4AI, 1O, 3C)
                    Mask.append(colors.hex2color(my_color[k])) # 2 AI
                    break
