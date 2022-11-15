# Twitter Archive Site Generator

Lots of people are downloading their Twitter-Archives right now and @timhutton created a parser to retrieve the original links and generate Markdown files from it.
I used extended this now by converting the output of @timhutton's parser back into a webpage using the MkDocs-Material framework.

## Requirements

- Twitter-Archive download
- Output from [timhutton's parser](https://github.com/timhutton/twitter-archive-parser)
- Python3

## Usage

- Download the site-generator.py and the requirements.txt
- _optional_: Create a new Python3-Virtual-Environment
- run the following commands from a terminal in the folder with the Markdown output:
  
    ```sh
    pip install -Ur requirements.txt
    python3 site-generator.py
    mkdocs build --strict
    ```
