#!/bin/bash

set -e  # Exit on first error
set -x  # Echo invoked commands

# Usage: inject_html target_file contents_file
inject_html() {
    TARGET="$1"
    CONTENTS="$2"

    # Check if target file exists before processing
    if [ ! -f "${TARGET}" ]; then
        echo "Skipping ${TARGET} (file does not exist)"
        return 0
    fi

    echo "inject_html invoked: ${TARGET} ${CONTENTS}"

    JSFILE=$(echo "$CONTENTS" | sed -e 's/[.]html$/.js/')
    echo "Creating ${JSFILE}"

    # https://stackoverflow.com/questions/7189604/replacing-html-tag-content-using-sed
    # https://stackoverflow.com/questions/8988855/include-another-html-file-in-a-html-file
    echo "document.write('\\" > "${JSFILE}"
    sed 's/\\/\\\\/g;s/^.*$/&\\/g;s/'\''/\\'\''/g' "${CONTENTS}" >> "${JSFILE}"
    echo "');" >> "${JSFILE}"
    sudo cp -f "${JSFILE}" build_output/public/

    # The <footer> tag seems a reasonable place in the thumbsup output
    sed -i -e 's|<footer>|<script src="public/'"${JSFILE}"'"></script>\n      <footer>|' "${TARGET}"
}

# Prove we can access build_output/index.html
echo "Starting line count of index.html: $(wc -l build_output/index.html)"

inject_html "build_output/index.html" "desc_index.html"

# Copy the JavaScript file for moving thumbnails
sudo cp -f move_thumbs.js build_output/public/

# Copy the logo
sudo cp -f logo.png build_output/public/

# Copy the favicons (favicon.ico also at the site root, where browsers look by default)
sudo cp -f favicon-32x32.png favicon-512.png apple-touch-icon.png favicon.ico build_output/public/
sudo cp -f favicon.ico build_output/

# Inject the logo into the header (before the h1)
sed -i -e 's|<header>|<header>\n      <img src="public/logo.png" alt="Rock Haven Property logo" class="rh-logo">|' "build_output/index.html"

# Inject favicon into all HTML files
for html_file in build_output/*.html; do
  if [ -f "$html_file" ]; then
    sed -i -e 's|<head>|<head>\n    <link rel="icon" href="public/favicon.ico" sizes="any">\n    <link rel="icon" type="image/png" sizes="32x32" href="public/favicon-32x32.png">\n    <link rel="icon" type="image/png" sizes="512x512" href="public/favicon-512.png">\n    <link rel="apple-touch-icon" href="public/apple-touch-icon.png">|' "$html_file"
  fi
done

# Inject a small GitHub logo linking to the source repo into the footer of all HTML files
GITHUB_LINK='<a class="rh-github" href="https://github.com/technical-rockhaven-llc/www.rockhaven.llc" target="_blank" rel="noopener" aria-label="Source code on GitHub" title="Source code on GitHub"><svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.06-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg></a>'
for html_file in build_output/*.html; do
  if [ -f "$html_file" ]; then
    sed -i -e 's|</footer>|  '"${GITHUB_LINK}"'\n      </footer>|' "$html_file"
  fi
done

# Inject the script tag into index.html
sed -i -e 's|<footer>|<script src="public/move_thumbs.js"></script>\n      <footer>|' "build_output/index.html"
inject_html "build_output/Unit-2B.html" "desc_u2b.html"

# Contents of build_output
ls -la build_output/
