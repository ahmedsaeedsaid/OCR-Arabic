from segmentation import *


pages_split=page_segmentation(img_clean)
words_parts=[]
for page in pages_split :
    columns=column_segmentation(page)
    for column in columns :
        lines=line_segmentation(column)
        threshold_word_sigmentation=calculate_threshold_word_sigmentation(lines)
        for line in lines :
            words,baseline=word_segmentation(line)
            for word in words :
                word_parts=sub_word_segmentation(word[0],word[1])
                words_parts.append(word_parts)
            print(mean_pens(words_parts))






