import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
import os
import sys

### FUNCTIONS ###

def make(size):
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot()
    return fig, ax

def readFile(path):
    return pd.read_table(path, header=None)

def getAni(file):
    size = len(file)
    pairs = [[j, i] for j in range(int(len(file.T))) for i in range(len(file)) if file[j][size - 1 - i] == 1]
    if len(pairs) == 0:
        return [], []
    x, y = zip(*pairs)
    return x, y

def getHeat(ax, arq, i, j):
    axes = {"z": 2, "y": 1, "x": 0}
    if type(ax) == str:
        ax = axes[ax.lower()]
    size = len(arq)
    return arq[j + ax][size - 1 - i]

def getVectors(ax1, ax2, arq):
    axes = {"z": 2, "y": 1, "x": 0}
    if type(ax1) == str:
        ax1 = axes[ax1.lower()]
    if type(ax2) == str:
        ax2 = axes[ax2.lower()]

    pairs = [[j, i] for j in range(int(len(arq.T) / 3)) for i in range(len(arq))]

    x, y = zip(*pairs)
    size = len(arq)
    
    pairs = [[arq[j + ax1][size - 1 - i], arq[j + ax2][size - 1 - i]] for j in range(0, len(arq.T), 3) for i in range(len(arq))]
    u, v = zip(*pairs)

    return x, y, u, v

def getIm(ax, arq):
    return [[getHeat(ax, arq, i, j) for j in range(0, len(arq.T), 3)] for i in range(len(arq))]

def selectImAx(ax):
    axes = {"z": 2, "y": 1, "x": 0}
    axes_ = {2: "z", 1: "y", 0: "x"}
    if type(ax) == str:
        ax = axes[ax.lower()]
    if ax == 2:
        return axes_[0], axes_[1], axes_[2]
    elif ax == 1:
        return axes_[0], axes_[2], axes_[1]
    elif ax == 0:
        return axes_[1], axes_[2], axes_[0]

def plotByDirectory(path):
    filesList = []
    filesList = os.listdir(path)
    count = 0
    for fileName in filesList:
        filePath = path + fileName
        print('save image file: ', fileName)
        saveImages(filePath)
    return count

def saveImages(filePath):
    file = readFile(filePath)
    fileName = Path(filePath).stem
    fig, ax = make([Nx, Ny])

    ax1, ax2, ax3 = selectImAx("z")
    
    vecs = getVectors(ax1, ax2, file)
    ax.quiver(*vecs, linewidth=5, angles='xy', scale_units='xy', scale=2.0, pivot="mid")
    
    if (hasAni == True): ax.scatter(xAni, yAni, color='green', s=300.0)
    
    ax.set_xlabel(fr"${ax1}$", size=20)
    ax.set_ylabel(fr"${ax2}$", size=20)
    im = ax.imshow(getIm(ax3, file), cmap='bwr', vmin=-1, vmax=1, interpolation='none')
    bar = plt.colorbar(im)
    bar.set_label(fr"$m_{ax3}$", size=20)
    ybot, ytop = ax.get_ylim()
    xleft, xright = ax.get_xlim()

    ax.set_ylim([min([ybot, ytop]), max([ybot, ytop])])
    ax.set_xlim([min([xleft, xright]), max([xleft, xright])])
    fig.savefig("images/" + fileName + ".jpeg", bbox_inches='tight')
    
### END FUNCTIONS ###

### MAIN PROGRAM ###

Nx = Ny = 40
ani = False
hasAni = False
xAni = yAni = 0

if (os.path.exists('./in/ani.in')):
    hasAni = True
    ani = readFile('./in/ani.in')
    xAni, yAni = getAni(ani)

plotByDirectory('files/')

### END ###