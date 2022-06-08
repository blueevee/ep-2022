from statistics import mean, stdev
from time import *
from typing import List
from functools import *
from matplotlib import pyplot as plt


def setupFunction():
  fat: int = 1
  start: int = 20

  while start > 1:
    fat *= start
    start -= 1


def measure(fn)-> float:
  before: float = time()
  fn()
  after: float = time()

  return after - before

def goldenRule(desvioPadrao: float, media: float)-> bool:
  return desvioPadrao <= (media * 0.15) # NOT a regra especificada no documento

def experiment(n: int, fn):
  for i in range(n):
    results.append(measure(fn))

  media = mean(results)
  desvioPadrao = stdev(results)

  return media, desvioPadrao


quantidadeDeExperimentos = 30
tamanhoDoExperimento = 100
results: List[float] = []
medias: List[float] = []
desvios: List[float] = []
grResults: List[bool] = []

for i in range(quantidadeDeExperimentos):
  avg, sttdDev = experiment(tamanhoDoExperimento, setupFunction)
  medias.append(avg)
  desvios.append(sttdDev)
  grResults.append(goldenRule(avg, sttdDev))

print("Resultados da verificação da máquina: ", grResults)

plt.plot(medias,label='media')
plt.plot(desvios,label='desvio padrão')
plt.legend(['media','desvio padrão'])
plt.title("Evolução da média e o desvio padrão (atrexp)")
plt.ylabel("tempo (s)")
plt.xlabel("repetição")
plt.show()