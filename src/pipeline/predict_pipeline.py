import os
import sys
import pandas as pd
import pickle

class PredictPipeline:
    def __init__(self):
        model_path = os.path.join("artifacts", "model.pkl")
        preprocessor_path = os.path.join("artifacts", "proprocessor.pkl")

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

        with open(preprocessor_path, "rb") as f:
            self.preprocessor = pickle.load(f)

    def predict(self, features: pd.DataFrame):
        data_scaled = self.preprocessor.transform(features)
        preds = self.model.predict(data_scaled)
        return preds
    
    def predict_proba(self, features: pd.DataFrame):
        data_scaled = self.preprocessor.transform(features)
        probs = self.model.predict_proba(data_scaled)
        return probs


class CustomData:
    def __init__(self,
                 Age: int,
                 DistanceFromHome: int,
                 NumCompaniesWorked: int,
                 PercentSalaryHike: int,
                 StockOptionLevel: int,
                 TrainingTimesLastYear: int,
                 YearsAtCompany: int,
                 YearsSinceLastPromotion: int,
                 YearsWithCurrManager: int,
                 MonthlyIncome: int,
                 TotalWorkingYears: int,
                 YearsInCurrentRole: int,
                 Education: int,
                 EnvironmentSatisfaction: int,
                 JobInvolvement: int,
                 JobSatisfaction: int,
                 PerformanceRating: int,
                 RelationshipSatisfaction: int,
                 WorkLifeBalance: int,
                 BusinessTravel: str,
                 Department: str,
                 EducationField: str,
                 Gender: str,
                 JobRole: str,
                 MaritalStatus: str,
                 OverTime: str):

        # Numeric
        self.Age = Age
        self.DistanceFromHome = DistanceFromHome
        self.NumCompaniesWorked = NumCompaniesWorked
        self.PercentSalaryHike = PercentSalaryHike
        self.StockOptionLevel = StockOptionLevel
        self.TrainingTimesLastYear = TrainingTimesLastYear
        self.YearsAtCompany = YearsAtCompany
        self.YearsSinceLastPromotion = YearsSinceLastPromotion
        self.YearsWithCurrManager = YearsWithCurrManager
        self.MonthlyIncome = MonthlyIncome
        self.TotalWorkingYears = TotalWorkingYears
        self.YearsInCurrentRole = YearsInCurrentRole

        # Label Encoded
        self.Education = Education
        self.EnvironmentSatisfaction = EnvironmentSatisfaction
        self.JobInvolvement = JobInvolvement
        self.JobSatisfaction = JobSatisfaction
        self.PerformanceRating = PerformanceRating
        self.RelationshipSatisfaction = RelationshipSatisfaction
        self.WorkLifeBalance = WorkLifeBalance

        # One-hot
        self.BusinessTravel = BusinessTravel
        self.Department = Department
        self.EducationField = EducationField
        self.Gender = Gender
        self.JobRole = JobRole
        self.MaritalStatus = MaritalStatus
        self.OverTime = OverTime

    def get_data_as_dataframe(self):
        
            data_dict = {
                # Numeric
                "Age": [self.Age],
                "DistanceFromHome": [self.DistanceFromHome],
                "NumCompaniesWorked": [self.NumCompaniesWorked],
                "PercentSalaryHike": [self.PercentSalaryHike],
                "StockOptionLevel": [self.StockOptionLevel],
                "TrainingTimesLastYear": [self.TrainingTimesLastYear],
                "YearsAtCompany": [self.YearsAtCompany],
                "YearsSinceLastPromotion": [self.YearsSinceLastPromotion],
                "YearsWithCurrManager": [self.YearsWithCurrManager],
                "MonthlyIncome": [self.MonthlyIncome],
                "TotalWorkingYears": [self.TotalWorkingYears],
                "YearsInCurrentRole": [self.YearsInCurrentRole],

                # Label Encoded
                "Education": [self.Education],
                "EnvironmentSatisfaction": [self.EnvironmentSatisfaction],
                "JobInvolvement": [self.JobInvolvement],
                "JobSatisfaction": [self.JobSatisfaction],
                "PerformanceRating": [self.PerformanceRating],
                "RelationshipSatisfaction": [self.RelationshipSatisfaction],
                "WorkLifeBalance": [self.WorkLifeBalance],

                # One-hot
                "BusinessTravel": [self.BusinessTravel],
                "Department": [self.Department],
                "EducationField": [self.EducationField],
                "Gender": [self.Gender],
                "JobRole": [self.JobRole],
                "MaritalStatus": [self.MaritalStatus],
                "OverTime": [self.OverTime],
            }
            return pd.DataFrame(data_dict)
        
