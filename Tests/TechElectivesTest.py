from bs4 import BeautifulSoup
import re

# Load the HTML file
with open("C:/Users/ryanb/Documents/WinProjects/CourseFinder/Tests/TechElectives.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

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
print(course_codes)
