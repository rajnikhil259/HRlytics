# 🧑‍💼 HR Attrition Prediction System

An end-to-end Employee Attrition Prediction system built with **Flask**, **PostgreSQL**, and **Machine Learning (scikit-learn)**.

This application provides HR professionals with a dashboard to:
- ✅ Add, edit, and remove employees.
- ✅ View all employees in a central dashboard.
- ✅ Predict attrition probability for individual employees using an ML model.

---

## 📂 Project Structure

├── artifacts/ │ ├── data.csv │ ├── model.pkl │ ├── preprocessor.pkl │ ├── train.csv │ └── test.csv │ ├── logs/ │ ├── notebook/ │ ├── data/ │ │ ├── clean_hr_data.csv │ │ └── HRlytic-Attrition.csv │ ├── eda.ipynb │ └── model.ipynb │ ├── src/ │ ├── components/ │ │ ├── data_ingestion.py │ │ ├── data_transformation.py │ │ └── model_trainer.py │ ├── pipeline/ │ │ ├── predict_pipeline.py │ │ └── init.py │ ├── init.py │ ├── exception.py │ ├── logger.py │ └── utils.py │ ├── templates/ │ ├── index.html │ ├── dashboard.html │ ├── add_employee.html │ ├── edit_employee.html │ └── predict.html │ ├── venv/ │ ├── .env ├── .gitignore ├── app.py ├── requirements.txt └── setup.py



---

## ⚙️ Features

### 1. Employee Management
- Add employee details
- Edit existing employee data
- Delete employees
- View all employees in a dashboard

### 2. Attrition Prediction
- Predicts whether an employee is likely to leave (Yes/No)
- Displays attrition probability for better decision-making
- Uses both numerical and categorical features

### 3. Database Integration
- Employee data stored in **PostgreSQL**
- ORM powered by **SQLAlchemy**

---

## 📊 Features Used in Prediction

**Numerical Features:**
- Age, DistanceFromHome, NumCompaniesWorked, PercentSalaryHike, StockOptionLevel, TrainingTimesLastYear, YearsAtCompany, YearsSinceLastPromotion, YearsWithCurrManager, MonthlyIncome, TotalWorkingYears, YearsInCurrentRole

**Label Encoded Features:**
- Education, EnvironmentSatisfaction, JobInvolvement, JobSatisfaction, PerformanceRating, RelationshipSatisfaction, WorkLifeBalance

**One-Hot Encoded Features:**
- BusinessTravel, Department, EducationField, Gender, JobRole, MaritalStatus, OverTime

---

## 🚀 Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/hr-attrition-prediction.git
cd hr-attrition-prediction
```
### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Setup PostgreSQL database

Create a database named hr_analytics
Update app.config['SQLALCHEMY_DATABASE_URI'] in app.py with your credentials

## ▶️ Run the App

```bash
python app.py
```
Open your browser and navigate to: http://localhost:5000

## 🛠️ Tech Stack
- Backend: Flask, SQLAlchemy
- Database: PostgreSQL
- Machine Learning: Scikit-learn, Pandas, Numpy
- Frontend: HTML5, Bootstrap (inside templates/)

## 📌 Future Improvements
- Add authentication for HR users
- Support bulk CSV upload of employees
- Add visualizations for attrition trends

## 👨‍💻 Author
- Developed by [NIKHIL RAJ] 
- 🎯 IIIT Manipur | B.Tech CSE


