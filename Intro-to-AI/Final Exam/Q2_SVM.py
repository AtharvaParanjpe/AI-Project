import numpy as np

class SVM:
    
    def __init__(self):
        self.X_train = np.array([[0,0,1,1,1,1,0,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,0,0],
        [0,0,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
        [1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,0,1,0,0],
        [1,0,1,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,1,1,1,1,1,1,0,1,0,1,1,0,1,1,1,1,0,0,1,1,1,0,1],
        [0,0,1,1,1,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,0,1,0,1,0,1],
        [1,0,0,1,1,0,0,1,1,0,1,0,1,1,1,1,1,0,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,0,0]
        ])
        ## For the hyperplane
        self.weights = np.zeros(len(self.X_train[0]))
        self.y_train = [-1,1,-1,1,-1,1,-1,1,-1,1]
        
    def fit(self):
        lr = 0.05
        epoch = 100
        for ep in range(epoch):
            for i in range(len(self.X_train)):
                temp = np.dot(self.X_train[i],self.weights)
                if(self.y_train[i]*temp<1):
                    ## Calculation with regularization parameters uses the function given below
                    self.weights = self.weights + lr *((self.y_train[i]*self.X_train[i]) - 2*self.weights*(1/ep))
                    ##
                else:
                    ## Gives the hyper plane
                    self.weights = self.weights - lr*(2*self.weights*(1/ep)) 
                    

    def predict(self):
        out_class = []
        out_val = []
        test_val = np.array([[0,1,1,1,1,0,1,0,1,0,1,1,1,1,1,1,1,0,0,0,1,1,1,0,1],
        [0,0,0,1,1,0,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,1,0,1,1],
        [1,1,1,1,0,1,1,1,1,0,1,1,1,0,0,1,1,1,1,0,1,0,1,0,0],
        [1,0,0,1,1,0,0,1,1,1,1,0,0,1,1,1,0,1,1,0,1,1,1,1,1],
        [0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0]])
        for x in test_val:
            out_val.append(np.dot(x,self.weights))
            out_class.append('A' if np.dot(x,self.weights)<0 else 'B')
        print(out_class)
        print(out_val)


svm = SVM()
svm.fit()
svm.predict()