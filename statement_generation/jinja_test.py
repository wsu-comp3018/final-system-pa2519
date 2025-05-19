import jinja2
from jinja2 import Environment, FileSystemLoader

# Your data
data = {
    # claimant data
    "name": "Joel Crocker",
    "phone": "0491130126",
    "email": "example@gmail.com",
    "occupation": "Systems Administrator",
    "age": "22",
    "DOB": "20-09-2002",

    # injury info
    "location": "123 Fake St",
    "time": "12:37",
    "company_name": "Bathirst Liquor",
    "injury_date": "12 April 2025",
    "injury_details": "lower back nerve pain after lifting a box of paperwork",
    "client": "EPL"
}

# Jinja2 setup
env = Environment(loader=FileSystemLoader("templates/"))
template = env.get_template("josh_template.txt")

# Render the template with data
content = template.render(**data)

# Write to output file
filename = "statement_output2.txt"
with open(filename, mode="w", encoding="utf-8") as output:
    output.write(content)
    print("...wrote", filename)

