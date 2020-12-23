import pandas as pd 
import numpy as np

class LogisticRegressionModel:
    def __init__(self):

        ## Black is 0 , White is 1
        ## Will reshape to 5x5 while processing

        self.X_train = np.array([[0,0,1,1,1,1,0,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,0,0],
        [0,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,0],
        [1,0,1,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,0,1,1,1,0,1],
        [0,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,0,1,0,1,0,1],
        ])
        
        self.X_test = np.array([[1,0,0,1,1,0,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0]])

        self.findX = np.array([[0,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,0,0,0,1,1,1,0,1],
        [0,0,0,1,1,0,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,1,0,1,1],
        [1,1,1,1,0,1,1,1,1,0,1,1,1,0,0,1,1,1,1,0,1,0,1,0,0],
        [1,0,0,1,1,0,0,1,1,1,1,0,0,1,1,1,0,1,1,0,1,1,1,1,1],
        [0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0]])

        ## Logistic Regression Output
        self.y_train = [0,1,0,1,0,1,0,1]
        self.y_test = [0,1]
        for x in self.X_train:
            x = x.reshape(5,5)
            # print(x)
    
        self.weights1 = np.random.rand(1,5)
        self.weights2 = np.random.rand(1,5)
        self.bias1 = np.zeros((1,5))
        self.bias2 = np.zeros((1,1))
        


    def sigmoid(self,val):
        return 1/(1+np.exp(-val))
    
    def sigmoidDerivative(self,val):
        return self.sigmoid(val)*(1-self.sigmoid(val))

    def calc_loss(self,lossVal,actualVal):
        ## a regularization term could also be added to this loss value : lambda * (w**2)/2
        return (-actualVal*np.log(lossVal) - (1 - actualVal)*np.log(1 - lossVal)).mean() 

    def fit(self):
        loss = 0
        for j in range(50):
            for i in range(self.X_train.shape[0]):
                ## Forward Prop
                h1 = np.dot(self.weights1,self.X_train[i].reshape(5,5)) + self.bias1
                z1 = self.sigmoid(h1)
                h2 = np.dot(self.weights2,z1.T) + self.bias2
                z2 = self.sigmoid(h2)
                # print("bias: ",bias1 )
                loss=self.calc_loss(z2,self.y_train[i])
                
                
                ## Backprop
                dz2 = z2 - self.y_train[i]
                ## a regularization factor of lambda*w would reduce overfitting
                dw2 = np.dot(dz2,h1)
                db2 = np.sum(dz2,axis =1,keepdims=True)
                self.weights2 -= dw2
                self.bias2 -=db2
                dz1 = np.dot(dz2,self.weights2)*self.sigmoidDerivative(h1)
                dw1 = np.dot(dz1,self.X_train[i].reshape(5,5))
                db1 = np.sum(dz1,axis =1,keepdims=True)
                self.weights1 -= dw1
                self.bias1 -=db1
                
        
        for k in range(self.X_test.shape[0]):
            h1 = np.dot(self.weights1,self.X_test[k].reshape(5,5)) + self.bias1
            z1 = self.sigmoid(h1)
            h2 = np.dot(self.weights2,h1.T) + self.bias2
            z2 = 0 if(self.sigmoid(h2)<0.5) else 1
            

    def predict(self):
        for x in self.findX:
            # print(x)
            h1 = np.dot(self.weights1,x.reshape(5,5)) + self.bias1
            z1 = self.sigmoid(h1)
            h2 = np.dot(self.weights2,h1.T) + self.bias2
            z2 = 'A' if(self.sigmoid(h2)<0.5) else 'B'
            print(z2)    

        
l = LogisticRegressionModel()
l.fit()
l.predict()
