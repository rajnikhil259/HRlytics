import os
import sys
import urllib.parse
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from src.logger import logging
from src.exception import CustomException

load_dotenv()

application = Flask(__name__)
app = application

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
password = urllib.parse.quote_plus(DB_PASSWORD)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    distance_from_home = db.Column(db.Integer, nullable=True)
    num_companies_worked = db.Column(db.Integer, nullable=True)
    percent_salary_hike = db.Column(db.Integer, nullable=True)
    stock_option_level = db.Column(db.Integer, nullable=True)
    training_times_last_year = db.Column(db.Integer, nullable=True)
    years_at_company = db.Column(db.Integer, nullable=True)
    years_since_last_promotion = db.Column(db.Integer, nullable=True)
    years_with_curr_manager = db.Column(db.Integer, nullable=True)
    monthly_income = db.Column(db.Integer, nullable=True)
    total_working_years = db.Column(db.Integer, nullable=True)
    years_in_current_role = db.Column(db.Integer, nullable=True)
    education = db.Column(db.Integer, nullable=True)
    environment_satisfaction = db.Column(db.Integer, nullable=True)
    job_involvement = db.Column(db.Integer, nullable=True)
    job_satisfaction = db.Column(db.Integer, nullable=True)
    performance_rating = db.Column(db.Integer, nullable=True)
    relationship_satisfaction = db.Column(db.Integer, nullable=True)
    work_life_balance = db.Column(db.Integer, nullable=True)
    business_travel = db.Column(db.String(50), nullable=True)
    department = db.Column(db.String(50), nullable=True)
    education_field = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    job_role = db.Column(db.String(50), nullable=True)
    marital_status = db.Column(db.String(20), nullable=True)
    overtime = db.Column(db.String(10), nullable=True)

@app.route('/')
def dashboard():
    try:
        employees = Employee.query.all()
        logging.info("Fetched all employees for dashboard.")
        return render_template('dashboard.html', employees=employees)
    except Exception as e:
        logging.error(f"Error fetching employees: {str(e)}")
        raise CustomException(e, sys)

@app.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        try:
            emp = Employee(
                name=request.form['name'],
                age=int(request.form['age']),
                distance_from_home=int(request.form.get('DistanceFromHome', 0)),
                num_companies_worked=int(request.form.get('NumCompaniesWorked', 0)),
                percent_salary_hike=int(request.form.get('PercentSalaryHike', 0)),
                stock_option_level=int(request.form.get('StockOptionLevel', 0)),
                training_times_last_year=int(request.form.get('TrainingTimesLastYear', 0)),
                years_at_company=int(request.form.get('YearsAtCompany', 0)),
                years_since_last_promotion=int(request.form.get('YearsSinceLastPromotion', 0)),
                years_with_curr_manager=int(request.form.get('YearsWithCurrManager', 0)),
                monthly_income=int(request.form.get('MonthlyIncome', 0)),
                total_working_years=int(request.form.get('TotalWorkingYears', 0)),
                years_in_current_role=int(request.form.get('YearsInCurrentRole', 0)),
                education=int(request.form.get('Education', 0)),
                environment_satisfaction=int(request.form.get('EnvironmentSatisfaction', 0)),
                job_involvement=int(request.form.get('JobInvolvement', 0)),
                job_satisfaction=int(request.form.get('JobSatisfaction', 0)),
                performance_rating=int(request.form.get('PerformanceRating', 0)),
                relationship_satisfaction=int(request.form.get('RelationshipSatisfaction', 0)),
                work_life_balance=int(request.form.get('WorkLifeBalance', 0)),
                business_travel=request.form.get('BusinessTravel'),
                department=request.form.get('Department'),
                education_field=request.form.get('EducationField'),
                gender=request.form.get('Gender'),
                job_role=request.form.get('JobRole'),
                marital_status=request.form.get('MaritalStatus'),
                overtime=request.form.get('OverTime')
            )
            db.session.add(emp)
            db.session.commit()
            logging.info(f"Added new employee: {emp.name}")
            return redirect(url_for('dashboard'))
        except Exception as e:
            logging.error(f"Error adding employee: {str(e)}")
            raise CustomException(e, sys)
    return render_template('add_employee.html')

