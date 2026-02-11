"""Fetch modules for URL and PDF content extraction."""

from src.fetch.url_fetcher import fetch_article_from_url
from src.fetch.pdf_reader import extract_text_from_pdf

__all__ = ["fetch_article_from_url", "extract_text_from_pdf"]
