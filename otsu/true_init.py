"""
  AE = 76

  for1:
  4 * (1 + 1 + 4)
  4 * 6 = 24

  for2:
  4 * (1 + 1 + 1)
  4 * 3 = 12

  for3:
  20 * (1)
  20 * 1 = 20


  AI = 42

  for1:
  4 * (1 + 1 + 1 + 1 + 1 + 1 + 1 + 1)
  4 * 8 = 32

  for2:
  4 * (1 + 1)
  4 * 2 = 8


  O = 3

  C = 28

  for1:
    4 * (1 ) = 4

  for2:
    4 * (1 ) = 4

  for3:
    20 * (1 ) = 20


==================================================================
  preFunc

  AE = 

  for1
    4 * (1 + 1 + 1 + [
      for2
        3 * (1 + 1 + [
          for3
            1 * (4)
        ] + 1 + 1 + [
          for4
            TAMANHO * (1 + [
              for5
                KZÃO * ()
            ])

        ])
    ] )



  AI = 

  O = 

  C

=====================================================================
  func

  AE = 

  AI = 

  O = 

  C

=====================================================================
  postFunc

  AE = 

  AI = 

  O = 

  C

=====================================================================












  INPUT_PATH = 2
  FILES = 2
  nImg = 3
  file = 4
  path = 4
  RX = 4
  RY = 4
  Img = 4
  OrigImg = 4


  X =
  O =
  ResX =
  ResY =
  n =
  Y =
  oI =
  my_color =
 """

"""
  FOR - Atribuições explícitas

  for file in tqdm(Files[:nImg]) = 4
  for i in range(nImg) = 4
  for i in range(20): = 20



 """


INPUT_PATH = 'D:/Users/diego/Google Drive/UNEB/ADocencia/EP/datasets/faces'
# 'D:/Users/diego/Google Drive/UNEB/ADocencia/EP/datasets/short_faces'
#'D:/Users/diego/Google Drive/NOTEBOOKS/IA WORKS/datasets/Concrete/Positive'
Files=os.listdir(INPUT_PATH)

nImg=len(Files)

X=[]
O=[]
ResX=[]
ResY=[]
n=[]

nImg=4

for file in tqdm(Files[:nImg]): # tqdm(Files[:nImg]): #

    path=os.path.join(INPUT_PATH, file)
    X.append([])
    O.append([])

    RX, RY, Img, OrigImg = image_loader(path,True,True) # returns a grayscale image of the same size. bool prm: plot RGB & plot grayscale

    n.append(Img.shape[0])

    ResX.append(RX)
    ResY.append(RY)
    X[-1].append(Img)
    O[-1].append(OrigImg)


Y=[]
oI=[]

for i in range(nImg):
    Y.append([])
    oI.append([])
    Y[-1]=X[i][0]
    oI[-1]=O[i][0]


ResX=[]
ResY=[]

my_color = []
my_color.append('#%06X' % 0)
my_color.append('#%06X' % 0xFFFFFF)
for i in range(20):
    my_color.append('#%06X' % randint(0, 0xFFFFFF))

L=256

nexp=1

Kmax=4
