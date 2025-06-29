import os
import sys

from src.exception import CustomException
from src.logger import logging
# from src.components.data_ingestion import DataIngestion
from src.utils import save_object

from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        ''' This function creates a preprocessor object that handles 
        both numerical and categorical data transformations.
        It includes imputation, scaling, and encoding.'''

        try:
            numerical_columns = ['writing_score', 'reading_score']
            categorical_columns =  ['gender','race_ethnicity', 'parental_level_of_education',
                                    'lunch', 'test_preparation_course']

            numerical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),   # Fill missing values with median
                ('scaler', StandardScaler())                      # Standardize numerical features
            ])

            categorical_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),  # Fill missing values with most frequent
                ('onehot', OneHotEncoder(handle_unknown='ignore')),    # One-hot encode categorical features
                ('scaler', StandardScaler(with_mean=False))            # Scale categorical features
            ])

            logging.info("Numerical and categorical pipelines created successfully.")
            # Combine numerical and categorical pipelines into a preprocessor
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numerical_pipeline, numerical_columns),         # Numerical features
                    ('cat', categorical_pipeline, categorical_columns)      # Categorical features
                ]
            )
            logging.info("Preprocessor object created successfully.")

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)
    
    def initiate_data_transformation(self, train_path, test_path):
        logging.info("Entered the data transformation method or component")

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test dataframes successfully.")
            logging.info("Obtaining preprocessor object.")

            preprocessor_obj = self.get_data_transformer_object()
            target_column_name = 'math_score'
            numerical_columns = ['writing_score', 'reading_score']

            # Split the data into input features and target variable
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            # Transform the input features using the preprocessor
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessor to training and test dataframes.")

            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Data transformation completed successfully.")

            # Calling the save_object function to save the preprocessor object
            logging.info("Saving preprocessor object to file.")
            save_object(file_path=self.data_transformation_config.preprocessor_obj_file_path,
                        obj=preprocessor_obj)

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)