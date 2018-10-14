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


Line Sigmentation


'''
from sigmentation_helps import *
import matplotlib.pyplot as plt



def page_Segmentatin(img):

    #vertical projection is applied
    V_proj=vertical_projection(img)
    # get separation region indices and separated regions

    Separation_indices=Separation_indices_f(V_proj)

    # calculate page threshold
    count_spaces=np.array(count_spaces_conected(V_proj))
    if len(count_spaces)>0:
        threshold_page_sigmentation=np.mean(count_spaces)
    else:
        threshold_page_sigmentation=1

    if(len(Separation_indices)>0):
        separated_regions=separated_regions_f(Separation_indices,threshold_page_sigmentation)
        page_columns=[]
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            page_columns.append(img[: , min:max])
            #cv2.imwrite('result_image/page_segmanted'+str(i)+'.jpg',img[: , min:max])

    else:
        page_columns=[img]
    return page_columns





def column_Segmentatin(img):
    #horizontal projection is applied
    H_proj=horizontal_projection(img)
    # get separation region indices and separated regions
    Separation_indices=Separation_indices_f(H_proj)

    # calculate column threshold
    count_spaces=np.array(count_spaces_conected(H_proj))
    if len(count_spaces)>0:
        threshold_column_sigmentation=np.min(count_spaces)*5
    else:
        threshold_column_sigmentation=1
    if(len(Separation_indices)>0):
        separated_regions=separated_regions_f(Separation_indices,threshold_column_sigmentation)
        column_splets=[]
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            column_splets.append(img[min:max+1 , :])
    else:
        column_splets=[img]
    return column_splets



def height_of_line_Segmentatin(img):
    # horizontal projection is applied
    H_proj=horizontal_projection(img)
    peaksList = FindPeaks(H_proj) #List: (['peaks'],['indexes'])
    # plot peeks in image

    #plt.plot(peaksList[0])
    #plt.show()

    # get max peak and draw white line in max peak
    peaksList = FindMax(peaksList[0],peaksList[1],1)
    img[peaksList[1][0],:]=255

    # get connected components
    ret, labels = cv2.connectedComponents(img,connectivity=8)

    # get line with maximum peaks
    label_of_line=labels[peaksList[1][0],0]
    for i in np.arange(img.shape[0]):
        for j in np.arange(img.shape[1]):
            if(labels.item(i,j)==label_of_line):
                img.itemset((i,j),255)
            else:
                img.itemset((i,j),0)
    line_image=column_Segmentatin(img)[0]

    # get height of line
    height_line=line_image.shape[0]
    return height_line






def line_Segmentatin (img) :
    #img=column_Segmentatin(np.copy(img))[0]
    # get height of one line
    height_line=height_of_line_Segmentatin(np.copy(img))
    # calculate space between lines
    error=int((height_line*20)/100)
    # calculate numbers of lines
    number_of_line=int(img.shape[0]/(height_line+error))
    if number_of_line==0:
        return [img]
    height_line=int(img.shape[0]/number_of_line)
    # split image to lines
    lines_splets=[]
    start=0
    for i in range(number_of_line):
        if img.shape[0]>=height_line+start :
            lines_splets.append(img[start:height_line+start , :])
            #cv2.imwrite('result_image/line_segmanted'+str(i)+'.jpg',img[start:height_line+start , :])
            start+=height_line
    return lines_splets





def word_Segmentatin (img) :

    #vertical projection is applied
    V_proj=vertical_projection(img)

    # horizontal projection is applied
    H_proj=horizontal_projection(img)
    peaksList = FindPeaks(H_proj)
    # get max peak and draw white line in max peak
    peaksList = FindMax(peaksList[0],peaksList[1],1)
    upgrade_image=np.copy(img)
    line_change=np.copy(upgrade_image[peaksList[1][0],:])
    upgrade_image[peaksList[1][0],:]=255

    # get connected components
    ret, labels = cv2.connectedComponents(upgrade_image,connectivity=8)

    # get line with maximum peaks
    label_of_line=labels[peaksList[1][0],0]
    for i in np.arange(img.shape[0]):
        for j in np.arange(img.shape[1]):
            if(labels.item(i,j)==label_of_line):
                upgrade_image.itemset((i,j),255)
            else:
                upgrade_image.itemset((i,j),0)

    upgrade_image[peaksList[1][0]]=line_change

    # get separation region indices and separated regions
    Separation_indices=Separation_indices_f(V_proj)

    # calculate word threshold
    count_spaces=np.array(count_spaces_conected(V_proj))
    threshold_word_sigmentation=np.mean(count_spaces)

    if(len(Separation_indices)>0):
        separated_regions=separated_regions_f(Separation_indices,threshold_word_sigmentation)
        line_words=[]

        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            line_words.append((img[: , min:max+1],upgrade_image[: , min:max+1]))
            #cv2.imwrite('result_image/word_segmanted'+str(i)+'.jpg',upgrade_image[: , min:max+1])

    else:
        line_words=[(img,upgrade_image)]
    return line_words







def part_Segmentatin(img,upgrade_img):
    #vertical projection is applied
    V_proj=vertical_projection(img)
    # get separation region indices and separated regions
    Separation_indices=Separation_indices_f(V_proj)
    if(len(Separation_indices)>0):
        separated_regions=separated_regions_f(Separation_indices,0)
        word_parts=[]
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            word_parts.append((img[: , min:max+1],upgrade_img[: , min:max+1]))
            #cv2.imwrite('result_image/part_segmanted'+str(i+len(separated_regions)+len(Separation_indices)+min+max)+'.jpg',img[: , min:max+1])

    else:
        word_parts=[(img,upgrade_img)]
    return word_parts
