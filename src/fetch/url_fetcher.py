"""
Fetch article text from URLs.
"""

from typing import Tuple

try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def fetch_article_from_url(url: str, timeout: int = 30) -> Tuple[bool, str, str]:
    """
    Fetch and extract article text from a URL.

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Tuple of (success, message, article_text)
    """
    if not REQUESTS_AVAILABLE:
        return False, "requests and beautifulsoup4 not installed. Run: pip install requests beautifulsoup4", ""

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Remove script and style elements
        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()

        # Try to find article content in common containers
        article_text = ""

        # Priority 1: <article> tag
        article = soup.find("article")
        if article:
            article_text = article.get_text(separator="\n", strip=True)

        # Priority 2: main content div
        if not article_text:
            main = soup.find("main") or soup.find("div", class_=["content", "article", "post", "entry"])
            if main:
                article_text = main.get_text(separator="\n", strip=True)

        # Priority 3: body text (fallback)
        if not article_text:
            body = soup.find("body")
            if body:
                article_text = body.get_text(separator="\n", strip=True)

        if not article_text:
            return False, "Could not extract text from page", ""

        # Clean up whitespace
        lines = [line.strip() for line in article_text.split("\n") if line.strip()]
        article_text = "\n".join(lines)

        return True, "Success", article_text

    except requests.exceptions.Timeout:
        return False, f"Request timed out after {timeout}s", ""
    except requests.exceptions.RequestException as e:
        return False, f"Request failed: {e}", ""
    except Exception as e:
        return False, f"Error extracting text: {e}", ""
