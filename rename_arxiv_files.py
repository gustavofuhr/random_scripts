import os
import re
import argparse

import feedparser


def get_arxiv_number(s):
    p = re.compile(r"(\d{4}.\d{5})(v\d)?\.pdf")
    result = p.search(s)
    if result is not None:
        return result.group(1)
    return None

def fetch_paper_details_arxiv(arxiv_number):
    url = f"http://export.arxiv.org/api/query?id_list={arxiv_number}&max_results=1"
    d = feedparser.parse(url)
    return d
    
def sanitize_title(title):
    return title.replace(":", ",").replace("/", "-")

def rename_arxiv_files(root_path, include_updated_year = False, dry_run = False):
    arxiv_files = {}
    pdf_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(root_path) \
               for f in filenames if os.path.splitext(f)[1].lower() == '.pdf']
    for f_path in pdf_files:
        filename = os.path.basename(f_path)
        arxiv_no = get_arxiv_number(filename)
        if arxiv_no is not None:
            if arxiv_no in arxiv_files.keys():
                print(f"GOT SAME FILE TWICE: {arxiv_files[arxiv_no]} and {f_path}")

            arxiv_files[arxiv_no] = f_path
            
            arxiv_d = fetch_paper_details_arxiv(arxiv_no)
            
            if "entries" in arxiv_d.keys() and len(arxiv_d["entries"]) > 0:
                arxiv_title = arxiv_d["entries"][0]["title"]
                if include_updated_year:
                    # extract year from string like '2024-01-05T13:16:25Z'
                    year_arxiv_updated = arxiv_d["entries"][0]["updated"][:4]
                    new_filename = f"{arxiv_no} - {year_arxiv_updated} - {sanitize_title(arxiv_title)}.pdf"
                else:
                    new_filename = f"{arxiv_no} - {sanitize_title(arxiv_title)}.pdf"
                new_filepath = f_path.replace(filename, new_filename)
                cmd = f'mv "{f_path}" "{new_filepath}"'
                print(cmd)
                if not dry_run:
                    os.rename(f_path, new_filepath)



if __name__ == "__main__":
    parse = argparse.ArgumentParser("Rename arxiv PDF files recursively.")
    parse.add_argument("root_path", type=str, help="Path to the PDF folder.")
    parse.add_argument("--dry-run", action="store_true", help="Just show which files will rename and to what.")
    parse.add_argument("--include-year", action="store_true", help="Includes in the file name the year of last update.")

    args = parse.parse_args()
    rename_arxiv_files(args.root_path, args.include_year, args.dry_run)