@app.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    emp = Employee.query.get_or_404(id)
    if request.method == 'POST':
        try:
            emp.name = request.form['name']
            emp.age = int(request.form['age'])
            emp.distance_from_home = int(request.form.get('DistanceFromHome', emp.distance_from_home))
            emp.num_companies_worked = int(request.form.get('NumCompaniesWorked', emp.num_companies_worked))
            emp.percent_salary_hike = int(request.form.get('PercentSalaryHike', emp.percent_salary_hike))
            emp.stock_option_level = int(request.form.get('StockOptionLevel', emp.stock_option_level))
            emp.training_times_last_year = int(request.form.get('TrainingTimesLastYear', emp.training_times_last_year))
            emp.years_at_company = int(request.form.get('YearsAtCompany', emp.years_at_company))
            emp.years_since_last_promotion = int(request.form.get('YearsSinceLastPromotion', emp.years_since_last_promotion))
            emp.years_with_curr_manager = int(request.form.get('YearsWithCurrManager', emp.years_with_curr_manager))
            emp.monthly_income = int(request.form.get('MonthlyIncome', emp.monthly_income))
            emp.total_working_years = int(request.form.get('TotalWorkingYears', emp.total_working_years))
            emp.years_in_current_role = int(request.form.get('YearsInCurrentRole', emp.years_in_current_role))
            emp.education = int(request.form.get('Education', emp.education))
            emp.environment_satisfaction = int(request.form.get('EnvironmentSatisfaction', emp.environment_satisfaction))
            emp.job_involvement = int(request.form.get('JobInvolvement', emp.job_involvement))
            emp.job_satisfaction = int(request.form.get('JobSatisfaction', emp.job_satisfaction))
            emp.performance_rating = int(request.form.get('PerformanceRating', emp.performance_rating))
            emp.relationship_satisfaction = int(request.form.get('RelationshipSatisfaction', emp.relationship_satisfaction))
            emp.work_life_balance = int(request.form.get('WorkLifeBalance', emp.work_life_balance))
            emp.business_travel = request.form.get('BusinessTravel', emp.business_travel)
            emp.department = request.form.get('Department', emp.department)
            emp.education_field = request.form.get('EducationField', emp.education_field)
            emp.gender = request.form.get('Gender', emp.gender)
            emp.job_role = request.form.get('JobRole', emp.job_role)
            emp.marital_status = request.form.get('MaritalStatus', emp.marital_status)
            emp.overtime = request.form.get('OverTime', emp.overtime)
            db.session.commit()
            logging.info(f"Edited employee: {emp.name}")
            return redirect(url_for('dashboard'))
        except Exception as e:
            logging.error(f"Error editing employee: {str(e)}")
            raise CustomException(e, sys)
    return render_template('edit_employee.html', emp=emp)

@app.route('/employee/predict/<int:id>', methods=['GET'])
def predict_employee(id):
    emp = Employee.query.get_or_404(id)
    try:
        data = CustomData(
            Age=emp.age,
            DistanceFromHome=emp.distance_from_home,
            NumCompaniesWorked=emp.num_companies_worked,
            PercentSalaryHike=emp.percent_salary_hike,
            StockOptionLevel=emp.stock_option_level,
            TrainingTimesLastYear=emp.training_times_last_year,
            YearsAtCompany=emp.years_at_company,
            YearsSinceLastPromotion=emp.years_since_last_promotion,
            YearsWithCurrManager=emp.years_with_curr_manager,
            MonthlyIncome=emp.monthly_income,
            TotalWorkingYears=emp.total_working_years,
            YearsInCurrentRole=emp.years_in_current_role,
            Education=emp.education,
            EnvironmentSatisfaction=emp.environment_satisfaction,
            JobInvolvement=emp.job_involvement,
            JobSatisfaction=emp.job_satisfaction,
            PerformanceRating=emp.performance_rating,
            RelationshipSatisfaction=emp.relationship_satisfaction,
            WorkLifeBalance=emp.work_life_balance,
            BusinessTravel=emp.business_travel,
            Department=emp.department,
            EducationField=emp.education_field,
            Gender=emp.gender,
            JobRole=emp.job_role,
            MaritalStatus=emp.marital_status,
            OverTime=emp.overtime
        )
        pred_df = data.get_data_as_dataframe()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        prediction = "Yes (Attrition Likely)" if results[0] == 1 else "No (Attrition Unlikely)"
        probability = predict_pipeline.predict_proba(pred_df)[0][1] * 100
        logging.info(f"Predicted attrition for employee {emp.name}: {prediction} ({probability:.2f}%)")
        return render_template('predict.html', emp=emp, results=prediction, prob=round(probability, 2))
    except Exception as e:
        logging.error(f"Error predicting attrition for employee {emp.name}: {str(e)}")
        raise CustomException(e, sys)

@app.route('/employee/delete/<int:id>')
def delete_employee(id):
    try:
        emp = Employee.query.get_or_404(id)
        db.session.delete(emp)
        db.session.commit()
        logging.info(f"Deleted employee: {emp.name}")
        return redirect(url_for('dashboard'))
    except Exception as e:
        logging.error(f"Error deleting employee: {str(e)}")
        raise CustomException(e, sys)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        logging.info("Database tables created and app started.")
    app.run(host="0.0.0.0", debug=True)