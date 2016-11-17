#add column 1 and 2 (start is 1) in a textfile, starting from the 2nd row
#awk '!(NR%2){print $1+$2}' infile
