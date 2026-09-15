#!/usr/bin/env python3
"""
Web to Markdown Converter
Converts web pages to Markdown format with support for links, images, and tables.
"""

import requests
import argparse
import sys
from pathlib import Path
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import html2text


class WebToMarkdownConverter:
    """Convert web pages to Markdown format."""
    
    def __init__(self, timeout=10):
        """
        Initialize the converter.
        
        Args:
            timeout: Request timeout in seconds
        """
        self.timeout = timeout
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.ignore_images = False
        self.h.body_width = 0  # Disable line wrapping
        
    def fetch_url(self, url):
        """
        Fetch content from URL.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching URL: {e}", file=sys.stderr)
            return None
    
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
        for tag in soup.find_all(['script', 'style', 'meta', 'noscript']):
            tag.decompose()
        
        # Remove navigation and footer if possible
        for tag in soup.find_all(['nav', 'footer']):
            tag.decompose()
        
        return str(soup)
    
    def convert_html_to_markdown(self, html_content):
        """
        Convert cleaned HTML to Markdown.
        
        Args:
            html_content: HTML content to convert
            
        Returns:
            Markdown content
        """
        return self.h.handle(html_content)
    
    def convert_url(self, url):
        """
        Convert a URL to Markdown.
        
        Args:
            url: URL to convert
            
        Returns:
            Markdown content or None if failed
        """
        print(f"Fetching: {url}", file=sys.stderr)
        html_content = self.fetch_url(url)
        
        if not html_content:
            return None
        
        print("Cleaning HTML...", file=sys.stderr)
        cleaned_html = self.clean_html(html_content)
        
        print("Converting to Markdown...", file=sys.stderr)
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
            
            print("Cleaning HTML...", file=sys.stderr)
            cleaned_html = self.clean_html(html_content)
            
            print("Converting to Markdown...", file=sys.stderr)
            markdown_content = self.convert_html_to_markdown(cleaned_html)
            
            return markdown_content
        except FileNotFoundError:
            print(f"File not found: {file_path}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error processing file: {e}", file=sys.stderr)
            return None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Convert web pages or HTML files to Markdown',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Convert a web page and print to stdout
  python web_to_markdown.py https://example.com
  
  # Convert and save to file
  python web_to_markdown.py https://example.com -o output.md
  
  # Convert local HTML file
  python web_to_markdown.py input.html -f
  
  # Convert and save local file
  python web_to_markdown.py input.html -f -o output.md
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
    
    args = parser.parse_args()
    
    converter = WebToMarkdownConverter(timeout=args.timeout)
    
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
            print(f"\n✓ Saved to: {output_path}", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(markdown)


if __name__ == '__main__':
    main()
