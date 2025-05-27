import re
from jinja2 import Template

# 1. Load Template
def load_template(filepath):
    with open(filepath, "r") as f:
        return Template(f.read())

# 2. Extraction Logic with re
def extract_structured_data(text):
    data = {}

    # Names
    first_name = re.search(r"Claimant's name is ([A-Za-z\-]+)", text)
    last_name = re.search(r"surname ([A-Za-z\-]+)", text)
    data["first_name"] = first_name.group(1).replace("-", "").capitalize() if first_name else ""
    data["last_name"] = last_name.group(1).replace("-", "").capitalize() if last_name else ""
    data["name"] = f"{data['first_name']} {data['last_name']}".strip()

    # Marital status
    data["marital_status"] = "Single" if "single" in text.lower() else "Unknown"

    # Dependents
    data["has_dependents"] = not "no dependent" in text.lower()

    # Injuries
    injury_keywords = ["injury", "fracture", "hematoma", "fracture", "pain", "twinge", "swells"]
    data["injuries"] = [line.strip() for line in text.split(".") if any(k in line.lower() for k in injury_keywords)]

    # Job history
    job_keywords = ["nurse", "clinic", "employer", "manual handling", "lifting", "admin"]
    data["job_history"] = [line.strip() for line in text.split(".") if any(k in line.lower() for k in job_keywords)]

    # Tasks / daily duties
    task_keywords = ["liaise", "clients", "paperwork", "email", "computer", "sitting"]
    data["tasks"] = [line.strip() for line in text.split(".") if any(k in line.lower() for k in task_keywords)]

    # Medical follow-up
    medical_keywords = ["doctor", "ultrasound", "physio", "referral", "practitioner"]
    data["medical_follow_up"] = [line.strip() for line in text.split(".") if any(k in line.lower() for k in medical_keywords)]

    # Phone
    phone_match = re.search(r"phone(?: number)?(?: is|:)?\s*([\d\s\-\+\(\)]{7,})", text, re.IGNORECASE)
    data["phone"] = phone_match.group(1).strip() if phone_match else "Unknown"


    # Email
    email_match = re.search(r"email(?: address)?(?: is|:)?\s*([\w\.-]+@[\w\.-]+\.\w+)", text, re.IGNORECASE)
    data["email"] = email_match.group(1).strip() if email_match else "Unknown"

    # Occupation (look for "occupation is X" or "works as X")
    occupation_match = re.search(r"I (?:was|am) a ([\w\s]+?)(?: for| in| at|\.|,|$)", text, re.IGNORECASE)
    if occupation_match:
        data["occupation"] = occupation_match.group(1).strip()
    else:
        data["occupation"] = "Unknown"


    # Date (date of statement or report)
    date_match = re.search(r"date(?: is|:)?\s*([\d]{1,2} [A-Za-z]+ \d{4})", text, re.IGNORECASE)
    data["date"] = date_match.group(1) if date_match else "DD-MM-YYYY"

    # Client / Company name
    client_match = re.search(r"(?:client|company) name(?: is|:)?\s*([A-Za-z\s]+)", text, re.IGNORECASE)
    data["client"] = client_match.group(1).strip() if client_match else "Unknown"
    data["company_name"] = data["client"]

    # Injury date
    injury_date_match = re.search(r"injury date(?: is|:)?\s*([A-Za-z0-9\s]+)", text, re.IGNORECASE)
    data["injury_date"] = injury_date_match.group(1).strip() if injury_date_match else "Unknown"

    # Age (look for "age is X")
    age_match = re.search(r"(\d{1,3}) years old", text)
    data["age"] = age_match.group(1) if age_match else "Unknown"

    # Date of birth (DOB)
    dob_match = re.search(r"born on the (\d{2}-\d{2}-\d{4})", text, re.IGNORECASE)
    data["dob"] = dob_match.group(1) if dob_match else "Unknown"

    # Driver's licence number
    licence_match = re.search(r"(?:driver's licence number|license number)(?: is|:)?\s*([\w\d]+)", text, re.IGNORECASE)
    data["drivers_licence_number"] = licence_match.group(1) if licence_match else "Unknown"

    # State (look for "state is X")
    state_match = re.search(r"state(?: is|:)?\s*([A-Z]{2,3})", text, re.IGNORECASE)
    data["state"] = state_match.group(1).upper() if state_match else "Unknown"

    # Incident description (reuse injuries or fallback)
    data["incident_description"] = data["injuries"][0] if data["injuries"] else "an unexpected incident"
    data["injury_details"] = "; ".join(data["injuries"]) if data["injuries"] else "minor discomfort"

    return data


# 3. Generate Statement
def generate_statement(input_text, template_path="josh_template.txt"):
    template = load_template(template_path)
    structured_data = extract_structured_data(input_text)
    return template.render(**structured_data)

# 4. Usage
if __name__ == "__main__":
    with open("summarised_skye.txt", "r") as f:
        raw_text = f.read()

    rendered_statement = generate_statement(raw_text)

    with open("final_statement.txt", "w") as f:
        f.write(rendered_statement)

    print("Statement generated and saved to 'final_statement.txt'")

 