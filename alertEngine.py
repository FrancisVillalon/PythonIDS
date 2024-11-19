import pandas as pd
import numpy as np 



def calculateAnomaly(std,mean,weight,value):
    z = (value - mean) / std
    return z * weight


