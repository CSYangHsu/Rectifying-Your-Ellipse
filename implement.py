# -*- coding: utf-8 -*-
"""「Linear Algebra - hw4」的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yzQrf7qVjOkgZrW1nDVln-aznJTJs5r5
"""

#!/usr/bin/env python
# coding: utf-8

# In[4]:
import numpy as np
import matplotlib.image as img
import matplotlib.pyplot as plt
import math

# this is for algorithm 1
def fit_ellipse_general(sp):
    # from assignment 3
    # fit the model for the given points:  
    #      x[0]xx + x[1]xy + x[2]yy + x[3]x + x[4]y = 1
    
    n=len(sp)
    A = np.zeros((n, 5))
    b = np.ones((n))
    for i in range(n):
        pt = sp[i]
        A[i, :] = [pt[0]*pt[0], pt[0]*pt[1], pt[1]*pt[1], pt[0], pt[1]]
        
    x = np.linalg.lstsq(A, b, rcond=None)[0]
    return x


# this is for algorithm 1
def translation(x) :
    # do the translation for general_to_standard
    # input x means
    #      x[0] xx + x[1] xy + x[2] yy + x[3]x + x[4] y = 1
    #       a xx + b xy + c yy + d x + e y = 1
    # for the general model
    # output xp means
    #     xp = [a', b', c', z, w]
    # for the semi-standard model
    # a'(x-z)(x-z) + b'(x-z)(y-w) + c'(y-w)(y-w) = 1
    #
    # TODO: complete this part and replace the return values
    '''
      [[-2a,-b] * [z =  [d
      [-b,-2c]]   w]   e]
    '''
    a = x[0]
    b = x[1]
    c = x[2]
    d = x[3]
    e = x[4]

    A = [ [-2*a,-b],
         [-b,-2*c] ]
    B = [[d],
        [e]]
    X = np.linalg.solve(A,B)

    # z, w
    z, w = X[0][0], X[1][0]

    C = [ [ z*z + 1/a, z*w,   w*w ],
         [   z*z , z*w+1/b,  w*w ],
         [ z*z ,   z*w,    w*w+1/c] ]

    D = [ [1],
         [1],
         [1] ]
    
    Y = np.linalg.solve(C,D)

    out_a, out_b, out_c = Y[0][0], Y[1][0], Y[2][0]

    #return np.array([0.00141895161, -0.00106665618, 0.00127449289, 46.2251570, 59.9276681])
    return np.array([out_a, out_b, out_c, z, w])

# this is for algorithm 1
def rotation(xp):
    # Compute the rotation for general_to_standard
    # The input model is
    #        xp[0]xx+xp[1]xy+xp[2]yy = 1
    #and xp[3]=z, xp[4]=w
    # find the rotation matrix that make it 
    #       xx/alpha^{2}  + yy/beta^{2} = 1
    #
    # returns 
    # U : rotation matrix
    # P : [alpha, beta], where alpha and beta are the parameters 
    #     for the standard model
    # 
    # TODO: conplete this function and replace the return values


    '''
    U = np.array([[ 0.75306248,  -0.65794901],
                 [0.65794901,  0.75306248]])
    alpha = 35.16844663129803
    beta  = 23.03316576651734
    return U, alpha, beta
    '''
    #so we know that xp[3]=z, xp[4]=w
    a = xp[0]
    b = xp[1]/2
    c = xp[2]
    
    A = np.array([ [a, b],
         [b, c]])

    w, v = np.linalg.eig(A)
    
    Q = np.array(  [[v[0][0], v[0][1]], 
                [v[1][0], v[1][1]]] )
    
  
    W= np.array( [ [w[0],0],
        [0,w[1]] ] )
    '''
    print('this is W----')
    print(W)
    print('Thisi is v--------')
    print(v)
    print('Thisi is A--------')
    print(A)
    print('This is v.T.dot(W.dot(v))')
    print(v.T.dot(W.dot(v)))
    print('This is v.dot(W.dot(v.T))')
    print(v.dot(W.dot(v.T)))

    '''
    
    print('THIS is Q-----------')
    print(Q)
    
  

    return Q.T, np.sqrt(1/w[0]), np.sqrt(1/w[1])
    
def bigToSmall(a, b, U) :
  
    ret = U
    rotation = np.array([[0, -1], [1, 0]])

    if a > b :
        ret = U
    else :
        ret = U.dot(rotation)
    
    
    return max(a, b), min(a, b), ret
  

