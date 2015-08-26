# fish-dash

Tools to allow for the generation of a [Dash](https://kapeli.com/dash) docset for the [fish shell](http://fishshell.com). This docset can be imported into Dash, [Zeal](http://zealdocs.org), or any similar offline documentation browser.

## Dependencies

These tools require the following to be installed:

* `fish` - required for running the copy script. On OS X this can be installled with `brew install fish`, this homebrew distribution also contains a local copy of the docs which removes the need to pull them from the fishshell website.
* `convert` - command line tool for ImageMagick, installable on OS X via `brew install imagemagick`
* `python3` - the `build.py` script is only supported under Python 3, it may work under Python 2 but this is not a guarantee! On OS X you can use homebrew to install it via `brew install python3`.
* `BeautifulSoup` - for parsing the HTML files. Installable via `pip install beautifulsoup4`.

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
