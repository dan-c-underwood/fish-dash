#!/usr/local/bin/python3
"""
Generates a fish docset for use in Dash (or similar documentation browsers).

It requires that the `copy.fish` script has already been run to make sure that
there is a local working copy of the documentation files. `beautifulsoup4` is
also required, this can be installed via `pip`.
"""
import os
import sqlite3
import re

from subprocess import call
from urllib.parse import quote
from bs4 import BeautifulSoup

# Docset path
destination = "fish.docset/Contents/Resources/Documents/"


def strip_extras(soup):
    """Strip sidebar, navbar from HTML tree and "fish: " from titles."""
    fish_left_bar = soup.find(class_="fish_left_bar")
    qindex = soup.find(class_="qindex")
    title = soup.title

    title.string = title.string.replace("fish: ", "")

    if fish_left_bar is not None:
        fish_left_bar.extract()

    if qindex is not None:
        qindex.extract()

    return soup


def modify_css(filename, dest):
    """Remove the spacing included in the CSS."""
    css_file = open(filename, 'r')
    out_css_file = open(dest, 'w')
    for line in css_file:
        line = line.replace("top: 3.6rem;", "top: 0;")
        line = line.replace("margin-left: 25rem;", "margin-left: 0;")
        out_css_file.write(line)


def generate_toc_tag(soup, entity, name):
    """Generate tag for the Dash table of contents."""
    new_name = "//apple_ref/cpp/{}/{}".format(entity, quote(name, safe=''))

    toc_tag = soup.new_tag("a", **{"class": "dashAnchor"})
    toc_tag['name'] = new_name

    return toc_tag


def process_html(filename, cursor):
    """Index, clean up, and add HTML file to docset."""
    fish_soup = BeautifulSoup(open("./docs/" + filename, 'r'),
                              'html.parser')

    # index.html contains introductory tutorial, index as Guide and Sections
    if filename == "index.html":
        cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path)"
                    "VALUES ('Tutorial', 'Guide', 'index.html');")

        for tag in fish_soup.find_all(class_="anchor"):
            name = tag.parent.text[1:]

            cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path)"
                        "VALUES (?, 'Section', ?);",
                        (name, filename + "#" + tag['id']))

            tag.append(generate_toc_tag(fish_soup, "Section", name))

    # commands.html is indexed as Commands (unsurprisingly...)
    elif filename == "commands.html":
        for tag in fish_soup.find_all(class_="anchor", id=re.compile("^\w+$")):
            name = tag["id"]
            toc_name = tag.parent.text[1:]

            cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path)"
                        "VALUES (?, 'Command', ?);",
                        (name, filename + "#" + name))

            tag.append(generate_toc_tag(fish_soup, "Command", toc_name))

    # tutorial.html and faq.html are indexed as Guides
    elif filename == "faq.html" or filename == "tutorial.html":
        for tag in fish_soup.find_all(id=re.compile("^[faq|tut]"),
                                      class_="anchor"):
            name = tag.parent.text[1:]

            cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path)"
                        "VALUES (?, 'Guide', ?);",
                        (name, filename + "#" + tag['id']))

            tag.append(generate_toc_tag(fish_soup, "Section", name))

    with open(destination + doc_file, 'w') as output:
        output.write(str(strip_extras(fish_soup)))

# Create directory structure
call(["mkdir", "-p", destination])

# Copy Info.plist into the docset
call(["cp", "Info.plist", "fish.docset/Contents/Info.plist"])

# If an icon has been generated, copy it into the docset
if os.path.isfile("icon.png"):
    call(["cp", "icon.png", "fish.docset/icon.png"])

# Setup the sqlist instance
db = sqlite3.connect('fish.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try:
    cur.execute('DROP TABLE searchIndex;')
except:
    pass

# Generate index table
cur.execute("CREATE TABLE searchIndex(id INTEGER PRIMARY KEY,"
            "name TEXT, type TEXT, path TEXT);")
cur.execute("CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);")

# Process each file for the docset
for doc_file in os.listdir(os.getcwd() + "/docs"):

    if doc_file.endswith(".css"):
        # Fix the CSS for the Dash format
        modify_css("./docs/" + doc_file, destination + doc_file)

    elif doc_file.endswith(".png"):
        # Only image used is in the sidebar - saves space!
        pass

    elif doc_file.endswith(".html"):
        # Process HTML files by indexing and stripping unneeded sections
        if doc_file != "license.html" and doc_file != "design.html":
            process_html(doc_file, cur)


# Save database changes
db.commit()
db.close()
