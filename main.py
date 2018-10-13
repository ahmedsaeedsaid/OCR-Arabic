from sigmentation import *


pages_split=page_Segmentatin(img_clean)
for page in pages_split :
    columns=column_Segmentatin(page)
    for column in columns :
        lines=line_Segmentatin(column)
        for line in lines :
            word_Segmentatin(line)
