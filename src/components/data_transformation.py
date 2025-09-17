import sys
import os
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
       
        try:
            numeric_features = [
            'Age', 'DistanceFromHome', 'NumCompaniesWorked', 'PercentSalaryHike',
            'StockOptionLevel', 'TrainingTimesLastYear', 'YearsAtCompany',
            'YearsSinceLastPromotion', 'YearsWithCurrManager', 'MonthlyIncome',
            'TotalWorkingYears', 'YearsInCurrentRole'
            ]

            label_encoding_features = [
            'Education', 'EnvironmentSatisfaction', 'JobInvolvement',
            'JobSatisfaction', 'PerformanceRating', 'RelationshipSatisfaction',
            'WorkLifeBalance'
            ]

            onehot_encoding_features = [
            'BusinessTravel', 'Department', 'EducationField', 'Gender',
            'JobRole', 'MaritalStatus', 'OverTime'
            ]  

            num_pipeline=Pipeline(
                steps=[
                ("scaler",StandardScaler())
                ]
            )

            label_pipeline=Pipeline(
                steps=[
                ("label_encoder",OrdinalEncoder())
                ]
            )

            onehot_pipeline=Pipeline(
                steps=[
                ("onehot_encoder",OneHotEncoder()),
                ]
            )

            logging.info(f"ordinal columns: {label_encoding_features}")
            logging.info(f"onehot columns: {onehot_encoding_features}")
            logging.info(f"Numerical columns: {numeric_features}")

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numeric_features),
                    ("label_pipeline",label_pipeline,label_encoding_features),
                    ("onehot_pipeline",onehot_pipeline,onehot_encoding_features)
                ]
            )

            return preprocessor    
            
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")
            logging.info("Obtaining preprocessor object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="Attrition"

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name].map({"No": 0, "Yes": 1})

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name].map({"No": 0, "Yes": 1})

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr=np.c_[input_feature_train_arr,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)        

