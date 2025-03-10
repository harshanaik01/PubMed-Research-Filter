import argparse
import csv
import re
from Bio import Entrez

# Set up Entrez
Entrez.email = "harshanaik8951@gmail.com"  


def search_pubmed(query):
    """Searches PubMed for articles matching the query."""
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=10)
        record = Entrez.read(handle)
        handle.close()
        return record.get("IdList", [])
    except Exception as e:
        print(f"Error searching PubMed: {e}")
        return []


def fetch_paper_details(pubmed_ids):
    """Fetches paper details for given PubMed IDs."""
    papers = []
    try:
        handle = Entrez.efetch(db="pubmed", id=",".join(pubmed_ids), rettype="xml", retmode="xml")
        records = Entrez.read(handle)
        handle.close()
    except Exception as e:
        print(f"Error fetching PubMed details: {e}")
        return []

    for article in records.get("PubmedArticle", []):
        try:
            medline = article.get("MedlineCitation", {})
            article_data = medline.get("Article", {})

            pubmed_id = medline.get("PMID", "N/A")
            title = article_data.get("ArticleTitle", "N/A")
            pub_date = article_data.get("Journal", {}).get("JournalIssue", {}).get("PubDate", {}).get("Year", "N/A")
            authors = article_data.get("AuthorList", [])

            # Extract company-affiliated authors
            non_academic_authors = []
            company_affiliations = []
            corresponding_author_email = "N/A"

            for author in authors:
                if "AffiliationInfo" in author:
                    for aff in author.get("AffiliationInfo", []):
                        affiliation = aff.get("Affiliation", "")
                        if affiliation:
                            if not re.search(r"\b(university|college|institute|school|hospital|center)\b", affiliation, re.IGNORECASE):
                                non_academic_authors.append(f"{author.get('ForeName', '')} {author.get('LastName', '')}")
                                company_affiliations.append(affiliation)
                            if "@" in affiliation:
                                corresponding_author_email = affiliation

            # Append result
            papers.append([
                pubmed_id, title, pub_date,
                "; ".join(non_academic_authors) if non_academic_authors else "N/A",
                "; ".join(company_affiliations) if company_affiliations else "N/A",
                corresponding_author_email
            ])

        except Exception as e:
            print(f"Error processing article: {e}")

    return papers


def save_to_csv(papers, filename):
    """Saves results to a CSV file."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
            writer.writerows(papers)
        print(f"Results saved to {filename}")
    except Exception as e:
        print(f"Error saving CSV: {e}")


def main():
    """Main function to execute the script."""
    parser = argparse.ArgumentParser(description="Fetch research papers with company-affiliated authors from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Output filename (CSV).")

    args = parser.parse_args()

    if args.debug:
        print(f"Searching PubMed for: {args.query}")

    pubmed_ids = search_pubmed(args.query)

    if args.debug:
        print(f"Found {len(pubmed_ids)} papers.")

    if not pubmed_ids:
        print("No papers found. Exiting.")
        return

    papers = fetch_paper_details(pubmed_ids)

    if args.debug:
        print(f"Processed {len(papers)} papers.")

    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(paper)


if __name__ == "__main__":
    main()