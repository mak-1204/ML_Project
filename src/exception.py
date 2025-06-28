#to track exceptions in the code we use sys module
# and create a custom exception class that inherits from the Exception class
import sys
import logging


# Any exception that occurs in the code will be caught here
def error_message_details(error, error_details):
    """
    Print the error message and details.
    """
    _, _, exc_tb = error_details
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occurred in script: [{file_name}] at line number: [{exc_tb.tb_lineno}] with error message: [{str(error)}]"
    
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_details):
        """
        Custom exception class to handle exceptions with detailed error messages.
        """
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_details)

    def __str__(self):
        """
        Return the string representation of the error message.
        """
        return self.error_message  
    

