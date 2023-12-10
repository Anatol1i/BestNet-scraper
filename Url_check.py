from urllib.parse import urlparse
import pandas as pd
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}

def is_valid_url(url):
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return False
        if any(len(part) > 63 for part in result.netloc.split('.')):
            return False
        return True
    except:
        return False

def check_url_status(url):
    print(f"Processing URL: {url}")
    if not is_valid_url(url):
        return "Invalid URL"
    try:
        response = requests.get(url, headers=headers, timeout=5)
        return response.status_code
    except UnicodeError as e:
        print(f"Unicode Error for URL {url}: {e}")
        return "Unicode Error"
    except requests.RequestException as e:
        print(f"Request Exception for URL {url}: {e}")
        return "Request Exception"

df = pd.read_csv('file.csv', dtype=str)
df['Status'] = df['Website'].apply(check_url_status)

filtered_df = df[df['Status'].isin([200])]

filtered_df.to_csv('new_file.csv', index=False)

print(filtered_df)