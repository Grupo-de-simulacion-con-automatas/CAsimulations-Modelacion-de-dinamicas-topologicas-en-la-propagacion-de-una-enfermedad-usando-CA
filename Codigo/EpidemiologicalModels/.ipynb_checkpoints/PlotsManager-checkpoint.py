import numpy as np
import matplotlib.pyplot as plt

def _spline3(A):     #spline cubico para la lista de coordenadas A
    n = len(A); l = [1]; B = [0] ; g = [0]; gn = 0; C = [0]*n
    alpha = []; spline = []; a = []; h = []; x = []; y = []*(n-1)
    for i in range(n):
        a.append(A[i][1])
    for i in range(n-1):
        xh = A[i+1][0]-A[i][0]; h.append(xh)
    for i in range(1, n-1):
        xa = (3/h[i])*(a[i+1]-a[i])-(3/h[i-1])*(a[i]-a[i-1]); alpha.append(xa)
    for i in range(1, n-1):
        xl = 2*(A[i+1][0]-A[i-1][0])-h[i-1]*B[i-1]; l.append(xl)
        xb = h[i]/l[i]; B.append(xb)
        xg = (alpha[i-1]-h[i-1]*g[i-1])/l[i]; g.append(xg)
    l.append(1); g.append(0)
    for i in range(n-1):
        j = (n-1)-(i+1)
        xC = g[j]-B[j]*C[j+1]; C[j] = xC
        xy = ((a[j+1]-a[j])/h[j])-(h[j]/3)*(C[j+1]+2*C[j]); y.append(xy)
        xx = (C[j+1]-C[j])/(3*h[j]); x.append(xx)
    for i in range(n-1):
        j=(n-1)-(i+1)
        S3 = [a[i],y[j],C[i],x[j]]; spline.append(S3)
    return np.array(spline)

def plotSolutions(variables, etiquetas, colores, title, limit=True):
    if len(etiquetas) != len(variables):
        print("La cantidad de etiquetas debe ser igual a la cantidad de variables")
    elif len(colores) != len(variables):
        print("La cantidad de colores debe ser igual a la cantidad de variables")
    else:
        for j in range(len(variables)):
            funcion = []; cond = []; x = []; y = []
            A = variables[j]
            SP = _spline3(A)
            for i in range(len(_spline3(A))):
                xa = np.linspace(A[i,0],A[i+1,0] - 0.0001,11); x = np.concatenate((x,xa))
                ya = SP[i,0] + SP[i,1]*(xa-A[i,0]) + SP[i,2]*(xa-A[i,0])**2 + SP[i,3]*(xa-A[i,0])**3
                y = np.concatenate((y,ya))
            plt.plot(x,y,c = colores[j],label = etiquetas[j])
    if limit == True:
        plt.plot(x, x**0, 'k--')
        plt.ylim(0,1.05)
    plt.title(title)
    plt.xlabel("Time")
    plt.legend(loc=0)
    plt.show()