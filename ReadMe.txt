This python program allows you to download Cyanide and Happiness Comics from explosm.net/comics/archive.

Follow these steps:

1) Open the input.txt file (placed in the current directory) and edit it according to the format:

'''
start_month start_year
end_month end_year
authorname1 authorname2 ... authornameN
'''

Write only the first names of the authors. This will download all the comics by all the authors in the duration (start_month, start_year) to (end_month, end_year) [including both months].

Year format: XYZW (e.g. 2013)
Month format: Complete name of month and first letter capitalised

2) Open the Command Prompt in the current directory and run the "scraping.py" file using python.

python scraping.py

This should download the comics!

Note: The comics are downloaded in the directory: current_directory\\Year\\Month\\"Date_Written-Author_Name.png".
The directories are created by the program if they do not exist.






    