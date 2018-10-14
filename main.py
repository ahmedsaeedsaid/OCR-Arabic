from sigmentation import *


pages_split=page_Segmentatin(img_clean)
for page in pages_split :
    columns=column_Segmentatin(page)
    for column in columns :
        lines=line_Segmentatin(column)
        for line in lines :
            words=word_Segmentatin(line)
            for word in words :
                word_parts=part_Segmentatin(word[0],word[1])


