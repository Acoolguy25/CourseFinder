import requests
from pathlib import Path
import pandas as pd
from typing import Optional
from io import StringIO

parentPath = Path(__file__).parent
outputsPath = parentPath / 'Outputs'

def sub_get_last(value: str, search: str) -> int:
    best = -1
    while True:
        attempt = value.find(search, best + 1)
        if attempt == -1:
            break
        else:
            best = attempt
    return best

def import_url(url: str, output_name: Optional[str]) -> pd.DataFrame:
    # outputsPath / ''
    resp = requests.get(url)
    resp.raise_for_status()

    csv_data = StringIO(resp.text)
    df = pd.read_csv(csv_data) # pyright: ignore[reportUnknownMemberType]

    if output_name:
        
        suffix = url[sub_get_last(url, "."):]
        # with open(outputsPath / (output_name + suffix), 'rb') as f:
            # f.write(resp.content)
        df.to_csv(outputsPath / (output_name + suffix))
    return df

if __name__ == "__main__":
    import_url("https://waf.cs.illinois.edu/visualizations/Grade-Disparities-and-Accolades-by-Instructor/final.csv",
               "test")
    