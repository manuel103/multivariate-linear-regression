import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = pd.read_csv('C:/users/Immanuel/downloads/loan_pred.csv')
print(data.shape)
data.head()

#drop all rows with missing values
data.dropna(inplace=True)


#import the library LabelEncoder
from sklearn.preprocessing import LabelEncoder
#Create a list with categorical predictors
cat_var =['Gender','Married','Education','Self_Employed','Loan_Status']
#Initiate LabelEncoder
le = LabelEncoder() 
#A for loop to transform the categorical values to numerical values
for n in cat_var:
    data[n] = le.fit_transform(data[n])

#Checking for the type of the predictors afterwards
data.dtypes

#Getting the variables to an array.
LoanAmount = data['LoanAmount'].values
Credit_History = data['Credit_History'].values
Loan_Status = data['Loan_Status'].values	


# Plotting the scores as scatter plot
fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(LoanAmount, Credit_History, Loan_Status, color='#ef1234')
plt.show()

#Now we generate our parameters(the theta values)
m = len(LoanAmount)
x0 = np.ones(m)
X = np.array([x0, LoanAmount, Credit_History]).T
# Initial Coefficients
B = np.array([0, 0, 0])
Y = np.array(Loan_Status)
alpha = 0.0001

#We’ll define our cost function.
def cost_function(X, Y, B):
    m = len(Y)
    J = np.sum((X.dot(B) - Y) ** 2)/(2 * m)
    return J

inital_cost = cost_function(X, Y, B)
print("Initial Cost")
print(inital_cost)

#Defining the Gradient Descent
def gradient_descent(X, Y, B, alpha, iterations):
    cost_history = [0] * iterations
    m = len(Y)
    
    for iteration in range(iterations):
        # Hypothesis Values
        h = X.dot(B)
        # Difference b/w Hypothesis and Actual Y
        loss = h - Y
        # Gradient Calculation
        gradient = X.T.dot(loss) / m
        # Changing Values of B using Gradient
        B = B - alpha * gradient
        # New Cost Value
        cost = cost_function(X, Y, B)
        cost_history[iteration] = cost
        
    return B, cost_history

# 100 Iterations
newB, cost_history = gradient_descent(X, Y, B, alpha, 100)

# New Values of B
print("New Coefficients")
print(newB)

# Final Cost of new B
print("Final Cost")
print(cost_history[-1])

# Model Evaluation - RMSE
def rmse(Y, Y_pred):
    rmse = np.sqrt(sum((Y - Y_pred) ** 2) / len(Y))
    return rmse

# Model Evaluation - R2 Score
def r2_score(Y, Y_pred):
    mean_y = np.mean(Y)
    ss_tot = sum((Y - mean_y) ** 2)
    ss_res = sum((Y - Y_pred) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    return r2

Y_pred = X.dot(newB)

print("RMSE")
print(rmse(Y, Y_pred))
print("R2 Score")
print(r2_score(Y, Y_pred))



from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# X and Y Values
X = np.array([LoanAmount, Credit_History]).T
Y = np.array(Loan_Status)

# Model Intialization
reg = LinearRegression()
# Data Fitting
reg = reg.fit(X, Y)
# Y Prediction
Y_pred = reg.predict(X)

# Model Evaluation
rmse = np.sqrt(mean_squared_error(Y, Y_pred))
r2 = reg.score(X, Y)

print(rmse)
print(r2)