import pandas as pd 
import numpy as np 
from dataclasses import dataclass
import os 
import sys 
from src.logger import logging
from src.exception import CustomException
from sklearn.linear_model import LinearRegression, Lasso,Ridge,ElasticNet
from src.utils import evaluate_model,save_object


@dataclass
class Modeltrainerconfig :
    trained_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = Modeltrainerconfig()
    
    def initiate_model_training(self,train_arr,test_arr):
        try:
            logging.info("split train and test variables")

            X_train,X_test,y_train,y_test = (
                train_arr[:,:-1],
                test_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,-1]

            )

            models ={
                       'LinearRegression' : LinearRegression(),
                       'Lasso,': Lasso(),
                       'Ridge':Ridge(),
                       'ElasticNet': ElasticNet()
                }
            
            model_report: dict = evaluate_model(X_train,y_train,X_test,y_test,models)

            print(model_report)

            print('\n=======================================================')
            logging.info(f'Model report : {model_report}')

            #get best model 
            if model_report is not None:
                best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            logging.info(f'best model : {best_model_name},R2 score : {best_model_score}')

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )



        except Exception as e:
           logging.info("Error occured in training model")
           raise CustomException(e,sys)