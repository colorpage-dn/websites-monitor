import time
import hashlib
from playwright.sync_api import sync_playwright

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

# Save a record of changes (to compare with next run)
previous_hashes = {}

def check_website_change(url):
    # Start Playwright and navigate to the website
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Take screenshot and get page content
        page.goto(url)
        page.screenshot(path=f"screenshots/{url.split('//')[1].split('/')[0]}.png")
        page_content = page.content()

        # Create hash of page content
        page_hash = hashlib.md5(page_content.encode()).hexdigest()

        # Check if the page content has changed
        change_detected = False
        if url in previous_hashes:
            if previous_hashes[url] != page_hash:
                change_detected = True
        previous_hashes[url] = page_hash

        browser.close()

        return change_detected, url

# List to store URLs with changes
changed_urls = []

# Check each URL for changes
for url in URLs:
    change_detected, url = check_website_change(url)
    if change_detected:
        changed_urls.append(url)

# If there are changes, store the list for email
if changed_urls:
    with open('changed_urls.txt', 'w') as f:
        f.write('\n'.join(changed_urls))
