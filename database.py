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
    resource_df["Status"] = resource_df["Status"].astype("string").str.strip()

    mask = (
        (resource_df["Status"] == "Inactive") |
        (resource_df["Status"].isna()) |
        (resource_df["Status"] == "")
    )
    resource_df = resource_df[~mask]
    return resource_df

getResourceDf()