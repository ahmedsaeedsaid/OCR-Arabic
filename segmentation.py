from segmentation_character import *

def page_segmentation(img):

    #vertical projection is applied
    V_proj=vertical_projection(img)

    # get separation region indices and separated regions
    Separation_indices=separation_indices(V_proj)

    # calculate page sigmentation
    threshold_page_sigmentation=50

    if(len(Separation_indices)>0):
        separated_regions=separate_regions(Separation_indices,threshold_page_sigmentation)
        page_columns=[]
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            page_columns.append(img[: , min:max])

    else:
        page_columns=[img]
    return page_columns

def column_segmentation(img):

    # calculate threshold to ignore segmented image
    img_cleared, _ = clear_diacritics(img)
    line_image = determination_image(img_cleared)
    threshold=line_image.shape[0]/2

    #horizontal projection is applied
    H_proj=horizontal_projection(img)
    # get separation region indices and separated regions
    Separation_indices=separation_indices(H_proj)

    # ignore segmented image
    if len(Separation_indices) >0:
        separated_regions=separate_regions(Separation_indices,1)
        new_separated_regions=[]
        columns=[]
        for i in range(len(separated_regions)):

            if (separated_regions[i][1]-separated_regions[i][0])<threshold:

                if (i==(len(separated_regions)-1) or (i != 0 and (separated_regions[i][0]-separated_regions[i-1][1]) <(separated_regions[i+1][0]-separated_regions[i][1]))) and len(new_separated_regions)>0:
                    new_separated_regions[len(new_separated_regions)-1]=(new_separated_regions[len(new_separated_regions)-1][0],separated_regions[i][1])
                else:
                    separated_regions[i+1]=(separated_regions[i][0],separated_regions[i+1][1])
            else:
                new_separated_regions.append((separated_regions[i][0],separated_regions[i][1]))
        separated_regions = new_separated_regions

        for separated_region in separated_regions:
            columns.append(img[separated_region[0]:separated_region[1],:])
    else:
        columns=[img]
    return columns

def line_segmentation(img) :

    # get height of one line
    img_cleared, _ = clear_diacritics(img)
    line_image=determination_image(img_cleared)
    approx_height_line=line_image.shape[0]

    # calculate numbers of lines
    number_of_line = int(img.shape[0]/approx_height_line)
    if((img.shape[0]/approx_height_line)%number_of_line>0.85):
        number_of_line+=1
    if number_of_line <= 1 :
        return [img]

    H_proj=horizontal_projection(img)

    peaksList = find_peaks(H_proj)
    # take 35 % from peaks
    peaksList=find_max(peaksList[0],peaksList[1],int((len(peaksList[0])*35)/100))
    # sort locations
    locations=peaksList[1]
    insertionSort(locations,False)

    # culculate height of line
    distances=[]
    for i in range(len(locations)-1):
        if(locations[i]-locations[i+1]>=approx_height_line):
            distances.append(locations[i]-locations[i+1])

    if len(distances)>0 :
        height_line=np.mean(np.array(distances))
        if height_line<approx_height_line:
            height_line = int(img.shape[0]/number_of_line)
    else:
        height_line = int(img.shape[0]/number_of_line)
    # split image to lines
    lines = []
    start = 0
    for i in range(number_of_line):
        if img.shape[0]>=height_line+start :
            lines.append(img[start:height_line+start , :])
            start+=height_line
    return lines

def word_segmentation(img) :
    #remove under line from image
    img = remove_underline(img)
    # clear increases in line
    upgrade_image,baseline = clear_diacritics(img)

    # vertical projection is applied
    V_proj=vertical_projection(upgrade_image)

    # get separation region indices and separated regions
    Separation_indices=separation_indices(V_proj)
    # split image to words
    if(len(Separation_indices)>0):

        separated_regions=separate_regions(Separation_indices,1)
        words=[]
        pre_part=separated_regions[0]
        word=pre_part
        for i in range(1,len(separated_regions)):
            current_part=separated_regions[i]
            pre_pen=pen_size(upgrade_image[: , pre_part[0]:pre_part[1]])
            current_pen=pen_size(upgrade_image[: , current_part[0]:current_part[1]])
            if (current_part[0]-pre_part[1])>((pre_pen+current_pen)/2) :
                words.append((img[: ,  word[0]:word[1]],upgrade_image[: , word[0]:word[1]]))
                word=current_part
            else:
                word=(word[0],current_part[1])
            pre_part=current_part

        words.append((img[: ,  word[0]:word[1]],upgrade_image[: , word[0]:word[1]]))
    else:
        words=[(img,upgrade_image)]
    return words,baseline

