from pathlib import Path
import yaml
import datetime

parentPath = Path(__file__).parent
settingsPath = parentPath / "Settings"

def sub_get_last(value: str, search: str) -> int:
    best = -1
    while True:
        attempt = value.find(search, best + 1)
        if attempt == -1:
            break
        else:
            best = attempt
    return best

def get_settings(settingsName: str):
    return yaml.safe_load(open(settingsPath / (settingsName + '.yaml'), 'r'))

def format_with_date(input: str) -> str:
    output: str = datetime.datetime.now().strftime(input)
    return output