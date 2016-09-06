"""
Demo of the `streamplot` function.

A streamplot, or streamline plot, is used to display 2D vector fields. This
example shows a few features of the stream plot function:

    * Varying the color along a streamline.
    * Varying the density of streamlines.
    * Varying the line width along a stream line.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


data = np.loadtxt("RadForce-Y")
#data = np.loadtxt("IntField-Y")
#data = np.loadtxt("IncBeam-Y")

x = data[:,0]
y = data[:,1]
z = data[:,2]
force_mod = data[:,3]
force_x = data[:,4]
force_y = data[:,5]
force_z = data[:,6]

arrayLength = (int)(z.shape[0])

#########################################
itemNumList = [] 
itemPositionList = [0]



i=0
start = 0
for z_temp in z:
    if i==arrayLength-1: 
        itemPositionList.append(i+1)
        itemNumList.append(i-start)
        break
    if z_temp!=z[i+1]:
        itemPositionList.append(i+1)
        
        itemNumList.append(i-start+1)
        start = i
    i = i+1
#########################################

layerNum=14 #所在层数

#########################################
#构造新矩阵适用于任意横截面
xx = list(set(x[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])]))
yy = list(set(y[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])]))

xx.sort()
yy.sort()

x_length  = len(xx)
y_length  = len(yy)

X = [[0 for col in range(y_length)] for row in range(x_length)]
Y = [[0 for col in range(y_length)] for row in range(x_length)]

i = 0
for yy_temp in yy:
    j = 0 
    for xx_temp in xx:
        Y[i][j] = yy_temp
        j = j + 1
    i = i + 1
    
i = 0
for xx_temp in xx:
    j = 0 
    for yy_temp in yy:
        X[j][i] = xx_temp
        j = j + 1
    i = i + 1            
                
#########################################

# 初始化一行数据
# x = 原始数据x y = 原始数据y
# input_y  单个数据 每一行y的值
# inputLine_x 经处理后的一行x值 
# inputlinecon 需要填充的一行目标值
# outputline 处理后的目标值
# total 原始数据个数
# 适用于任意横截面初始化
def initLine(x, y, input_y, inputLine_x, inputLineCon, outputLine, total): 
    x = x.tolist()
    
    tempListX = []
    tempListCon = []
    i = 0
    for y_temp in y:
        if y_temp==input_y:
            tempListX.append(x[i])
            tempListCon.append(inputLineCon[i])
        i = i+1
            
    i = 0
    for inputTemp_x in inputLine_x:
        if inputTemp_x in tempListX:
            outputLine.append(tempListCon[i])
            i = i+1              
        else:
            outputLine.append(0)
        
                              
        

#########################################
# 需验证 
i = 0
outLine_force_mod = []
outLine_force_x = []
outLine_force_y = []
outLine_force_z = []
#outLine_force_z = []
for x_line_temp in X:
    outLinetemp = []
    initLine(x[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])],y[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])]
            ,yy[i], x_line_temp, force_x[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])], outLinetemp, itemNumList[layerNum-1])
    outLine_force_x.append(outLinetemp) 
    
    outLinetemp = []
    initLine(x[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])],y[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])]
            ,yy[i], x_line_temp, force_y[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])], outLinetemp, itemNumList[layerNum-1])
    outLine_force_y.append(outLinetemp)
    
    outLinetemp = []
    initLine(x[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])],y[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])]
            ,yy[i], x_line_temp, force_z[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])], outLinetemp, itemNumList[layerNum-1])
    outLine_force_z.append(outLinetemp)
    
    outLinetemp = []
    initLine(x[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])],y[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])]
            ,yy[i], x_line_temp, force_mod[(itemPositionList[layerNum-1]):(itemPositionList[layerNum])], outLinetemp, itemNumList[layerNum-1])
    outLine_force_mod.append(outLinetemp)
    i = i + 1
    
#########################################
#箭头图
plt.figure()
Q = plt.quiver(outLine_force_z, outLine_force_x)

#########################################
#平面图
#im = plt.imshow(outLine_force_mod, cmap=cm.gist_heat,
#                origin='lower')
#                
#plt.colorbar()
#
plt.show()


