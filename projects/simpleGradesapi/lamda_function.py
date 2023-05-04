# Date: May 4, 2023
# Purpose: Code for Lambda Function

import json
import pandas as pd
import numpy as np

GET_RAW_PATH = "/getGrades"
ADD_RAW_PATH = "/addGrades"

def lambda_handler(event, context):
    if event['rawPath']== GET_RAW_PATH:
        # This gets printed to our logs
        print("Start Request for computing central tendency")
        
        student1_grade = int(event['queryStringParameters']['student1'])
        student2_grade = int(event['queryStringParameters']['student2'])
        student3_grade = int(event['queryStringParameters']['student3'])
        student4_grade = int(event['queryStringParameters']['student4'])
        student5_grade = int(event['queryStringParameters']['student5'])
        
        grades = np.array([student1_grade, student2_grade, student3_grade,
        student4_grade, student5_grade])
        mean = np.mean(grades)
        median = np.median(grades)
        std = round(np.std(grades),2)
        return{
            "Mean": str(mean),
            "Median": str(median),
            "Std": str(std)
        }
    
    if event['rawPath']== ADD_RAW_PATH:
        # This gets printed to our logs
        print("Adding to our database")
        return{
            "statusCode": 200,
            "body": "This has not been implemented yet."
        }
    
    