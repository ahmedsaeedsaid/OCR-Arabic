from segmentation import *

img_clean=pre_processing('test_image/test_13.jpg')
pages_split=page_segmentation(img_clean)
words_parts=[]
for page in pages_split :
    columns=column_segmentation(page)
    for column in columns :
        lines=line_segmentation(column)
        for line in lines :
            words,baseline=word_segmentation(line)
            for word in words :
                word_parts=sub_word_segmentation(word[0],word[1])
                words_parts.append(word_parts)

            pen=mean_pens(words_parts)
            for word_parts in words_parts:
                for part in word_parts:
                    chars=char_segmentation(part[0],part[1],pen,baseline)
