#!/usr/bin/env python3
"""
Web to Markdown Converter
Converts web pages to Markdown format with support for links, images, and tables.
Enhanced with JavaScript rendering, smart content extraction, and URL handling.
"""

import requests
import argparse
import sys
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import html2text
import logging

# Optional: for JavaScript rendering
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger(__name__)


class WebToMarkdownConverter:
    """Convert web pages to Markdown format with advanced features."""
    
    def __init__(self, timeout=10, use_js=False, remove_navbar=True):
        """
        Initialize the converter.
        
        Args:
            timeout: Request timeout in seconds
            use_js: Use JavaScript rendering (requires Selenium)
            remove_navbar: Automatically remove navigation and sidebar elements
        """
        self.timeout = timeout
        self.use_js = use_js and SELENIUM_AVAILABLE
        self.remove_navbar = remove_navbar
        self.base_url = None
        
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.ignore_images = False
        self.h.body_width = 0  # Disable line wrapping
        self.h.unicode_snob = True
        
        # Selectors for common nav elements
        self.nav_selectors = [
            'nav', 'header', 'footer', '.navbar', '.sidebar', '.navigation',
            '[role="navigation"]', '[role="complementary"]',
            '.breadcrumb', '.search-box', '.ad', '[class*="ad-"]'
        ]
        
        # Selectors for main content (helps when removing nav)
        self.content_selectors = [
            'article', 'main', '[role="main"]',
            '.post-content', '.entry-content', '.content',
            '.page-content', '.docs-content'
        ]
        
    def fetch_url_with_requests(self, url):
        """
        Fetch content using requests library (fast but no JS).
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching URL with requests: {e}")
            return None
    
    def fetch_url_with_selenium(self, url):
        """
        Fetch content using Selenium (handles JavaScript).
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        if not SELENIUM_AVAILABLE:
            logger.warning("Selenium not available. Install with: pip install selenium")
            return None
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(self.timeout)
            
            try:
                driver.get(url)
                # Wait for page to load
                WebDriverWait(driver, self.timeout).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "body"))
                )
                html = driver.page_source
                return html
            finally:
                driver.quit()
                
        except Exception as e:
            logger.error(f"Error fetching URL with Selenium: {e}")
            return None
    
    def fetch_url(self, url):
        """
        Fetch URL content, trying JavaScript rendering if enabled.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        logger.info(f"Fetching: {url}")
        self.base_url = url
        
        # Try with JavaScript if enabled
        if self.use_js:
            logger.info("Using JavaScript rendering...")
            html = self.fetch_url_with_selenium(url)
            if html:
                return html
            logger.warning("JavaScript rendering failed, falling back to requests")
        
        # Use requests as fallback or primary method
        return self.fetch_url_with_requests(url)
    
    def find_main_content(self, soup):
        """
        Find the main content area using common selectors.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Main content element or original soup if not found
        """
        # Try common content selectors
        for selector in self.content_selectors:
            content = soup.select_one(selector)
            if content:
                logger.info(f"Found main content using selector: {selector}")
                return content
        
        return soup
    
    def clean_html(self, html_content):
        """
        Clean HTML content by removing unwanted elements.
        
        Args:
            html_content: Raw HTML content
            
        Returns:
            Cleaned HTML content
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unwanted tags
        for tag in soup.find_all(['script', 'style', 'meta', 'noscript', 'iframe']):
            tag.decompose()
        
        # Remove navigation/sidebar if enabled
        if self.remove_navbar:
            for selector in self.nav_selectors:
                for tag in soup.select(selector):
                    tag.decompose()
        
        return str(soup)
    
    def convert_relative_urls(self, html_content):
        """
        Convert relative URLs to absolute URLs.
        
        Args:
            html_content: HTML content with relative URLs
            
        Returns:
            HTML content with absolute URLs
        """
        if not self.base_url:
            return html_content
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Convert link hrefs
        for link in soup.find_all('a', href=True):
            link['href'] = urljoin(self.base_url, link['href'])
        
        # Convert image srcs
        for img in soup.find_all('img', src=True):
            img['src'] = urljoin(self.base_url, img['src'])
        
        return str(soup)
    
    def convert_html_to_markdown(self, html_content):
        """
        Convert cleaned HTML to Markdown.
        
        Args:
            html_content: HTML content to convert
            
        Returns:
            Markdown content
        """
        # Convert relative URLs first
        html_content = self.convert_relative_urls(html_content)
        return self.h.handle(html_content)
    
    def convert_url(self, url):
        """
        Convert a URL to Markdown.
        
        Args:
            url: URL to convert
            
        Returns:
            Markdown content or None if failed
        """
        html_content = self.fetch_url(url)
        
        if not html_content:
            return None
        
        logger.info("Cleaning HTML...")
        cleaned_html = self.clean_html(html_content)
        
        logger.info("Converting to Markdown...")
        markdown_content = self.convert_html_to_markdown(cleaned_html)
        
        return markdown_content
    
    def convert_file(self, file_path):
        """
        Convert a local HTML file to Markdown.
        
        Args:
            file_path: Path to HTML file
            
        Returns:
            Markdown content or None if failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Set base URL for relative links
            self.base_url = Path(file_path).resolve().as_uri()
            
            logger.info("Cleaning HTML...")
            cleaned_html = self.clean_html(html_content)
            
            logger.info("Converting to Markdown...")
            markdown_content = self.convert_html_to_markdown(cleaned_html)
            
            return markdown_content
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Convert web pages or HTML files to Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic conversion
  python web_to_markdown.py https://example.com
  
  # Save to file
  python web_to_markdown.py https://example.com -o output.md
  
  # Use JavaScript rendering for dynamic content
  python web_to_markdown.py https://example.com --js
  
  # Keep navigation elements
  python web_to_markdown.py https://example.com --keep-navbar
  
  # Convert local HTML file
  python web_to_markdown.py input.html -f
  
  # GitHub page with JavaScript and nav removal
  python web_to_markdown.py https://github.com/owner/repo --js -o output.md
        '''
    )
    
    parser.add_argument(
        'input',
        help='URL or file path to convert'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: print to stdout)'
    )
    parser.add_argument(
        '-f', '--file',
        action='store_true',
        help='Input is a local HTML file (default: treat as URL)'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=10,
        help='Request timeout in seconds (default: 10)'
    )
    parser.add_argument(
        '--js',
        action='store_true',
        help='Use JavaScript rendering for dynamic content (requires Selenium/ChromeDriver)'
    )
    parser.add_argument(
        '--keep-navbar',
        action='store_true',
        help='Keep navigation/sidebar elements (default: remove them)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    
    converter = WebToMarkdownConverter(
        timeout=args.timeout,
        use_js=args.js,
        remove_navbar=not args.keep_navbar
    )
    
    # Convert based on input type
    if args.file:
        markdown = converter.convert_file(args.input)
    else:
        markdown = converter.convert_url(args.input)
    
    if markdown is None:
        sys.exit(1)
    
    # Output result
    if args.output:
        try:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            logger.info(f"\n✓ Saved to: {output_path}")
        except Exception as e:
            logger.error(f"Error writing output: {e}")
            sys.exit(1)
    else:
        print(markdown)


if __name__ == '__main__':
    main()