'''
def bigToSmall(a, b, U) :
    ret = U
    if a > b :
        ret = U.T
    else :
        ret = U
    return max(a, b), min(a, b), ret
'''

# this is for algorithm 1
def general_to_standard(x):
    # general form is 
    #     x[0] xx + x[1] xy + x[2] yy + x[3]x + x[4] y = 1
    # standard form 
    #     xx/alpha^{2}  + yy/beta^{2} = 1
    # 
    # input x is a list containing 5 elements
    # returns
    #     center: center of the translation
    #     U     : rotation matrix
    #     alpha, beta: coefficients for the standard form
    
    xp = translation(x)
    U, alpha, beta = rotation(xp)
    center = xp[3:5]
    return center, U, alpha, beta



# this is for algorithm2
def PCA(points):
    # Input are data in 2D
    # return the PCA for the given data
    #     means: center of the data
    #         U: rotation matrix for data point
    #        YR: the points after translation and rotation
    #   
    n = len(points)
    X = np.zeros((n,2))
    for i in range(n):
        X[i,:] = points[i]

    # do the translation
    means = np.mean(X, axis= 0)
    Y = np.zeros((n,2))
    Y[:,0] = [x - means[0] for x in X[:,0]]
    Y[:,1] = [x - means[1] for x in X[:,1]]

    # do the rotation
    # compute the covariance matrix Sigma
    #
    # TODO: find the rotation matrix U and replace it with the current values
    #
    s00, s01, s10, s11 = 0,0,0,0
    for i in range(n):
      s00 += Y[i][0]**2
      s10 += Y[i][0]*Y[i][1]
      s01 += Y[i][0]*Y[i][1]
      s11 += Y[i][1]**2
    s00 = s00 / n
    s10 = s10 / n
    s01 = s01 / n 
    s11 = s11 / n

    S = [[s00,s01],
         [s10,s11] ]

    eig_val, eig_vec = np.linalg.eig(S)

    V = np.array([ [eig_vec[0][0],eig_vec[0][1]],
         [eig_vec[1][0],eig_vec[1][1]]
         ])
    U = V.T
    W = (U).dot(Y.T)
    #W = U*Y.T

    '''
    U = np.array([[-0.73960154, -0.67304499], [ 0.67304499, -0.73960154]])
    YR = np.dot(U, Y.T)
    '''
    print('This is U---')
    print(U)
    
    
    return means, U, W

# this is for algorithm 2
def fit_ellipse_standard(X):
    # X: the points 
    # output: alpha, beta are the model of the standard form
    #       xx/alpha^2 + yy/alpha^2 = 1
    # 
    # Use least square method to fit the parameter alpha and beta.
    # 
    m, n = X.shape
    A = np.zeros((n, 2))
    b = np.ones((n))
    for i in range(n):
        A[i, :] = [X[0,i]*X[0,i], X[1,i]*X[1,i]]
    
    coef = np.linalg.lstsq(A, b, rcond=None)[0]
    alpha = math.sqrt(1/coef[0])
    beta  = math.sqrt(1/coef[1])
    return alpha, beta

# this is for algorithm 2
def standard_to_general(means, U, alpha, beta):
    # convert 
    #         xx/alpha^2 + yy/beta^2 = 1
    # to      a xx + bxy + cyy + dx + ey = 1
    # using rotation matrix U and translation means
    # return:
    #     coef = [a, b, c, d, e]
    # 
    # TODO: complete this code and replace the return values
    alpha, beta, U = bigToSmall(alpha, beta, U)
    
    #=========================
    
    x_bar = means[0]
    y_bar = means[1]
    alpha_sq_ = (1./alpha)**2
    beta_sq_  = (1./beta)**2
    u11 = U[0][0]
    u12 = U[0][1]
    u21 = U[1][0]
    u22 = U[1][1]
    I1  = u11*x_bar + u12*y_bar
    I2  = u21*x_bar + u22*y_bar

	  # to      a xx + bxy + cyy + dx + ey = 1
    #     coef = [a, b, c, d, e]
    ## 我算出來的是像
    ## a xx + bxy + cyy + dx + ey + constant = 1
    ## 要換成
    ## a xx + bxy + cyy + dx + ey = 1 - constant
    a = alpha_sq_*(u11**2) + beta_sq_*(u21**2)
    b = 2*alpha_sq_*u11*u12 + 2*beta_sq_*u21*u22
    c = alpha_sq_*(u12**2) + beta_sq_*(u22**2)
    d = -2*alpha_sq_*u11*I1 - 2*beta_sq_*u21*I2
    e = -2*alpha_sq_*u12*I1 - 2*beta_sq_*u22*I2
    constant = alpha_sq_*(I1**2) + beta_sq_*(I2**2)

    return [a/(1-constant), b/(1-constant), c/(1-constant), d/(1-constant), e/(1-constant)]
    '''
    A = np.array([[alpha**(-2),0],
          [0,beta**(-2)]])
    Z = (U.T).dot(A.dot(U))
    a11=Z[0][0]
    a21=Z[1][0]
    a12=Z[0][1]
    a22=Z[1][1]
    
    a = a11
    b = a12+a21
    c = a21
    d = -2*a11*means[0]-2*a12*means[1]
    e = -2*a21*means[0]-2*a22*means[1]
    constant = a11*means[0]*means[0]+a12*means[1]*means[0]+a21*means[0]*means[1]+a22*means[1]*means[1]
    return [a/(1-constant), b/(1-constant), c/(1-constant), d/(1-constant), e/(1-constant)]'''
    
    #return np.array([-0.0003901231267804706, 0.00038080859394188987, -0.0004260863980737427, 0.01480319696571577, 0.03235806929940388])

