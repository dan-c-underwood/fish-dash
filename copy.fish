#!/usr/local/bin/fish

# Create directory for local working copy of docs
if test ! -d ./docs
    mkdir ./docs
end

if test -f $__fish_help_dir/index.html
    # If the docs are available locally then just copy them across
    cp $__fish_help_dir/* ./docs
    # Grab the logo to iconify
    wget -O logo.png http://fishshell.com/assets/img/Terminal_Logo_CRT_Small.png
else
    # Grab the version of the docs currently installed
    set -l version_num (echo $FISH_VERSION| cut -d . -f 1,2)
    wget -p -rl 1 http://fishshell.com/docs/$version_num/index.html
    # Copy the logo to iconify
    cp ./fishshell.com/assets/img/Terminal_Logo_CRT_Small.png ./logo.png
    # Copy across the docs themselves
    cp ./fishshell.com/docs/$version_num/* ./docs
    rm -rf ./fishshell.com
end

if type -q convert
    # Turns the logo from the website to a 32x32 icon for the docset
    convert logo.png -gravity center -crop 75% -resize 32x32 icon.png
else
    echo "Install ImageMagick to generate icon"
end
