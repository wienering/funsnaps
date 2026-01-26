#!/usr/bin/env python3
"""
Asset extraction script for funsnaps.ca
Extracts images, contact info, and content from downloaded HTML files
"""

import os
import re
import json
import urllib.request
import urllib.parse
from pathlib import Path
from html.parser import HTMLParser
from collections import defaultdict

class ImageExtractor(HTMLParser):
    """Extract image URLs from HTML"""
    def __init__(self):
        super().__init__()
        self.images = set()
        self.in_style = False
        self.current_style = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == 'style':
            self.in_style = True
            self.current_style = ""
        
        # Extract from img src, data-src, srcset
        for attr_name, attr_value in attrs:
            if attr_value and attr_name in ['src', 'data-src', 'data-lazy-src', 'srcset']:
                if attr_name == 'srcset':
                    # Parse srcset (format: url1 1x, url2 2x)
                    urls = re.findall(r'(https?://[^\s,]+)', attr_value)
                    self.images.update(urls)
                else:
                    if attr_value.startswith('http'):
                        self.images.add(attr_value)
                    elif attr_value.startswith('/'):
                        self.images.add('https://www.funsnaps.ca' + attr_value)
        
        # Extract from background-image in style attributes
        for attr_name, attr_value in attrs:
            if attr_name == 'style' and attr_value:
                bg_images = re.findall(r'background-image:\s*url\(["\']?([^"\']+)["\']?\)', attr_value)
                for img in bg_images:
                    if img.startswith('http'):
                        self.images.add(img)
                    elif img.startswith('/'):
                        self.images.add('https://www.funsnaps.ca' + img)
    
    def handle_data(self, data):
        if self.in_style:
            self.current_style += data
    
    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False
            # Extract background-image from style tags
            bg_images = re.findall(r'background-image:\s*url\(["\']?([^"\']+)["\']?\)', self.current_style)
            for img in bg_images:
                if img.startswith('http'):
                    self.images.add(img)
                elif img.startswith('/'):
                    self.images.add('https://www.funsnaps.ca' + img)
            self.current_style = ""

def extract_images_from_html(html_file):
    """Extract all image URLs from an HTML file"""
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Also extract from JSON-LD schema
    schema_images = re.findall(r'"url":\s*"([^"]+\.(?:jpg|jpeg|png|gif|webp|svg))"', content, re.IGNORECASE)
    schema_images.extend(re.findall(r'"image":\s*"([^"]+\.(?:jpg|jpeg|png|gif|webp|svg))"', content, re.IGNORECASE))
    schema_images.extend(re.findall(r'"logo":\s*"([^"]+\.(?:jpg|jpeg|png|gif|webp|svg))"', content, re.IGNORECASE))
    
    # Extract from meta tags
    meta_images = re.findall(r'<meta[^>]+(?:property|content)=["\']([^"\']+\.(?:jpg|jpeg|png|gif|webp|svg))["\']', content, re.IGNORECASE)
    
    # Use HTML parser
    parser = ImageExtractor()
    parser.feed(content)
    
    all_images = parser.images.copy()
    all_images.update(schema_images)
    all_images.update(meta_images)
    
    # Filter to only funsnaps.ca images
    funsnaps_images = {img for img in all_images if 'funsnaps.ca' in img or img.startswith('/')}
    
    return funsnaps_images