# this is for both algorithms
def ellipse_info(center, U, alpha, beta):
    # returns 2x6 matrix C
    # 1. C[:,0:2]: the coordinates of two focal point, 
    # 2. C[:,2:4]: the coordinates of two end points of major axis
    # 3. C[:,4:6]: the coordinates of two end points of minor axis

    C = np.zeros((2,6))
    # for some reason, the x and y in center should be exchanged
    center = np.array([center[1], center[0]])
    alpha, beta, U = bigToSmall(alpha, beta, U)
    gamma = math.sqrt(alpha*alpha-beta*beta)
    C[:, 0] = center+gamma*U[:,1]
    C[:, 1] = center-gamma*U[:,1]
    C[:, 2] = center+alpha*U[:,1]
    C[:, 3] = center-alpha*U[:,1]
    C[:, 4] = center+beta *U[:,0]
    C[:, 5] = center-beta *U[:,0]
    return C


# this is for both algorithms
def draw_ellipse(x, center, U, alpha, beta):
    # plot the drawing and the fitted circle
    # the ellipse must be in the form
    #      x[0]xx + x[1]xy + x[2]yy + x[3]x + x[4]y = 1
    x_axis = np.linspace(0, 100, 500)
    y_axis = np.linspace(0, 100, 500)

    a, b = np.meshgrid(x_axis, y_axis)

    C = x[0]*a*a + x[1]*a*b + x[2]*b*b + x[3]*a + x[4]*b - 1

    print("=============================")
    print(center, alpha, beta)
    p = ellipse_info(center, U, alpha, beta)

    print('Focal points: (', p[0,0],',', p[1,0],'),(',p[0,1],',', p[1,1],')')
    print('Major axis: (', U[0,0],',',U[1,0], ')')
    print('Minor axis: (', U[0,1],',',U[1,1], ')')

    # start the plotting
    figure, axes = plt.subplots(1)
    plt.imshow(im1) 
    axes.contour(b, a, C, [0])
    axes.set_aspect(1)

    # plot focal points
    plt.plot(p[0,0], p[1,0], 'bo', p[0,1], p[1,1], 'bo')
    # plot major-axis
    plt.plot([p[0,2], p[0,3]], [p[1,2], p[1,3]], 'r-')
    # plot minor-axis
    plt.plot([p[0,4], p[0,5]], [p[1,4], p[1,5]], 'g-')

    plt.show()
    # If you want to save the result comparition image, uncomment this line
    # plt.savefig(file)

def algorithm1(points):
    # solve the least square problem
    x = fit_ellipse_general(points)

    # do the rotation
    center, U, alpha, beta = general_to_standard(x)

    # draw ellipse
    print('Algorithm 1')
    draw_ellipse(x, center, U, alpha, beta)
    
def algorithm2(points):
    # use PCA to find the center (means), the rotation matrix U, 
    # and the points after translation and rotation Y
    center, U, Y = PCA(points)
    
    # use least square to find the parameters of the standard form
    alpha, beta = fit_ellipse_standard(Y)
    
    # find the general form for drawing
    # x containts the coefficients of the general form
    x = standard_to_general(center, U, alpha, beta)
    
    # draw ellipse
    print('Algorithm 2')
    draw_ellipse(x, center, U, alpha, beta)

