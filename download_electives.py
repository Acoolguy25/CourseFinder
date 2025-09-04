from bs4 import BeautifulSoup
import re
import util
import requests
from pathlib import Path

parentPath = Path(__file__).parent
outputsPath = parentPath / "Outputs"

electives_settings = util.get_settings("core")["electives"]

def download_electives() -> list:
    # Load the HTML file
    # with open("C:/Users/ryanb/Documents/WinProjects/CourseFinder/Tests/TechElectives.html", "r", encoding="utf-8") as f:
        # html = f.read()
    resp = requests.get(electives_settings["electives_link"])
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the section after <h3><strong>Technical Electives</strong></h3>
    tech_header = soup.find("h3", string=lambda s: s and "Technical Electives" in s) # pyright: ignore[reportArgumentType]
    tech_table = tech_header.find_next("table") if tech_header else None

    course_codes = []
    if tech_table:
        # Extract text like "AE 452", "ECE 411", etc.
        for a in tech_table.find_all("a", href=True): # pyright: ignore[reportAttributeAccessIssue]
            match = re.match(r"([A-Z]{2,4})\s+(\d{2,3})", a.get("title").replace("\xa0", " ")) # pyright: ignore[reportOptionalMemberAccess, reportAttributeAccessIssue]
            if match:
                course_codes.append(f"{match.group(1)} {match.group(2)}")

    course_codes.sort()
    if electives_settings["save_electives"]:
        with open(outputsPath / util.format_with_date(electives_settings["save_electives_name"] + ".txt"), "w") as f:
            f.write("\n".join(course_codes))
    return course_codes

if __name__ == "__main__":
    download_electives()