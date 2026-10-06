from import_script import getResourceSheet
import pandas as pd


def getResourceDf():
    resource_df = getResourceSheet()
    headers = resource_df.row_values(1)
    data = resource_df.get("A:BD")

    resource_df = pd.DataFrame(
        data[2:] ,
        columns = data[1]
    )
    resource_df.rename(columns={resource_df.columns[1] : "Resource Type"} , inplace=True)
    return resource_df

getResourceDf()