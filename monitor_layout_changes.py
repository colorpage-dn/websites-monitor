import os
import time
import pixelmatch
from selenium import webdriver
from PIL import Image
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
from io import BytesIO

# List of URLs to monitor
urls_to_monitor = [
    'https://abcfuels.com/',
    'https://adventvalue.com/',
    'https://ahcllc.net/',
    'https://capsfund.org/',
    'https://carlbellplumbing.com/',
    'https://centerforspectrumservices.org/',
    'https://classroomauthors.com/',
    'https://colorpageonline.com/',
    'https://destinationrugby.com/',
    'https://dutchessfair.com/',
    'https://gcpennysaver.com/',
    'https://grassandgardens.com/',
    'https://greenheronfarm.com/',
    'https://herzogs.com/',
    'https://hopefarmpress.com/',
    'https://hvribfest.com/',
    'https://www.jeffloweplumbing.com/',
    'https://kingstonplaza.com/',
    'https://kingstonvisitorsguide.com/',
    'https://lhvprecast.com/',
    'https://mahv.net/',
    'https://mastenenterprises.com/',
    'https://mcgowanmasonry.com/',
    'https://newyorkinjurylaw.net/',
    'https://nve-cd.com/',
    'https://nveoffer.com/',
    'https://proguardcoverage.com/',
    'https://www.rbtcpas.com/',
    'https://rdcontracting-ny.com/',
    'https://rhinebeckcarshow.net/',
    'https://specpension.com/',
    'https://ucitalianamericanfoundation.org/',
    'https://ucpennysaver.com/',
    'https://ulsterchamber.net/',
    'https://ulstercountyfair.com/',
    'https://yourshoppersguide.com/',
]

# Directory to save screenshots
screenshot_dir = './screenshots/'

# Ensure the directory exists
os.makedirs(screenshot_dir, exist_ok=True)

def capture_screenshot(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)  # Allow time for CSS and content to load
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(screenshot_dir, f"{timestamp}_{url.replace('https://', '').replace('/', '_')}.png")
    driver.save_screenshot(screenshot_path)
    driver.quit()
    return screenshot_path

def compare_screenshots(old_screenshot_path, new_screenshot_path):
    old_image = Image.open(old_screenshot_path)
    new_image = Image.open(new_screenshot_path)

    # Convert images to grayscale and then to numpy arrays
    old_image = old_image.convert('L')
    new_image = new_image.convert('L')
    old_image_np = np.array(old_image)
    new_image_np = np.array(new_image)

    # Compare images using Pixelmatch
    diff = pixelmatch(old_image_np, new_image_np, None, old_image_np.shape[1], old_image_np.shape[0], threshold=0.1)
    return diff

def send_email_alert(subject, body, recipient_email, smtp_host, smtp_port, smtp_user, smtp_pass, sender_email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_pass)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)

# SMTP credentials (to be replaced with GitHub secrets)
smtp_host = os.getenv("SMTP_HOST")
smtp_port = os.getenv("SMTP_PORT")
smtp_user = os.getenv("SMTP_USER")
smtp_pass = os.getenv("SMTP_PASS")
sender_email = os.getenv("SENDER_EMAIL")
recipient_email = "dnolan@tsasinc.com"  # Fixed recipient

for url in urls_to_monitor:
    new_screenshot = capture_screenshot(url)

    # Check if there are existing screenshots
    existing_screenshots = sorted(os.listdir(screenshot_dir), reverse=True)

    if existing_screenshots:
        # Compare with the most recent screenshot
        previous_screenshot_path = os.path.join(screenshot_dir, existing_screenshots[0])
        diff = compare_screenshots(previous_screenshot_path, new_screenshot)

        if diff > 100:  # Arbitrary threshold for significant changes
            subject = f"GitHub Monitor - Website Change Alert: {url}"
            body = f"Significant layout change detected for {url}. Please check the website."
            send_email_alert(subject, body, recipient_email, smtp_host, smtp_port, smtp_user, smtp_pass, sender_email)
    else:
        print(f"No previous screenshot found for {url}, saving the first one.")
