import os
import sys 
from dataclasses import dataclass
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_models,get_best_model

@dataclass
class ModelTrainerConfig:  
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            smote = SMOTE(random_state=42)
            X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
            logging.info("Applied SMOTE to balance the classes in the training set")

            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000),
                "Random Forest": RandomForestClassifier(),
                "K-Neighbors Classifier": KNeighborsClassifier(),
                "XGBClassifier": XGBClassifier(),
                "CatBoosting Classifier": CatBoostClassifier(verbose=False),
                "AdaBoost Classifier": AdaBoostClassifier(),
                "SVC": SVC(probability=True),
                "GaussianNB": GaussianNB()
            }

            params = {
                "Logistic Regression": {
                "C": [0.01, 0.1, 1, 10],
                "solver": ["liblinear", "lbfgs"]
                },
                "Random Forest": {
                "n_estimators": [100, 200],
                "max_depth": [5, 10, None],
                "min_samples_split": [2, 5],
                },
                "K-Neighbors Classifier": {
                "n_neighbors": [3, 5, 7, 9],
                "weights": ["uniform", "distance"]
                },
                "XGBClassifier": {
                "n_estimators": [100, 200],
                "max_depth": [3, 5, 7],
                "learning_rate": [0.01, 0.1, 0.2],
                "subsample": [0.8, 1]
                },
                "CatBoosting Classifier": {
                "depth": [4, 6, 8],
                "learning_rate": [0.01, 0.1],
                "iterations": [200, 500]
                },
                "AdaBoost Classifier": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.1, 1.0]
                },
                "SVC": {
                "C": [0.1, 1, 10],
                "kernel": ["linear", "rbf"]
                },
                "GaussianNB": {
                "var_smoothing": [1e-09, 1e-08, 1e-07]
                }
            }
            
            model_report,trained_models=evaluate_models(X_train_res=X_train_res,y_train_res=y_train_res,X_test=X_test,y_test=y_test,models=models,param=params)    
            
            roc_threshold = 0.75 
            recall_threshold = 0.4 

            best_model_name, best_model_roc, best_model_recall = get_best_model(
            model_report, roc_threshold=roc_threshold, recall_threshold=recall_threshold
            )

            if best_model_name is None:
               logging.info("No model met the performance thresholds. Try tuning again.")
               return None, None, None
            else:
                best_model = trained_models[best_model_name]
                logging.info(
                f"Best Model Selected: {best_model_name} "
                f"(ROC_AUC={best_model_roc:.4f}, Recall={best_model_recall:.4f})"
                )

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            return best_model_name, best_model_roc, best_model_recall

        except Exception as e:
            raise CustomException(e,sys)    