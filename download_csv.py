import requests
from pathlib import Path
import pandas as pd
from typing import Optional
from io import StringIO
import util

parentPath = Path(__file__).parent
outputsPath = parentPath / 'Outputs'
root_settings = util.get_settings("core")
download_settings = root_settings['download']
save_settings = root_settings["save"]

def import_url(url: str = download_settings["download_link"]) -> pd.DataFrame:
    # outputsPath / ''
    resp = requests.get(url)
    resp.raise_for_status()

    csv_data = StringIO(resp.text)
    df = pd.read_csv(csv_data) # pyright: ignore[reportUnknownMemberType]

    if download_settings["save_download"]:
        # suffix = url[util.sub_get_last(url, "."):]
        # with open(outputsPath / (output_name + suffix), 'rb') as f:
            # f.write(resp.content)
        save_csv(df, no_html=True)
    return df

def save_csv(df: pd.DataFrame, output_name: str = util.format_with_date(download_settings["download_name"]), no_html: bool = False):
    if save_settings["save_csv"]:
        file_path_csv = outputsPath / (output_name + '.csv')
        df.to_csv(file_path_csv)
    if save_settings["save_html"] and not no_html:
        file_path_html = outputsPath / (output_name + '.html')
        # Convert to HTML table
        html_output = df.to_html(index=False, border=0, classes="table table-striped")
        html_output = html_output.replace("text-align: right;", "text-align: center;")

        # Save to HTML file
        with open(file_path_html, "w", encoding="utf-8") as f:
            f.write("""
            <html>
            <head>
                <title>{}</title>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            </head>
            <body class="p-4">
                <div class="container">
                    <h2 class="mb-4" style="text-align: center;">Technical Electives</h2>
                    {}
                </div>
            </body>
            </html>
            """.format(file_path_html.name, html_output))


if __name__ == "__main__":
    import_url()
    