def draw_template(x, center, U, alpha, beta):
    x_axis = np.linspace(0, 100, 500)
    y_axis = np.linspace(0, 100, 500)

    a, b = np.meshgrid(x_axis, y_axis)

    C = x[0]*a*a + x[1]*a*b + x[2]*b*b + x[3]*a + x[4]*b - 1

    p = ellipse_info(center, U, alpha, beta)

    return a, b, C, p


def compare(points) :
    # Algorithm 1
    # solve the least square problem
    x1 = fit_ellipse_general(points)

    # do the rotation
    center1, U1, alpha1, beta1 = general_to_standard(x1)

    a1, b1, C1, p1 = draw_template(x1, center1, U1, alpha1, beta1)

    ## Calculate loss for Algorithm 1
    loss1 = 0
    a_ = x1[0]
    b_ = x1[1]
    c_ = x1[2]
    d_ = x1[3]
    e_ = x1[4]

    for i in range(len(points)):
        x_1 = points[i][0]
        x_2 = points[i][1]
        loss1 = loss1 + ( a_*(x_1)**2 + b_*x_1*x_2 + c_*(x_2)**2 + d_*x_1 + e_*x_2 - 1)**2
    print("Loss for Algorithm 1: ", loss1/len(points))

    # Algorithm 2
    center2, U2, Y2 = PCA(points)
    
    # use least square to find the parameters of the standard form
    alpha2, beta2 = fit_ellipse_standard(Y2)
    
    # find the general form for drawing
    # x containts the coefficients of the general form
    x2 = standard_to_general(center2, U2, alpha2, beta2)
    a2, b2, C2, p2 = draw_template(x2, center1, U1, alpha1, beta1)

    ## Calculate the error for Algorithm 2
    ## x2 is [a, b, c, d, e,]
    loss2 = 0
    a_ = x2[0]
    b_ = x2[1]
    c_ = x2[2]
    d_ = x2[3]
    e_ = x2[4]

    for i in range(len(points)):
        x_1 = points[i][0]
        x_2 = points[i][1]
        loss2 = loss2 + ( a_*(x_1)**2 + b_*x_1*x_2 + c_*(x_2)**2 + d_*x_1 + e_*x_2 - 1)**2
    print("Loss for Algorithm 2: ", loss2/len(points))

    figure, axes = plt.subplots(1)
    plt.imshow(im1) 
    cs = axes.contour(b1, a1, C1, [0], colors='red')
    cs.collections[0].set_label('Algorithm 1')
    axes.set_aspect(1)

    cs = axes.contour(b2, a2, C2, [0], colors='blue')
    cs.collections[0].set_label('Algorithm 2')
    axes.set_aspect(1)
    plt.legend(loc='upper left')
    plt.show()

    # If you want to save the result comparition image, uncomment this line
    # plt.savefig(file)

# Mount your google drive to save your gif result.
from google.colab import drive
drive.mount('/content/drive')

#----------------main------------------
# read image and get circle points
# a 100x100 image 
print('FOR bean.png')
im1 = img.imread('/content/drive/My Drive/bean.png')
[h, w, c] = np.array(im1).shape
points = [];
for i in range(h):
    for j in range(w):
        if (all(im1[i,j,:])==0):
            points.append([i, j])

algorithm1(points)
algorithm2(points)
compare(points)


#------------------------------------------------
print('FOR eclipse-1,png')
im1 = img.imread('/content/drive/My Drive/eclipse-1.png')
[h, w, c] = np.array(im1).shape
points = [];
for i in range(h):
    for j in range(w):
        if (all(im1[i,j,:])==0):
            points.append([i, j])

algorithm1(points)
algorithm2(points)
compare(points)
#-------------------------------------------------
print('FOR eclipse-2,png')
im1 = img.imread('/content/drive/My Drive/eclipse-2.png')
[h, w, c] = np.array(im1).shape
points = [];
for i in range(h):
    for j in range(w):
        if (all(im1[i,j,:])==0):
            points.append([i, j])

algorithm1(points)
algorithm2(points)
compare(points)
#--------------------------------------------------------------
print('FOR eclipse-3,png')
im1 = img.imread('/content/drive/My Drive/eclipse-3.png')
[h, w, c] = np.array(im1).shape
points = [];
for i in range(h):
    for j in range(w):
        if (all(im1[i,j,:])==0):
            points.append([i, j])

algorithm1(points)
algorithm2(points)
compare(points)

from google.colab import drive
drive.mount('/content/drive')

"""# 新增區段"""