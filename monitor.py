import asyncio
from pyppeteer import launch
import hashlib
import smtplib
from email.mime.text import MIMEText
import os
from PIL import Image, ImageChops
import io

async def capture_screenshot_hash(url):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 720})
    await page.goto(url, {'waitUntil': 'networkidle2'})
    screenshot = await page.screenshot()
    await browser.close()
    return hashlib.sha256(screenshot).hexdigest()

async def compare_screenshots(url, old_hash):
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 720})
    await page.goto(url, {'waitUntil': 'networkidle2'})
    screenshot_bytes = await page.screenshot()
    await browser.close()
    new_hash = hashlib.sha256(screenshot_bytes).hexdigest()

    if new_hash != old_hash:
        image1 = Image.open(io.BytesIO(screenshot_bytes))
        image2 = Image.open(io.BytesIO(bytes.fromhex(old_hash)))
        diff = ImageChops.difference(image1, image2)
        if diff.getbbox():
            return True
        else:
            return False
    else:
        return False

async def check_for_changes(urls):
    hashes = {}
    for url in urls:
        hashes[url] = await capture_screenshot_hash(url)

    while True:
        changed_urls = []
        for url in urls:
            if await compare_screenshots(url, hashes[url]):
                print(f"Visual change detected on {url}")
                changed_urls.append(url)
                hashes[url] = await capture_screenshot_hash(url)
            await asyncio.sleep(60)
        if changed_urls:
            await send_email(f"Visual layout changes detected on: \n{', '.join(changed_urls)}")

async def send_email(message):
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    smtp_server = os.environ.get('SMTP_SERVER')
    smtp_port = int(os.environ.get('SMTP_PORT'))
    smtp_username = os.environ.get('SMTP_USERNAME')

    msg = MIMEText(message)
    msg['Subject'] = "Website Visual Layout Change Detected"
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
