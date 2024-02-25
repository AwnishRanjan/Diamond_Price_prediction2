from sklearn.impute import SimpleImputer  # impute null values to what we want 
from sklearn.preprocessing import StandardScaler # to scale 
from sklearn.preprocessing import OrdinalEncoder  #categories to rank

from sklearn.pipeline import Pipeline   # pipeline creation 
from sklearn.compose import ColumnTransformer  # to join the pipelines 

import pandas as pd 
import numpy as np 
from dataclasses import dataclass
import os 
import sys 
from src.logger import logging
from src.exception import CustomException

from src.utils import save_object


# data transformaation config 
@dataclass
class DataTransformationConfig :
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')



# data injection config class 

class DataTransformation:
    def __init__(self):
        self.data_transformation_config  = DataTransformationConfig()

    def get_data_transformation_object(self):
        try:
            logging.info("Data transfromation initated ")

            categorical_cols = ['cut', 'color', 'clarity']
            numerical_cols = ['carat', 'depth', 'table', 'x', 'y', 'z']
            cut_map = ['Fair' ,'Good' ,'Very Good' ,'Premium' ,'Ideal']
            clearity_map = ['I1' ,'SI2' ,'SI1' ,'VS2' ,'VS1' ,'VVS2' , 'VVS1' , 'IF']
            colour_map = ['D','E','F','G','H','I','J']

            logging.info("pipelining initiated ")

            numerical_pipeline = Pipeline(
                steps = [('imputer',SimpleImputer(strategy='median')),
                          ('scaler',StandardScaler()) 
                   ]
                )

            categorical_pipeline =  Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('encoder', OrdinalEncoder(categories=[cut_map,colour_map,clearity_map])),
                ('scaler',StandardScaler())
                ]
            )

            preprocesser = ColumnTransformer(
                transformers=[('numerical_pipe',numerical_pipeline,numerical_cols),
                              ('categorical_pipe',categorical_pipeline,categorical_cols)
                            ]

             
                       )
            logging.info(" pipeline completed ")
            return preprocesser
        
            

        except Exception as e :
            logging.info("Error in Data Transformation")
            raise CustomException(e,sys)

    def initiate_data_transformation(self, train_path , test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df =  pd.read_csv(test_path)

            logging.info("Read train and test data")
            

            preprocessing_obj = self.get_data_transformation_object()

            target_col_name = 'price'
            drop_columns = [target_col_name,'id']
            
          #  divison in independent and dependent features
            # train
            input_features_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_features_train_df = train_df[target_col_name]
            #test 
            input_features_test_df = test_df.drop(columns=drop_columns,axis = 1)
            target_features_test_df = test_df[target_col_name]

            # print(target_features_test_df.columns)

             # Ensure target_features_test_df is a DataFrame
            if isinstance(target_features_test_df, pd.Series):
                target_features_test_df = target_features_test_df.to_frame()
            
            # print(target_features_test_df.columns)

            # preprocessing  on independent datas 
            input_features_train_array = preprocessing_obj.fit_transform(input_features_train_df)
            input_features_test_array = preprocessing_obj.transform(input_features_test_df)


            logging.info('Applying preprocessing in training and testing datasets')
            #concinate 
            train_arr = np.c_[input_features_train_array,np.array(target_features_train_df)]
            test_arr = np.c_[input_features_test_array, np.array(target_features_test_df)]

            # dump the pkl file 
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
             )

            logging.info("processor pickel is created and saved")

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )




        except Exception as e:
            logging.info("Error has occured in initiate_data_tranformation")
            raise CustomException(e,sys)