def word_segmentation_V2(img,threshold_word_segmentation) :

    #remove under line from image
    img = remove_underline(img)

    # clear increases in line
    upgrade_image,baseline = clear_diacritics(img)

    # vertical projection is applied
    V_proj=vertical_projection(img)

    # get separation region indices and separated regions
    Separation_indices=separation_indices(V_proj)

    # split image to words
    if(len(Separation_indices)>0):

        separated_regions=separate_regions(Separation_indices,threshold_word_segmentation)
        words=[]
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            words.append((img[: , min:max],upgrade_image[: , min:max]))
    else:
        words=[(img,upgrade_image)]
    return words,baseline

def sub_word_segmentation(img,upgrade_img):
    number_of_sub_words, labels = cv2.connectedComponents(upgrade_img,connectivity=8)
    diacritics_img, found=filtering_diacritics(img,upgrade_img)

    parts=[]
    parts_dir=[]
    sub_words=[]
    parts_not_valid=[]
    # create empty image to save sub-word without director and doted
    for i in range(1,number_of_sub_words):
        part = filtering_component(upgrade_img,labels,i)
        det_part=determination_image(part)
        if (check_dotted(det_part)==1) and det_part.shape[0]<pen_size(upgrade_img)*3:
            parts_not_valid.append(i)
            marge_two_image(diacritics_img,upgrade_img)


        parts.append(np.zeros(upgrade_img.shape))

    # seperate sub-word in var 'parts' without director and doted and create diacritics image
    for i in np.arange(labels.shape[0]):
        for j in np.arange(labels.shape[1]):
            for k in range(1,number_of_sub_words):
                if labels.item(i,j)==k and k not in parts_not_valid:
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
            if labels_of_diacritics.item(i,j)!=0 :
                parts_dir[diacrtics[labels_of_diacritics.item(i,j)-1]][i][j]=255



    # seperate sub-word in var 'parts_dir' with director and doted
    for i in range(1,number_of_sub_words):
        if i not in parts_not_valid:
            V_proj=vertical_projection(parts_dir[i-1])
            Separation_indices=separation_indices(V_proj)
            if(len(Separation_indices)>0):
                separated_regions=separate_regions(Separation_indices,1)
                sub_words.append((parts_dir[i-1][:,separated_regions[0][0]:separated_regions[0][1]+2],parts[i-1][:,separated_regions[0][0]:separated_regions[0][1]+2]))


    return sub_words

