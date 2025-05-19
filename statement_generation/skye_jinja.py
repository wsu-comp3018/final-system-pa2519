from jinja2 import Environment, FileSystemLoader

# Load template
env = Environment(loader=FileSystemLoader("templates/"))
template = env.get_template("josh_template.txt")

# Your extracted/filled-in data
data = {
    "name": "Skye Whiteley",
    "occupation": "Administration Officer",
    "phone": "Unknown",
    "email": "Unknown",
    "date": "19 May 2025",
    "location": "Workplace Office",
    "client": "EML Insurance",
    "company_name": "EML Insurance",
    "injury_date": "Approx. early April 2025",
    "age": "32",
    "DOB": "03 March 1993",
    "drivers_licence_number": "NSW1234567",
    "claim_number": "CLM-0029481",
    "time": "10:45am"
    # Add more fields as needed
}

# Render content
rendered_content = template.render(**data)

# Write to file
with open("final_statement.txt", "w", encoding="utf-8") as f:
    f.write(rendered_content)
    print("...wrote final_statement.txt")
