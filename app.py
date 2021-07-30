
# importing the necessary dependencies
from flask import Flask, render_template, request
from flask_cors import cross_origin
import joblib
import numpy as np
import pandas as pd
from cassandra_send import send_user_info
# importing logging for debug purposes
from setup_logger import setup_logger
log = setup_logger(logger_name = 'log1', log_file='log1.log')
# loading the model
model = joblib.load('census_income_84_auc_scr_full_pipeline2.pkl')

# cassandra code
send_user_info()

app = Flask(__name__) # creating an instance of the Flask class
@app.route('/', methods=['GET']) # the decorator
@cross_origin()
def homePage():
    log.info("-----------------------Home pahe shown------------------------")
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET']) 
@cross_origin()
def index():
    log.info("Prediction page shown")
    if request.method == 'POST':
        log.info("If passed")
        try:
            log.info("enter inside try")
            # getting data from user
            age = int(request.form['age']) # int
            log.info("age")
            workclass = str(request.form['workclass']) # cat
            log.info("workclass")
            occupation = str(request.form['occupation']) # cat
            log.info("occupation")
            sex = str(request.form['sex']) # cat
            log.info("sex")
            hours_per_week = int(request.form['hours_per_week']) # int
            log.info("hourse per week")
            education_label = str(request.form['education_label']) # cat
            log.info("education label")
            # loading the model
            # model = joblib.load('E:\My_Projects\Census Income\census_income_84_auc_scr_full_pipeline2.pkl')
            log.info("model loaded")
            arr = np.array([age, workclass, occupation, sex, hours_per_week, education_label])
            log.info("array created")
            data = pd.DataFrame([arr], columns=['age', 'workclass', 'occupation', 'sex', 
                                   'hours.per.week', 'Education Level'])

            p = model.predict(data) # prforming prediction 
            log.info("prediction  done")
            if p == 1:
                pr = "Your Income is likely Above 50k"
            else:
                pr = "Your Income is likely Below 50k"
            # showing prediction on the result index page
            log.info("pass the prediction if else")
            print(p)
            log.info('Returning the result html page')
            return render_template('results.html', prediction=pr, method=request.method)
        except Exception as e:
            log.info("come to exception")
            print(str(e))
            return "Something Went Wrong You may did not fill some information that is requierd"

    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)

