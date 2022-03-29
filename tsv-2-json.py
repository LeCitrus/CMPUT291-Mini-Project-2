from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)

def tsv2json(input_file,output_file):

    
    arr = [] 
    file = open(input_file, 'r') 
    a = file.readline()
      
    # The first line consist of headings of the record 
    # so we will store it in an array and move to 
    # next line in input_file.
    titles = [t.strip() for t in a.split('\t')]
    for line in file:
        d = {}
        for t, f in zip(titles, line.split('\t')):
            
            # Convert each row into dictionary with keys as titles
            d[t] = f.strip()

            # Nested Arrays
            if t == "primaryProfession":
                d[t] = f.strip().split(',')
             
            if t == "knownForTitles":
                    d[t] = f.strip().split(',')
             
            if t == "genres":
                    d[t] = f.strip().split(',')
          
            if t == "characters":
                    d[t] = f.strip().split(',')
                   
        # we will use strip to remove '\n'.n
        arr.append(d)
     
        # we will append all the individual dictionaires into list 
        # and dump into file.
    with open(output_file, 'w', encoding='utf-8') as output_file:
        output_file.write(json.dumps(arr, indent=4))
       
  
# Driver Code
location = input('Please enter the directory of the tsv and json files: ')

files_in = [location + '/name.basics.tsv', 
location+'/title.basics.tsv',
location+'/title.principals.tsv',
location+'/title.ratings.tsv']

files_out = [location+'/name.basics.json', 
location+'/title.basics.json',
location+'/title.principals.json',
location+'/title.ratings.json']

for i in range(0,4):
    input_filename = files_in[i]
    output_filename = files_out[i]
    tsv2json(input_filename,output_filename)



