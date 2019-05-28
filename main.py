from text_combine import *



all_chars = []
charCount=0
allwordchars=[]
alllines=[]
linechars=0
img_clean=pre_processing('test_image/test_13.jpg')

# preprocessing stage
pages_split=page_segmentation(img_clean)

# segmentation stage
words_parts=[]
for page in pages_split :
    columns=column_segmentation(page)
    for column in columns :
        lines=line_segmentation(column)
        for line in lines :
            alllines.append(linechars)
            linechars=0
            words,baseline=word_segmentation(line)
            for word in words :
                word_parts=sub_word_segmentation(word[0],word[1])
                words_parts.append(word_parts)

            pen=mean_pens(words_parts)
            for word_parts in words_parts:
                allwordchars.append(charCount)
                charCount=0
                for part in word_parts:
                    chars=char_segmentation(part[0],part[1],pen,baseline)
                    charCount=charCount+len(chars)
                    linechars = linechars+len(chars)
                    for char in chars:
                        all_chars.append(char[0])

# pattern stage
combine_text(allwordchars,all_chars,alllines)





