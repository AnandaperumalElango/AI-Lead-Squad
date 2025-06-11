import re
from fuzzywuzzy import fuzz

def is_valid_email(email: str) -> bool:
    """Validate the format of an email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def deduplicate_leads(leads: list) -> list:
    """Remove duplicate leads based on email and company name similarity."""
    unique = []
    seen_emails = set()
    seen_companies = []

    for lead in leads:
        email = lead.get("Email", "").lower()
        company = lead.get("Company", "").lower()

        if email in seen_emails:
            continue

        duplicate = False
        for seen_company in seen_companies:
            if fuzz.ratio(company, seen_company) > 90:
                duplicate = True
                break

        if not duplicate:
            seen_emails.add(email)
            seen_companies.append(company)
            unique.append(lead)

    return unique
