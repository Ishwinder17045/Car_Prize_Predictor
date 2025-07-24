from flask import Flask,render_template,request

import pandas as pd
import numpy as np
import pickle

app=Flask(__name__)


model=pickle.load(open('LinearRegressionModel.pkl','rb'))
car=pd.read_csv('Cleaned_data.csv')

@app.route('/')
def index():
    companies=sorted(car['company'].unique())
    car_models=sorted(car['name'].unique())
    year=sorted(car['year'].unique(), reverse=True)
    fuel_type=car['fuel_type'].unique()
    companies.insert(0,'Select Company')
    year.insert(0,'Select Year')
    return render_template('index.html', companies=companies, car_models=car_models, years=year, fuel_types=fuel_type)


@app.route('/predict', methods=['POST'])

def predict():
    try:
        company = request.form.get('company')
        car_model = request.form.get('car_models')
        year = request.form.get('year')
        fuel_type = request.form.get('fuel_type')
        kms_driven = request.form.get('kilo_driven')

        # Debug print
        print("INPUTS:", company, car_model, year, fuel_type, kms_driven)

        # Validation
        if not company or company == "Select Company" or \
           not year or year == "Select Year" or \
           not fuel_type or not kms_driven or not car_model:
            return "Error: Please fill all fields correctly"

        # Convert numeric fields
        year = int(year)
        kms_driven = int(kms_driven)

        # **Add this check here**
        if kms_driven > 350000:
            return "Error: Enter realistic kilometres (less than 350000)"
        

        # Predict price
        prediction = model.predict(pd.DataFrame(
            columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
            data=[[car_model, company, year, kms_driven, fuel_type]]
        ))

        # Round and avoid negative prices
        predicted_price = np.round(prediction[0], 2)
        predicted_price = max(0, predicted_price)

        return str(predicted_price)

    except Exception as e:
        import traceback
        print("ERROR TRACEBACK:")
        traceback.print_exc()
        return f"Error: {e}"



if __name__=="__main__":
    app.run(debug=True)


