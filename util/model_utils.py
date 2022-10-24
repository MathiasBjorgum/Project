from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report



def train_test_model(model, X_train, y_train, X_test, y_test):
    '''Trains and tests a given model, printing out classification report and accuracy. The function also returns the model.'''
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print(accuracy_score(y_test, y_pred))

    print(classification_report(y_test, y_pred))

    return model