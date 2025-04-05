import requests
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# List of URLs to monitor
URLs = [
    "https://abcfuels.com/",
    "https://adventvalue.com/",
    "https://ahcllc.net/",
    "https://capsfund.org/",
    "https://carlbellplumbing.com/",
    "https://centerforspectrumservices.org/",
    "https://classroomauthors.com/",
    "https://colorpageonline.com/",
    "https://destinationrugby.com/",
    "https://dutchessfair.com/",
    "https://gcpennysaver.com/",
    "https://grassandgardens.com/",
    "https://greenheronfarm.com/",
    "https://herzogs.com/",
    "https://hopefarmpress.com/",
    "https://hvribfest.com/",
    "https://www.jeffloweplumbing.com/",
    "https://kingstonplaza.com/",
    "https://kingstonvisitorsguide.com/",
    "https://lhvprecast.com/",
    "https://mahv.net/",
    "https://mastenenterprises.com/",
    "https://mcgowanmasonry.com/",
    "https://newyorkinjurylaw.net/",
    "https://nve-cd.com/",
    "https://nveoffer.com/",
    "https://proguardcoverage.com/",
    "https://www.rbtcpas.com/",
    "https://rdcontracting-ny.com/",
    "https://rhinebeckcarshow.net/",
    "https://specpension.com/",
    "https://ucitalianamericanfoundation.org/",
    "https://ucpennysaver.com/",
    "https://ulsterchamber.net/",
    "https://ulstercountyfair.com/",
    "https://yourshoppersguide.com/"
]

# Function to hash the content of the page to detect changes
def get_page_hash(url):
    response = requests.get(url)
    page_hash = hashlib.md5(response.text.encode('utf-8')).hexdigest()
    return page_hash

# Load previously saved hashes from file (if any)
def load_previous_hashes():
    if os.path.exists("previous_hashes.txt"):
        with open("previous_hashes.txt", "r") as file:
            return {line.split()[0]: line.split()[1] for line in file.readlines()}
    return {}

# Save the current hashes to file
def save_current_hashes(hashes):
    with open("previous_hashes.txt", "w") as file:
        for url, page_hash in hashes.items():
            file.write(f"{url} {page_hash}\n")

# Send email notification
def send_email(subject, body):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECIPIENT_EMAIL")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print(f"Alert email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main function to check for changes
def monitor_changes():
    previous_hashes = load_previous_hashes()
    current_hashes = {}

    for url in URLs:
        print(f"Checking {url}...")
        current_hashes[url] = get_page_hash(url)

        if url in previous_hashes:
            if current_hashes[url] != previous_hashes[url]:
                print(f"Layout change detected on {url}")
                send_email(f"GitHub Monitor - Website Change Alert", f"Layout change detected on {url}")
        else:
            print(f"First check for {url}")
        
    save_current_hashes(current_hashes)

if __name__ == "__main__":
    monitor_changes()
