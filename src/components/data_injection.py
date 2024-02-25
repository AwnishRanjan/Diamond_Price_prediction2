import os 
import sys 
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split
import pandas as pd 
from dataclasses import dataclass

# initilise datainjection configuration  #  save the paths which dataoinjection is doing 
@dataclass
class DataInjectionConfig:
    train_data_path = os.path.join('artifacts','train.csv')
    test_data_path = os.path.join('artifacts','test.csv')
    raw_data_path = os.path.join('artifacts','raw.csv')    # raw data before splitting


# create datainjection class 
class DataInjection:
    def __init__(self):
        self.injection_config = DataInjectionConfig()    # takes the names  train_data_path....etc

    def initiate_data_injection(self):
            logging.info('Data injection method started')

            try : 
                df = pd.read_csv(os.path.join('notebook/data','gemstone.csv'))
                logging.info('Data read as pandas dataframe ')

                os.makedirs(os.path.dirname(self.injection_config.raw_data_path),exist_ok=True)

                df.to_csv(self.injection_config.raw_data_path,index=False)

                logging.info("Train test split starting ")

                train_set, test_set = train_test_split(df,test_size=0.30 , random_state = 42)

                train_set.to_csv(self.injection_config.train_data_path,index = False,header=True)
                test_set.to_csv(self.injection_config.test_data_path,index = False,header=True)


                logging.info("Data injection completed")

                return(
                     self.injection_config.train_data_path,
                     self.injection_config.test_data_path
                )


            except Exception as e:
                 logging.info('Error occured in data injection config')