def extract_contact_info(html_file):
    """Extract contact information from HTML"""
    with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    contact_info = {
        'phone': [],
        'email': [],
        'address': {},
        'social_media': {}
    }
    
    # Extract phone numbers
    phone_patterns = [
        r'\+?1?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',
        r'tel:([+\d\s\-\(\)]+)',
        r'"telephone":\s*"([^"]+)"',
    ]
    
    for pattern in phone_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                phone = ''.join(match)
            else:
                phone = match
            if phone and phone not in contact_info['phone']:
                contact_info['phone'].append(phone)
    
    # Extract emails
    email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    emails = re.findall(email_pattern, content)
    contact_info['email'] = list(set(emails))
    
    # Extract from JSON-LD schema
    schema_match = re.search(r'"address":\s*\{[^}]+\}', content)
    if schema_match:
        addr_content = schema_match.group(0)
        street = re.search(r'"streetAddress":\s*"([^"]+)"', addr_content)
        city = re.search(r'"addressLocality":\s*"([^"]+)"', addr_content)
        region = re.search(r'"addressRegion":\s*"([^"]+)"', addr_content)
        postal = re.search(r'"postalCode":\s*"([^"]+)"', addr_content)
        country = re.search(r'"addressCountry":\s*"([^"]+)"', addr_content)
        
        if street:
            contact_info['address']['street'] = street.group(1)
        if city:
            contact_info['address']['city'] = city.group(1)
        if region:
            contact_info['address']['region'] = region.group(1)
        if postal:
            contact_info['address']['postal_code'] = postal.group(1)
        if country:
            contact_info['address']['country'] = country.group(1)
    
    # Extract social media
    facebook = re.search(r'facebook\.com/([^/"\')\s]+)', content, re.IGNORECASE)
    instagram = re.search(r'instagram\.com/([^/"\')\s]+)', content, re.IGNORECASE)
    
    if facebook:
        contact_info['social_media']['facebook'] = f"https://www.facebook.com/{facebook.group(1)}"
    if instagram:
        contact_info['social_media']['instagram'] = f"https://www.instagram.com/{instagram.group(1)}"
    
    return contact_info

def download_image(url, output_dir):
    """Download an image and save it preserving directory structure"""
    try:
        # Parse URL to get path
        parsed = urllib.parse.urlparse(url)
        if not parsed.netloc:
            # Relative URL
            url = 'https://www.funsnaps.ca' + url
        
        # Get path from URL
        path_parts = urllib.parse.urlparse(url).path.split('/')
        # Remove empty first element and 'wp-content'
        if 'wp-content' in path_parts:
            idx = path_parts.index('wp-content')
            rel_path = '/'.join(path_parts[idx:])
        else:
            rel_path = '/'.join([p for p in path_parts if p])
        
        if not rel_path:
            return False
        
        # Create output path
        output_path = Path(output_dir) / rel_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Download
        print(f"Downloading: {url}")
        urllib.request.urlretrieve(url, output_path)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    # Setup directories
    base_dir = Path('.')
    html_dir = Path('.')  # HTML files are in current directory
    assets_dir = base_dir / 'assets' / 'images'
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all HTML files
    html_files = list(html_dir.glob('*.html'))
    
    if not html_files:
        print("No HTML files found. Please download HTML files first.")
        return
    
    all_images = set()
    all_contact_info = defaultdict(set)
    
    # Process each HTML file
    for html_file in html_files:
        print(f"\nProcessing: {html_file.name}")
        
        # Extract images
        images = extract_images_from_html(html_file)
        all_images.update(images)
        print(f"Found {len(images)} images")
        
        # Extract contact info
        contact_info = extract_contact_info(html_file)
        for key, value in contact_info.items():
            if isinstance(value, list):
                all_contact_info[key].update(value)
            elif isinstance(value, dict):
                if key not in all_contact_info:
                    all_contact_info[key] = {}
                all_contact_info[key].update(value)
    
    # Convert sets to lists for JSON
    contact_json = {}
    for key, value in all_contact_info.items():
        if isinstance(value, set):
            contact_json[key] = list(value)
        elif isinstance(value, dict):
            contact_json[key] = value
    
    # Save contact info
    contact_file = base_dir / 'contact_info.json'
    with open(contact_file, 'w', encoding='utf-8') as f:
        json.dump(contact_json, f, indent=2)
    print(f"\nContact info saved to: {contact_file}")
    
    # Download all images
    print(f"\nDownloading {len(all_images)} images...")
    downloaded = 0
    for img_url in all_images:
        if download_image(img_url, assets_dir):
            downloaded += 1
    
    print(f"\nDownloaded {downloaded} images to {assets_dir}")
    
    # Save image list
    image_list_file = base_dir / 'image_urls.txt'
    with open(image_list_file, 'w', encoding='utf-8') as f:
        for img in sorted(all_images):
            f.write(img + '\n')
    print(f"Image URLs saved to: {image_list_file}")

if __name__ == '__main__':
    main()

