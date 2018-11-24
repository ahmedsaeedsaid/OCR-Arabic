'''
Page Sigmentation
ﬁnd the number of columns that the page consists of and extract them as individual pieces
this algorithm that applying vertical projection to the image results from pre-processing stage

Separation regions where the vertical projection equals to zero.

The separation will be applied according to these areas
if the length of the separation area greater than a certain threshold value
determined experimentally

The separation is done by determining the min and max column indices for each column region


Column Sigmentation
Horizontal projection is applied to the column image
continuous indices where the projection equals to zero is determined and grouped
Each group performs a separation region between the segments

'''
from sigmentation_helps import *

def page_Segmentatin(img):

    #vertical projection is applied
    V_proj=vertical_projection(img)

    # get separation region indices and separated regions
    Separation_indices=Separation_indices_f(V_proj)

    # calculate page sigmentation
    threshold_page_sigmentation=50

    if(len(Separation_indices)>0):
        separated_regions=separated_regions_f(Separation_indices,threshold_page_sigmentation)
        page_columns=[]
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            page_columns.append(img[: , min:max+2])
            #cv2.imwrite('result_image/page_segmanted'+str(i)+'.jpg',img[: , min:max+2])

    else:
        page_columns=[img]
    return page_columns

def column_Segmentatin(img):
    #horizontal projection is applied
    H_proj=horizontal_projection(img)
    # get separation region indices and separated regions
    Separation_indices=Separation_indices_f(H_proj)

    # calculate column threshold
    count_spaces=np.array(count_spaces_connected(H_proj))
    if len(Separation_indices) >0:
        if len(count_spaces) >0:
            threshold_column_sigmentation=round(float(np.mean(count_spaces)))
        else :
            threshold_column_sigmentation=1
        separated_regions=separated_regions_f(Separation_indices,threshold_column_sigmentation)
        column_splets=[]
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            column_splets.append(img[min:max+2 , :])
            cv2.imwrite('result_image/column_segmanted'+str(i)+'.jpg',img[min:max+2,:])
    else:
        column_splets=[img]
    return column_splets

def height_of_line_Segmentatin(img):

    img = Clear_increases_in_line(img)

    line_image=column_Segmentatin(img)[0]

    # get height of line
    height_line=line_image.shape[0]
    return height_line

def line_Segmentatin (img) :

    # get height of one line
    height_line=height_of_line_Segmentatin(np.copy(img))

    # calculate numbers of lines
    number_of_line = int(img.shape[0]/height_line)
    height_line = int(img.shape[0]/number_of_line)

    if number_of_line == 0 or number_of_line == 1 :
        return [img]

    # split image to lines
    lines_splets = []
    start = 0
    for i in range(number_of_line):
        if img.shape[0]>=height_line+start :
            lines_splets.append(img[start:height_line+start , :])
            #cv2.imwrite('result_image/line_segmanted'+str(i)+'.jpg',img[start:height_line+start , :])
            start+=height_line
    return lines_splets

def word_Segmentatin (img,threshold_word_sigmentation) :

    #remove under line from image
    img = remove_underline(img)
    cv2.imwrite('result_image/test.jpg',img)
    # clear increases in line
    upgrade_image = Clear_increases_in_line(img)



    # vertical projection is applied
    V_proj=vertical_projection(upgrade_image)

    # get separation region indices and separated regions
    Separation_indices=Separation_indices_f(V_proj)

    # split image to words
    if(len(Separation_indices)>0):
        #threshold_word_sigmentation=round(pen_size(upgrade_image,Separation_indices)+2)
        separated_regions=separated_regions_f(Separation_indices,threshold_word_sigmentation)
        line_words=[]
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            cv2.imwrite('result_image/word_segmanted'+str(i)+'.jpg',upgrade_image[: , min:max+2])
            line_words.append((img[: , min:max+2],upgrade_image[: , min:max+2]))
    else:
        line_words=[(img,upgrade_image)]
    return line_words

def sub_word_Segmentatin(img,upgrade_img):
    number_of_sub_words, labels = cv2.connectedComponents(upgrade_img,connectivity=8)
    diacritics_img=np.copy(img)
    parts=[]
    parts_dir=[]
    sub_words=[]

    # create empty image to save sub-word without director and doted
    for i in range(1,number_of_sub_words):
        parts.append(np.zeros(upgrade_img.shape))

    # seperate sub-word in var 'parts' without director and doted and create diacritics image
    for i in np.arange(labels.shape[0]):
        for j in np.arange(labels.shape[1]):
            if diacritics_img.item(i,j)==upgrade_img.item(i,j):
                diacritics_img[i][j]=0
            for k in range(1,number_of_sub_words):
                if labels.item(i,j)==k:
                    parts[k-1][i][j]=255

    # create image to save sub-word with director and doted
    for k in range(1,number_of_sub_words):
        parts_dir.append(np.copy(parts[k-1]))


    # calculate rate for each diacritic
    number_of_diacritic, labels_of_diacritics = cv2.connectedComponents(diacritics_img,connectivity=8)
    V_proj_sub_words=[]
    diacrtics=[]
    for part in parts:
        V_proj_sub_words.append(vertical_projection(part))

    for i in range(1,number_of_diacritic):
        diacrtics.append([])
        for j in range(len(parts)):
            diacrtics[i-1].append(0)

    for i in np.arange(labels_of_diacritics.shape[0]):
        for j in np.arange(labels_of_diacritics.shape[1]):
            if labels_of_diacritics.item(i,j)!=0:
                for k in range(len(V_proj_sub_words)):
                    if V_proj_sub_words[k][j]!=0:
                        diacrtics[labels_of_diacritics.item(i,j)-1][k]+=1

    # get part of maximum rate
    for i in range(len(diacrtics)):
        diacrtics[i]=diacrtics[i].index(max(diacrtics[i]))

    # add diacritics to parts
    for i in np.arange(labels_of_diacritics.shape[0]):
        for j in np.arange(labels_of_diacritics.shape[1]):
            if labels_of_diacritics.item(i,j)!=0:
                parts_dir[diacrtics[labels_of_diacritics.item(i,j)-1]][i][j]=255



    # seperate sub-word in var 'parts_dir' with director and doted
    for i in range(1,number_of_sub_words):
        V_proj=vertical_projection(parts_dir[i-1])
        Separation_indices=Separation_indices_f(V_proj)
        if(len(Separation_indices)>0):
            separated_regions=separated_regions_f(Separation_indices,1)
            sub_words.append((parts_dir[i-1][:,separated_regions[0][0]:separated_regions[0][1]+2],parts[i-1][:,separated_regions[0][0]:separated_regions[0][1]+2]))

    #for i in range(1,number_of_sub_words):
        #cv2.imwrite('result_image/part'+str(i)+'.jpg',sub_words[i-1][0])
    return sub_words
