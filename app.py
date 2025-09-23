from flask import Flask, request, render_template
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            # Collect form data into CustomData object
            data = CustomData(
                Age=int(request.form.get('Age')),
                DistanceFromHome=int(request.form.get('DistanceFromHome')),
                NumCompaniesWorked=int(request.form.get('NumCompaniesWorked')),
                PercentSalaryHike=int(request.form.get('PercentSalaryHike')),
                StockOptionLevel=int(request.form.get('StockOptionLevel')),
                TrainingTimesLastYear=int(request.form.get('TrainingTimesLastYear')),
                YearsAtCompany=int(request.form.get('YearsAtCompany')),
                YearsSinceLastPromotion=int(request.form.get('YearsSinceLastPromotion')),
                YearsWithCurrManager=int(request.form.get('YearsWithCurrManager')),
                MonthlyIncome=int(request.form.get('MonthlyIncome')),
                TotalWorkingYears=int(request.form.get('TotalWorkingYears')),
                YearsInCurrentRole=int(request.form.get('YearsInCurrentRole')),

                # Label encoded
                Education=int(request.form.get('Education')),
                EnvironmentSatisfaction=int(request.form.get('EnvironmentSatisfaction')),
                JobInvolvement=int(request.form.get('JobInvolvement')),
                JobSatisfaction=int(request.form.get('JobSatisfaction')),
                PerformanceRating=int(request.form.get('PerformanceRating')),
                RelationshipSatisfaction=int(request.form.get('RelationshipSatisfaction')),
                WorkLifeBalance=int(request.form.get('WorkLifeBalance')),

                # One-hot encoded
                BusinessTravel=request.form.get('BusinessTravel'),
                Department=request.form.get('Department'),
                EducationField=request.form.get('EducationField'),
                Gender=request.form.get('Gender'),
                JobRole=request.form.get('JobRole'),
                MaritalStatus=request.form.get('MaritalStatus'),
                OverTime=request.form.get('OverTime')
            )

            # Convert to DataFrame
            pred_df = data.get_data_as_dataframe()

            # Prediction pipeline
            predict_pipeline = PredictPipeline()
            results = predict_pipeline.predict(pred_df)

            prediction = "Yes (Attrition Likely)" if results[0] == 1 else "No (Attrition Unlikely)"

            return render_template('home.html', results=prediction)

        except Exception as e:
            return render_template('home.html', results=f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
