# fish-dash

Following an update to the Fish documentation format, this repository is now archived. You can find a new Fish docset generator at: https://github.com/schrodincat/dash-fish

Tools to allow for the generation of a [Dash](https://kapeli.com/dash) docset for the [fish shell](http://fishshell.com). This docset can be imported into Dash, [Zeal](http://zealdocs.org), or any similar offline documentation browser.

## Requirements

* `fish`: required for running the copy script ;
* `convert`: part of ImageMagick ;
* `python3`: `build.py` script only supported under Python 3 ;
* `BeautifulSoup` - for parsing the HTML files.

### MacOS

This homebrew distribution of `fish` also contains a local copy of the docs which removes the need to pull them from the fishshell website.
 
    brew install fish imagemagick
    python3 -m venv .env 
    . .env/bin/activate
    pip install beautifulsoup4

### Linux

Be sure to have [`fish`](https://github.com/fish-shell/fish-shell) installed.

    apt-get install python3 imagemagick    
    python3 -m venv .env
    . .env/bin/activate
    pip install BeautifulSoup4

## Install

    git clone git@github.com:dan-c-underwood/fish-dash.git

## Usage

To generate the docset, run the command:

```
$ make
```

The docset is then generated and placed in the top level directory.

Cleaning up the generated files can be performed using:

```
$ make clean
```
