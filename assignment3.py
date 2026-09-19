import argparse
import csv
import io
import re
import urllib.request
from datetime import datetime

def download_data(url):
    """Download the web log CSV file from the given URL."""
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    return data

def process_data(data):
    """Process the CSV data and store each request."""
    requests = []

    csv_file = io.StringIO(data)
    reader = csv.reader(csv_file)

    for row in reader:
        if len(row) >= 5:
            requests.append(row)

    return requests

def calculate_image_percentage(requests):
    """Calculate the percentage of requests for image files."""
    image_count = 0
    image_pattern = re.compile(r'\.(jpg|gif|png)$', re.IGNORECASE)

    for row in requests:
        path = row[0].strip()

        if image_pattern.search(path):
            image_count += 1

    if len(requests) == 0:
        return 0

    return (image_count / len(requests)) * 100

def find_most_popular_browser(requests):
    """Find the most popular browser."""
    browser_counts = {
        "Firefox": 0,
        "Chrome": 0,
        "Internet Explorer": 0,
        "Safari": 0
    }

    for row in requests:
        user_agent = row[2]

        if re.search(r'Firefox', user_agent, re.IGNORECASE):
            browser_counts["Firefox"] += 1
        elif re.search(r'Chrome', user_agent, re.IGNORECASE):
            browser_counts["Chrome"] += 1
        elif re.search(r'MSIE|Trident', user_agent, re.IGNORECASE):
            browser_counts["Internet Explorer"] += 1
        elif re.search(r'Safari', user_agent, re.IGNORECASE):
            browser_counts["Safari"] += 1

    return max(browser_counts, key=browser_counts.get)

def calculate_hourly_hits(requests):
    """Count the number of requests for each hour of the day."""
    hourly_hits = {hour: 0 for hour in range(24)}

    for row in requests:
        date_string = row[1].strip()

        try:
            access_time = datetime.strptime(date_string, "%m/%d/%Y %H:%M:%S")
            hourly_hits[access_time.hour] += 1
        except ValueError:
            continue

    return hourly_hits

def main(url):
    print(f"Running main with URL = {url}...")
    data = download_data(url)
    requests = process_data(data)

    print(f"Total requests: {len(requests)}")
    
    image_percentage = calculate_image_percentage(requests)
    print(f"Image requests account for {image_percentage:.1f}% of all requests")

    popular_browser = find_most_popular_browser(requests)
    print(f"The most popular browser is {popular_browser}")

    hourly_hits = calculate_hourly_hits(requests)

    for hour, hits in sorted(hourly_hits.items(), key=lambda item: item[1], reverse=True):
        print(f"Hour {hour:02d} has {hits} hits")


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
    
