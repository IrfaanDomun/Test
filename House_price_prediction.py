__author__ = "Irfaan Domun"
__email__  = "irfaan@hotmail.fr"

import pandas as pd
from sklearn.linear_model import LinearRegression

def getData():
    """
    get data from csv, then set name to each columns
    """
    data = pd.read_csv("C:\\Users\\i\\downloads\\pp-monthly-update-new-version.csv")
    columns_name = [ "Transaction unique identifier","Price"\
                    ,"Date of Transfer","Postcode","Property Type"\
                    ,"Old/New","Duration","PAON","SAON","Street","Locality"\
                    ,"Town/City","District","County","PPD Category Type"\
                    ,"Record Status - monthly file only"]
    for i in xrange(len(columns_name)):
        columns_name[i]=columns_name[i].replace(" ","_")
        columns_name[i]=columns_name[i].replace("/","")
    data.columns = columns_name
    return data

"""    reshaping the data    """
def createQuantitativeData(data):
    """
    Creating dummies to get quantitative data from qualitative ones
    """
    data['IsFreehold'] = data.Duration.map({'L':0, 'F':1})
    data['IsLondon'] = [ 1 if i=='LONDON' else 0 for i in data.TownCity]
    # creating dummy variables using get_dummies, then exclude the first dummy column
    property_type_dummies = pd.get_dummies(data.Property_Type, prefix='Type').iloc[:, 1:]
    data = pd.concat([data, property_type_dummies], axis=1)
    return data

def createSetOfData(data):
    """
    spliting the dataframe into a training set and a testing set
    finding the non 2015 value for training data set
    data: dataframe you are spliting
    modify data to only get useful columns
    return two set of data, one for training, one for testing
    """
    IsTest = [ i[ :4]!='2015' for i in data.Date_of_Transfer]
    #Choosing the useful columns
    feature_cols = ['Price','Type_F','Type_O','Type_S','Type_T','IsLondon','IsFreehold']
    data_temp = data[feature_cols]
    #Creating the training dataframe
    data_train = pd.DataFrame(data_temp[IsTest][feature_cols])
    #Creating the testing dataframe
    inverse_vector = [not i for i in IsTest]
    data_test = pd.DataFrame(data_temp[inverse_vector][feature_cols])
    return data_train, data_test

def getAndFormatData():
    """
    getData and return computable data
    """
    data = getData()
    data = createQuantitativeData(data)
    return createSetOfData(data)

if __name__ == '__main__':
    """    get train and test data    """
    data_train, data_test = getAndFormatData()
    """    linear regression   """
    #training the model
    X = data_train[data_train.columns[1:]]
    y = data_train.Price
    #training the model
    lm = LinearRegression()
    lm.fit(X, y)
    
    # print score, intercept and coefficients
    print "score:",lm.score(X, y)
    print "intercept:",lm.intercept_
    print "coeficient: \n",zip(data_test.columns[1:],lm.coef_)
    
    #test the model
    X_test =data_test[data_test.columns[1:]]
    data_test['predicted_price']= lm.predict(X_test)
    #print the first few elements of the test dataframe with the predicted values
    print "\n samples of the price predicted :\n",data_test.head(),data_test.shape
    #print score of the tested model
    print "\npredicted score",lm.score(X_test,data_test.Price)
