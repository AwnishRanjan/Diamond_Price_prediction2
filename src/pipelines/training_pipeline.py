import os 
import sys 
from src.logger import logging
from src.exception import CustomException
import pandas as pd 

from src.components.data_injection import DataInjection




if __name__ == "__main__":
    obj = DataInjection()

    train_data_path , train_data_path = obj.initiate_data_injection()

    print(  train_data_path , train_data_path )