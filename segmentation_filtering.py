from segmentation_algorithms import *

def clear_diacritics(img):
    # horizontal projection is applied
    img = np.copy(img)
    H_proj=horizontal_projection(img)

    peaksList = find_peaks(H_proj)
    if len(peaksList[0])==0:
        return img,int(img.shape[0]/2)
    # get max peak and draw white line in max peak
    peaksList = find_max(peaksList[0],peaksList[1],1)
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
    return upgrade_image,peaksList[1][0]

def remove_underline(img):
    # vertical projection is applied
    V_proj=vertical_projection(img)

    # get separation region indices and separated regions
    Separation_indices=separation_indices(V_proj)

    # split image to words
    if(len(Separation_indices)>0):
        separated_regions=separate_regions(Separation_indices,1)
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            #remove under line from subWord
            img = remove_underline_help(img,max-2,min)
    return img

def remove_underline_help(img,max,min):
    word=img[: , min:max]
    # horizontal projection is applied
    H_proj=horizontal_projection(word)

    # declare Variables
    min_index=-1
    max_index=-1
    ranges=[]

    # get ranges of street line
    for i in range(len(H_proj)):
        if (max-min) == H_proj[i]:
            if min_index==-1:
                min_index=i
            max_index=i
        elif  min_index !=-1:
            ranges.append((min_index,max_index))
            min_index=-1


    if len(ranges) > 0:
        line_range=None
        for range_1 in ranges:

            count_upper=calculate_number_white_pixels(word[:range_1[0] , :])
            count_down=calculate_number_white_pixels(word[range_1[1]+1: , :])
            count_pure=calculate_number_white_pixels(word)
            max_H_upper=0
            max_H_down =0
            H_upper=horizontal_projection(word[:range_1[0] , :])
            H_down=horizontal_projection(word[range_1[1]+1: , :])
            if len(H_upper)> 0:
                max_H_upper = np.max(np.array(H_upper))
            if len(H_down)> 0:
                max_H_down = np.max(np.array(H_down))
            if (count_down+count_upper)/count_pure>0.5  and (max_H_upper/(max-min)>0.35 or max_H_down/(max-min)>0.35):
                line_range=range_1

        if line_range is not None:
            for i in range(min,max+2):
                try:
                    if (img[line_range[0]-1 , i]==255) and img[line_range[1]+1 , i]==255 :
                        continue
                    if (img[line_range[0]-1 , i+1]==255) and img[line_range[1]+1 , i-1]==255 :
                        continue
                    if (img[line_range[0]-1 , i-1]==255) and img[line_range[1]+1 , i+1]==255 :
                        continue
                    if (img[line_range[0]-1 , i+1]==255) and img[line_range[1]+1 , i-1]==255 :
                        continue

                    img[line_range[0]:line_range[1]+1 , i]=0
                except:
                    img[line_range[0]:line_range[1]+1 , i-1]=0

    return img

def filtering_diacritics(img,upgrade_img):
    found=False
    diacritics_img=np.copy(img)
    for i in np.arange(diacritics_img.shape[0]):
        for j in np.arange(diacritics_img.shape[1]):
            if diacritics_img.item(i,j)==upgrade_img.item(i,j):
                diacritics_img[i][j]=0
            else:
                found=True
    return diacritics_img , found

def filtering_component(img,labels,label):
    img_process=np.copy(img)
    for i in np.arange(labels.shape[0]):
        for j in np.arange(labels.shape[1]):
            if(labels.item(i,j)!=label):
                img_process.itemset((i,j),0)
    return img_process

def determination_image(img):
    img_process=np.copy(img)
    V_proj=vertical_projection(img_process)
    H_proj=horizontal_projection(img_process)
    Separation_indices=separation_indices(H_proj)
    if len(Separation_indices)>0:
        separated_regions=separate_regions(Separation_indices,1)
        if len(separated_regions)>0:
            min=separated_regions[0][0]
            max=separated_regions[len(separated_regions)-1][1]
            img_process=img_process[min:max+1,:]

    Separation_indices=separation_indices(V_proj)
    if len(Separation_indices)>0:
        separated_regions=separate_regions(Separation_indices,1)
        if len(separated_regions)>0:
            min=separated_regions[0][0]
            max=separated_regions[len(separated_regions)-1][1]
            img_process=img_process[:,min:max+1]
    return img_process
