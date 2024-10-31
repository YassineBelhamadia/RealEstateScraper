# importing the necessary libraries

import pandas as pd
import numpy as np




def data_to_csv(data) :

    """
        params : data from the main script
        logic : transforms the data into a csv file and making the right adjustments
        return : none 
    """

    # creating a pandas dataFrame from the data list of dictionnaries
    df = pd.DataFrame(data)

    df.to_csv('./data/output.csv',index=True)

   