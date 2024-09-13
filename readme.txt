This code scrapes a financial website using Selenium. It:

Opens the website in headless Chrome.
Handles iframes to accept cookies.
Scrapes links from paginated pages.
Visits each link to extract fund details (name, ISIN, price, one-year change).
Scrapes the top 5 holdings and sector data.
Uses error handling to avoid crashes if elements are missing.