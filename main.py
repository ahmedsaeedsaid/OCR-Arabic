from sigmentation import *


pages_split=page_Segmentatin(img_clean)
for page in pages_split :
    columns=column_Segmentatin(page)
    for column in columns :
        lines=line_Segmentatin(column)
        threshold_word_sigmentation=calculate_threshold_word_sigmentation(lines)
        for line in lines :
            words=word_Segmentatin(line,threshold_word_sigmentation)
            for word in words :
                word_parts=sub_word_Segmentatin(word[0],word[1])



