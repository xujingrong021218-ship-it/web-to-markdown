#!/usr/bin/env python3
"""
Example usage of Web to Markdown converter as a library.
"""

from web_to_markdown import WebToMarkdownConverter
from pathlib import Path


def example_1_convert_url():
    """Example 1: Convert a URL and print to stdout"""
    print("=" * 50)
    print("Example 1: Convert URL to Markdown")
    print("=" * 50)
    
    converter = WebToMarkdownConverter()
    markdown = converter.convert_url('https://www.wikipedia.org')
    
    if markdown:
        # Print first 500 characters
        print(markdown[:500])
        print("\n... (truncated for display)")


def example_2_convert_and_save():
    """Example 2: Convert URL and save to file"""
    print("\n" + "=" * 50)
    print("Example 2: Convert URL and save to file")
    print("=" * 50)
    
    converter = WebToMarkdownConverter()
    markdown = converter.convert_url('https://www.python.org')
    
    if markdown:
        output_file = Path('python_org.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"✓ Saved to: {output_file}")
        print(f"File size: {len(markdown)} characters")


def example_3_convert_local_html():
    """Example 3: Convert local HTML file"""
    print("\n" + "=" * 50)
    print("Example 3: Convert local HTML file")
    print("=" * 50)
    
    # Create a sample HTML file first
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sample Page</title>
        <script>console.log('This should be removed')</script>
    </head>
    <body>
        <h1>Hello World</h1>
        <p>This is a sample HTML file.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        <a href="https://example.com">Example Link</a>
        <img src="https://example.com/image.jpg" alt="Sample Image">
    </body>
    </html>
    """
    
    sample_file = Path('sample.html')
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_html)
    
    converter = WebToMarkdownConverter()
    markdown = converter.convert_file(str(sample_file))
    
    if markdown:
        print("Converted Markdown:")
        print(markdown)
        
        # Clean up
        sample_file.unlink()


def example_4_batch_conversion():
    """Example 4: Batch convert multiple URLs"""
    print("\n" + "=" * 50)
    print("Example 4: Batch conversion")
    print("=" * 50)
    
    urls = [
        ('https://www.github.com', 'github.md'),
        ('https://www.google.com', 'google.md'),
    ]
    
    converter = WebToMarkdownConverter(timeout=15)
    
    for url, output_file in urls:
        print(f"\nConverting: {url}")
        markdown = converter.convert_url(url)
        
        if markdown:
            output_path = Path(output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown)
            print(f"✓ Saved to: {output_path} ({len(markdown)} chars)")
        else:
            print(f"✗ Failed to convert: {url}")


if __name__ == '__main__':
    print("\nWeb to Markdown Converter - Examples\n")
    
    # Run examples
    example_1_convert_url()
    example_2_convert_and_save()
    example_3_convert_local_html()
    # Uncomment to run batch example (may take longer)
    # example_4_batch_conversion()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("=" * 50)
