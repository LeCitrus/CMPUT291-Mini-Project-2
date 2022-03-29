import json

def tsv2json(input_file, output_file):

    
    arr = [] 
    file = open(input_file, 'r') 
    title_line = file.readline()
      
    # The first line consist of headings of the record 
    # so we will store it in an array and move to 
    # next line in input_file.
    titles = [title.strip() for title in title_line.split('\t')]
    for line in file:
        row = {}
        for key, value in zip(titles, line.split('\t')):
            
            # Convert each row into dictionary with keys as titles
            row[key] = value.strip()

            # Nested Arrays
            if key in ("primaryProfession", "knownForTitles", "genres", "characters"):
                row[key] = value.strip().split(',')

                   
        # We will use strip to remove '\n'.n
        arr.append(row)
     
        # We will append all the individual dictionaries into list and dump into file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))
       
  
# Driver Code
location = input('Please enter the directory of the tsv and json files: ')

files_in = [location + '/name.basics.tsv', 
location + '/title.basics.tsv',
location + '/title.principals.tsv',
location + '/title.ratings.tsv']

files_out = [location+'/name.basics.json', 
location + '/title.basics.json',
location + '/title.principals.json',
location + '/title.ratings.json']

for i in range(0, 4):
    input_filename = files_in[i]
    output_filename = files_out[i]
    tsv2json(input_filename,output_filename)



