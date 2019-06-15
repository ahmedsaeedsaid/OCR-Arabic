from text_combine import *
#from segmentation import *
def aocr(url,loaded_model):

    all_chars = []
    charCount=0
    allwordchars=[]
    alllines=[]
    linechars=0
    allwordsparts=[]
    allwordspartslens=[]
    index=0
    img_clean=pre_processing (url)

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
                    allwordsparts.append(len(word_parts))
                pen=mean_pens(words_parts)

                for word_parts in words_parts:

                    for part in word_parts:

                        index+=1
                        chars=char_segmentation(part[0],part[1],pen,baseline,index)
                        charCount=charCount+len(chars)
                        linechars = linechars+len(chars)
                        allwordspartslens.append(len(chars))
                        for char in chars:
                            all_chars.append(char[0])
                    allwordchars.append((charCount))
                    charCount=0


    i=0
    for char in all_chars :
        cv2.imwrite('result_image/char_'+str(i)+'.jpg',char)
        i+=1
    # pattern stage
    text = combine_text(allwordchars,all_chars,alllines,allwordsparts,allwordspartslens,loaded_model)
    return text