def char_segmentation(img,upgrade_img,pen,baseline,index):
    img = increase_shape(img,2)
    upgrade_img = increase_shape(upgrade_img,2)


    try:
        contour_image,contour = contour_extraction(upgrade_img)
    except:
        return [(determination_image(img),determination_image(img))]


    image,start_point,end_point = up_contour(contour_image,contour,pen+2)
    if len(image) == 0 :

        return [(determination_image(img),determination_image(upgrade_img))]

    up_contour_chars, _ = seperated_region_area(image,start_point,end_point)


    output_chars = cut_original_sub_word(img,upgrade_img,contour_image,up_contour_chars,image)

    chars = formation_char_data(output_chars,up_contour_chars)

    # post precessing


    space_counter=0
    len_chars=len(chars)

    for i in range(len_chars):


        if chars[i].startPoint[0]<baseline-pen and i!=0:

            temp_image=chars[i].upgradeChar.copy()
            marge_two_image(temp_image,chars[i-1].upgradeChar)
            if check_hole_found(temp_image) and not check_hole_found(chars[i-1].upgradeChar):
                chars[i-1].ignore=True
                if (i>1):
                    chars[i-2].ignore=False

            space_counter=0

        elif character_satisfied(chars[i].char,chars[i].upgradeChar,chars[i].startPoint[0],chars[i].endPoint[0],pen,i,baseline,len_chars) and i!=len_chars-1:

            if i>=2 and check_sheen(chars[i-1],chars[i-2],pen,i,baseline,len_chars):

                chars[i-1].ignore=True
                chars[i-2].ignore=True
                if i>2:
                    chars[i-3].ignore=False
                space_counter=0
            else:
                space_counter+=1

        else:

            if i == len_chars-1:

                if chars[i].startPoint[0]>baseline+pen or character_satisfied(chars[i].char,chars[i].upgradeChar,chars[i].startPoint[0],chars[i].endPoint[0],pen,i,baseline,len_chars) or check_part_of_kaf(chars[i].char,chars[i].upgradeChar,chars[i].startPoint[0],chars[i].endPoint[0],pen,i,baseline,len_chars):
                    chars[i-1].ignore=True
                    if i>=3 and check_sheen(chars[i-2],chars[i-3],pen,i,baseline,len_chars):
                        chars[i-2].ignore=True
                        chars[i-3].ignore=True
                    elif space_counter==2:
                        chars[i-2].ignore=True
                        chars[i-3].ignore=True
                    elif space_counter==1:
                        chars[i-2].ignore=True
                        if (i>2):
                            chars[i-3].ignore=False
                else:

                    if space_counter==3:
                        chars[i-2].ignore=True
                        chars[i-3].ignore=True
                        space_counter=0
                    elif space_counter==2:

                        chars[i-2].ignore=True
                        chars[i-3].ignore=True
                        space_counter=0
                    elif space_counter==1:
                        chars[i-2].ignore=True
                        if (i>2):
                            chars[i-3].ignore=False
                        space_counter=0

            if space_counter%3==0 and space_counter>=3:
                count=0

                for k in range(0,int(space_counter/3)):

                    chars[i-(2+count)].ignore=True
                    chars[i-(3+count)].ignore=True
                    count+=3
                space_counter=0
            elif space_counter==1:
                chars[i-2].ignore=True
                if (i>2):
                    chars[i-3].ignore=False
                space_counter=0
            elif space_counter==2:
                chars[i-2].ignore=True
                chars[i-3].ignore=True
                space_counter=0
            elif space_counter>3:
                count=0
                for k in range(0,int((space_counter-1)/3)):
                    chars[i-(2+count)].ignore=True
                    chars[i-(3+count)].ignore=True
                    count+=3
                chars[i-(2+count)].ignore=True
                if (i>2):
                    chars[i-(3+count)].ignore=False
                space_counter=0


    chars[len_chars-1].ignore=False
    for i in range(len_chars-1):
        if chars[i].ignore:

            marge_two_image(chars[i+1].char,chars[i].char)
            marge_two_image(chars[i+1].upgradeChar,chars[i].upgradeChar)

    reChars=[]
    for i in range(len_chars):

        if not chars[i].ignore :

            #overSeg_chars=overcheck_yaa(chars[i].char,chars[i].upgradeChar,baseline,pen)
            overSeg_chars=[]
            if len(overSeg_chars)==0  and not (len_chars>=2 and determination_image(chars[i].char).shape[1]==determination_image(img).shape[1]):
                reChars.append((determination_image(chars[i].char),determination_image(chars[i].upgradeChar)))
                continue
            else:
                for overSeg_char in overSeg_chars:
                    countwhite= calculate_number_white_pixels(overSeg_char[1])
                    size = overSeg_char[0].shape[0] * overSeg_char[0].shape[1]

                    if  countwhite!=0 and size > 4 and not (len_chars!=1 and overSeg_char[0].shape[0]==img.shape[0]):
                        reChars.append((determination_image(overSeg_char[0]),determination_image(overSeg_char[1])))
                continue
    if len(reChars)==0:
        reChars.append((determination_image(img),determination_image(upgrade_img)))

    return reChars
