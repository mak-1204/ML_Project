import os
import sys
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation

import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'raw.csv')

class DataIngestion:
    def __init__ (self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")

        try:   
            #Reading the dataset can be done from any source, here we are using a local CSV file
            df=pd.read_csv("notebook/data/stud.csv")
            logging.info("Read the dataset as dataframe")

            #Checking if the dataset is empty
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            #Storing the train and test split in the artifacts folder
            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Ingestion of the data is completed")
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        
        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":

    #Data ingestion process
    obj = DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    print("Data ingestion completed successfully.")
    
    # Now we can proceed with data transformation
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)