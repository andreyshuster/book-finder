# Books Finder CLI

A Python CLI tool to search and download books from legal sources like Project Gutenberg and Open Library.

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make the script executable:
```bash
chmod +x books_finder.py
```

## Usage

### Search for books
```bash
# Search by title
python books_finder.py --title "Pride and Prejudice"

# Search by author
python books_finder.py --author "Jane Austen"

# Search by both title and author
python books_finder.py --title "Alice" --author "Lewis Carroll"

# Search only Project Gutenberg
python books_finder.py --title "Moby Dick" --source gutenberg

# Search only Open Library
python books_finder.py --author "Charles Dickens" --source openlibrary
```

### Download books
```bash
# Download by Project Gutenberg ID (after finding it via search)
python books_finder.py --download 1342
```

## Features

- Search Project Gutenberg's public domain books
- Search Open Library's catalog
- Download EPUB files from Project Gutenberg
- Simple command-line interface

## Sources

- **Project Gutenberg**: Public domain books with direct EPUB downloads
- **Open Library**: Comprehensive book catalog (search only)

Downloaded files are saved in the `downloads/` directory.