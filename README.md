Research Paper Extraction from PubMed

Overview

This project extracts research papers from PubMed using the Entrez API and filters out authors affiliated with non-academic institutions. The extracted details are then saved into a CSV file.

Features

Searches PubMed using a user-defined query

Fetches paper details (Title, Authors, Publication Date, etc.)

Filters non-academic authors based on affiliation

Saves results in CSV format

Installation

Prerequisites

Ensure you have Python installed (>=3.7).

Setup

Install dependencies:

pip install -r requirements.txt

Usage

Run the script using:

python research.py "your search query" -f output.csv

Optional Arguments:

-d : Enable debug mode

-f FILE : Specify output CSV filename

Example:

python research.py "Artificial Intelligence in Medicine" -f results.csv

Output

The script generates a CSV file with the following columns:

PubmedID

Title

Publication Date

Non-academic Author(s)

Company Affiliation(s)

Corresponding Author Email

Testing

Run tests to validate correct filtering of non-academic affiliations.

pytest test_script.py

Challenges & Future Improvements

Handling API rate limits

Improving accuracy of non-academic affiliation filtering

Expanding metadata extraction

License

MIT License

Author

Harsha

