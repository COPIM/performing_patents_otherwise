# import required modules
import os
from striprtf.striprtf import rtf_to_text

# assign directory
directory = 'data/POP_Dataset_2022'
total = 0

# iterate over files in
# that directory
for root, dirs, files in os.walk(directory):
    for filename in files:
        if '.rtf' in filename:
            file = os.path.join(root, filename)
            file = open(file, "rt")
            content = file.read()
            #text = rtf_to_text(content)
            words = content.split()
            total += len(words)
            #print(text)

print(total)
