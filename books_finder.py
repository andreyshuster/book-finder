#!/usr/bin/env python3
import argparse
import requests
import sys
import os
from urllib.parse import quote
import json

def search_project_gutenberg(title=None, author=None):
    """Search Project Gutenberg for books by title and/or author"""
    params = []
    if title:
        params.append(f"search={quote(title.lower())}")
    if author:
        params.append(f"search={quote(author.lower())}")
    
    if not params:
        return []
    
    url = f"https://gutendex.com/books/?{'&'.join(params)}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.RequestException as e:
        print(f"Error searching Project Gutenberg: {e}")
        return []

def search_open_library(title=None, author=None):
    """Search Open Library for books by title and/or author"""
    params = []
    if title:
        params.append(f"title={quote(title.lower())}")
    if author:
        params.append(f"author={quote(author.lower())}")
    
    if not params:
        return []
    
    url = f"https://openlibrary.org/search.json?{'&'.join(params)}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('docs', [])
    except requests.RequestException as e:
        print(f"Error searching Open Library: {e}")
        return []

def download_epub(url, filename):
    """Download EPUB file from URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        os.makedirs('downloads', exist_ok=True)
        filepath = os.path.join('downloads', filename)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded: {filepath}")
        return filepath
    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        return None

def display_gutenberg_results(books):
    """Display Project Gutenberg search results"""
    if not books:
        print("No books found on Project Gutenberg")
        return
    
    print(f"\nProject Gutenberg Results ({len(books)} found):")
    print("-" * 50)
    
    for i, book in enumerate(books[:10], 1):
        title = book.get('title', 'Unknown Title')
        authors = ', '.join([author['name'] for author in book.get('authors', [])])
        book_id = book.get('id')
        
        print(f"{i}. {title}")
        if authors:
            print(f"   Author(s): {authors}")
        print(f"   ID: {book_id}")
        
        formats = book.get('formats', {})
        if 'application/epub+zip' in formats:
            print(f"   EPUB available: Yes")
        else:
            print(f"   EPUB available: No")
        print()

def display_openlibrary_results(books):
    """Display Open Library search results"""
    if not books:
        print("No books found on Open Library")
        return
    
    print(f"\nOpen Library Results ({len(books)} found):")
    print("-" * 50)
    
    for i, book in enumerate(books[:10], 1):
        title = book.get('title', 'Unknown Title')
        authors = ', '.join(book.get('author_name', []))
        first_publish_year = book.get('first_publish_year', 'Unknown')
        
        print(f"{i}. {title}")
        if authors:
            print(f"   Author(s): {authors}")
        print(f"   First published: {first_publish_year}")
        print()

def get_book_info(book_id):
    """Get book information from Project Gutenberg API"""
    try:
        response = requests.get(f"https://gutendex.com/books/{book_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

def sanitize_filename(text):
    """Remove invalid characters from filename"""
    import re
    return re.sub(r'[<>:"/\\|?*]', '', text).strip()

def download_from_gutenberg(book_id):
    """Download EPUB from Project Gutenberg by book ID"""
    book_info = get_book_info(book_id)
    
    if book_info:
        title = book_info.get('title', 'Unknown Title')
        authors = book_info.get('authors', [])
        author_name = authors[0]['name'] if authors else 'Unknown Author'
        
        # Create filename: Author - Title.epub
        safe_author = sanitize_filename(author_name)
        safe_title = sanitize_filename(title)
        filename = f"{safe_author} - {safe_title}.epub"
    else:
        filename = f"gutenberg_{book_id}.epub"
    
    url = f"https://www.gutenberg.org/ebooks/{book_id}.epub.noimages"
    return download_epub(url, filename)

def main():
    parser = argparse.ArgumentParser(description='Search and download books from legal sources')
    parser.add_argument('--title', '-t', help='Book title to search for')
    parser.add_argument('--author', '-a', help='Author name to search for')
    parser.add_argument('--source', choices=['gutenberg', 'openlibrary', 'all'], 
                       default='all', help='Source to search (default: all)')
    parser.add_argument('--download', type=int, metavar='ID', 
                       help='Download book by Project Gutenberg ID')
    
    args = parser.parse_args()
    
    if args.download:
        download_from_gutenberg(args.download)
        return
    
    if not args.title and not args.author:
        parser.error("Must specify either --title or --author (or both)")
    
    if args.source in ['gutenberg', 'all']:
        gutenberg_books = search_project_gutenberg(args.title, args.author)
        display_gutenberg_results(gutenberg_books)
    
    if args.source in ['openlibrary', 'all']:
        openlibrary_books = search_open_library(args.title, args.author)
        display_openlibrary_results(openlibrary_books)
    
    print("\nTo download a book from Project Gutenberg, use: python books_finder.py --download <ID>")

if __name__ == "__main__":
    main()