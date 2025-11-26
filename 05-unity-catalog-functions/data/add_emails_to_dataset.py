"""
Add Email Addresses to Existing Santa Letters Dataset
Takes the real santa_letters_canada.csv and adds realistic email addresses
"""

import csv
import random

def generate_email(name, city):
    """Generate a realistic email address for a child."""
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "mail.com"]

    # Clean name (remove spaces, lowercase)
    clean_name = name.lower().replace(" ", "")

    # Clean city for use in email (take first 3 chars)
    clean_city = city.lower().replace(" ", "")[:3] if city else "can"

    # Create username variations
    username_styles = [
        f"{clean_name}{random.randint(2010, 2018)}",  # lucas2015
        f"{clean_name}.{clean_city}",                  # lucas.bra
        f"{clean_name}{random.choice(['123', '456', '789'])}",  # lucas123
        f"{clean_name}.{random.choice(['m', 'smith', 'wilson', 'brown', 'jones', 'miller'])}"  # lucas.smith
    ]

    username = random.choice(username_styles)
    domain = random.choice(domains)

    return f"{username}@{domain}"

def add_emails_to_csv(input_file, output_file):
    """Add email column to existing CSV with 80% fill rate."""

    records_processed = 0
    records_with_email = 0

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.DictReader(infile)

        # Add 'email' to fieldnames
        fieldnames = ['name', 'email', 'province', 'city', 'date', 'letter', 'gifts']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            # Generate email for 80% of records
            if random.random() < 0.8:
                row['email'] = generate_email(row['name'], row['city'])
                records_with_email += 1
            else:
                row['email'] = ''

            writer.writerow(row)
            records_processed += 1

            # Progress indicator
            if records_processed % 1000 == 0:
                print(f"Processed {records_processed} records...")

    print(f"\n✅ Processing complete!")
    print(f"📊 Total records: {records_processed}")
    print(f"📧 Records with email: {records_with_email}")
    print(f"📭 Records without email: {records_processed - records_with_email}")
    print(f"📈 Email fill rate: {records_with_email / records_processed * 100:.1f}%")
    print(f"\n💾 Saved to: {output_file}")

if __name__ == "__main__":
    input_csv = "/Users/danny.park/Downloads/santa_letters_canada.csv"
    output_csv = "/Users/danny.park/dbrx-12daysofdemos/05-unity-catalog-functions/data/santa_letters_canada_with_emails.csv"

    print("📧 Adding emails to Santa letters dataset...")
    print(f"📥 Reading from: {input_csv}")
    print(f"📤 Writing to: {output_csv}\n")

    add_emails_to_csv(input_csv, output_csv)

    # Print sample records
    print("\n📝 Sample Records:")
    with open(output_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, 1):
            if i <= 5:
                print(f"\n--- Record {i} ---")
                print(f"Name: {row['name']}")
                print(f"Email: {row['email'] if row['email'] else 'N/A'}")
                print(f"City: {row['city']}, {row['province']}")
                print(f"Gifts: {row['gifts']}")
            else:
                break
