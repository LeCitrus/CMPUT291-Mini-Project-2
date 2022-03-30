import json
import os


def tsv2json(input_file, output_file):
    arr = [] 
    file = open(input_file, 'r') 
    title_line = file.readline()

    # The first line consist of headings of the record, so we will store it in an array and move to next line in input_file.
    titles = [title.strip() for title in title_line.split('\t')]

    for line in file:
        row = {}

        for key, value in zip(titles, line.split('\t')):

            # Convert each row into dictionary with keys as titles
            # Nested Arrays
            if key in ("primaryProfession", "knownForTitles", "genres", "characters"):
                if key in ("primaryProfession", "knownForTitles", "genres"):
                    row[key] = value.strip(' \n').split(',')

                else:
                    row[key] = value.strip('\n "[]').split('","')

                if row[key][0] == '\\N':
                    row[key] = None

            # NULL values
            elif value == '\\N':
                row[key] = None 
            else:
                row[key] = value.strip()

        # We will use strip to remove '\n'.n
        
        arr.append(row)

    # We will append all the individual dictionaries into list and dump into file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr))
           
        

# Driver Code
def main():
    # Get current directory
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Prepare filenames for input and output
    files_in = [dir_path + '/name.basics.tsv', 
    dir_path + '/title.basics.tsv',
    dir_path + '/title.principals.tsv',
    dir_path + '/title.ratings.tsv']

    files_out = [dir_path + '/name.basics.json', 
    dir_path + '/title.basics.json',
    dir_path + '/title.principals.json',
    dir_path + '/title.ratings.json']

    for i in range(4):
        
        input_filename = files_in[i]
        output_filename = files_out[i]
        print("Converting", input_filename, "to JSON...")
        tsv2json(input_filename, output_filename)

    print("Done!")
if __name__ == "__main__":
    main()
