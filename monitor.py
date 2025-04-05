import asyncio
from pyppeteer import launch
import hashlib
import smtplib
from email.mime.text import MIMEText
import os

async def capture_layout_hash(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})
    content = await page.content()
    await browser.close()
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

async def check_for_changes(urls):
    hashes = {}
    for url in urls:
        hashes[url] = await capture_layout_hash(url)

    while True:
        await asyncio.sleep(600)  # Check every 10 minutes (adjust as needed)
        for url in urls:
            new_hash = await capture_layout_hash(url)
            if new_hash != hashes[url]:
                print(f"Change detected on {url}")
                await send_email(f"Layout change detected on {url}")
                hashes[url] = new_hash

async def send_email(message):
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT'))
    smtp_username = os.environ.get('SMTP_USERNAME')

    msg = MIMEText(message)
    msg['Subject'] = "Website Layout Change Detected"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

async def main():
    urls = [
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
        "https://yourshoppersguide.com/",
    ]
    await check_for_changes(urls)

if __name__ == "__main__":
    asyncio.run(main())
