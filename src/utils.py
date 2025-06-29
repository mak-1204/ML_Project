import os
import sys
import pickle
import numpy as np
import pandas as pd
import dill
from src.exception import CustomException
from src.logger import logging
from sklearn.base import BaseEstimator, TransformerMixin

def save_object(file_path: str, obj: BaseEstimator) -> None:
    """
    Save a scikit-learn object to a file using pickle.
    
    Parameters:
    - file_path (str): The path where the object will be saved.
    - obj (BaseEstimator): The scikit-learn object to save.
    
    Returns:
    None
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
            
        logging.info(f"Object saved at {file_path}")

    except Exception as e:
        raise CustomException(e, sys)