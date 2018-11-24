
from pre_processing import *

def vertical_projection(img):
    V_Proj=[]
    for i in np.arange(img.shape[1]):
        sum_values=0
        for j in np.arange(img.shape[0]):
            if img.item(j,i)==255:
                sum_values+=1
        V_Proj.append(sum_values)
    return V_Proj

def horizontal_projection(img):
    H_Proj=[]
    for i in np.arange(img.shape[0]):
        sum_values=0

        for j in np.arange(img.shape[1]):
            if img.item(i,j)==255:
                sum_values+=1
        H_Proj.append(sum_values)
    return H_Proj

def Separation_indices_f(list):
    Separation_indices=[i for i in range(len(list)) if list[i]>0]
    return Separation_indices

def count_spaces_connected(list):
    count_spaces=[]
    count=0
    if list[0]==0 :
        flag=False
    else:
        flag=True

    for value in list :
        if value==0 and flag:
            count+=1
        elif value!=0 and not flag :
            flag=True
        elif count!=0:
            count_spaces.append(count)
            count=0
    return count_spaces

def separated_regions_f(Separation_indices,threshold):

    separated_regions=[]
    min=Separation_indices[0]
    preavis_index=Separation_indices[0]
    count=0
    for index in Separation_indices:
        if index==preavis_index:
            continue
        elif index==(preavis_index+1):
            preavis_index=index
            count+=1
        elif (index-preavis_index) >= threshold:
            separated_regions.append((min,preavis_index))
            count=0
            min=index
            preavis_index=index
        else:
            preavis_index=index
            count=0
    separated_regions.append((min,preavis_index))
    return separated_regions

def FindPeaks(listY):
    'This method finds the peaks from the list with the Y values'
    peaks = []
    indexes = []
    count = 0
    m2 = 0 #Old slope: starts with 0
    for value in range(1,len(listY)):
        m1 = listY[value] - listY[value-1] #New slope
        if( m2 > 0 and m1 < 0 ):
            peaks.append(listY[value-1])
            indexes.append( value-1 )
        m2 = m1 #Old slope is assigned
    return peaks, indexes

def FindMax( listOfY , indexes, numOfMax):
    'This method finds the maximum values in the list of peaks'
    listMax = []
    xList = []
    reconstructedList = []
    for c in range(0,numOfMax):
        listMax.append(max(listOfY))
        index = listOfY.index(max(listOfY))
        xList.append(indexes[index])
        listOfY.pop(index)
    return listMax, xList

def Clear_increases_in_line(img):
    # horizontal projection is applied
    H_proj=horizontal_projection(img)

    peaksList = FindPeaks(H_proj)
    if len(peaksList[0])==0:
        return img
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
    return upgrade_image

def remove_underline(img):
    # vertical projection is applied
    V_proj=vertical_projection(img)

    # get separation region indices and separated regions
    Separation_indices=Separation_indices_f(V_proj)

    # split image to words
    if(len(Separation_indices)>0):
        #threshold_word_sigmentation=round(pen_size(upgrade_image,Separation_indices)+2)
        separated_regions=separated_regions_f(Separation_indices,1)
        for i in range(len(separated_regions)):
            min=separated_regions[i][0]
            max=separated_regions[i][1]
            #remove under line from image
            img = remove_underline_help(img,max,min)
    return img

def remove_underline_help(img,max,min):
    word=img[: , min:max]
    H_proj=horizontal_projection(word)
    min_index=-1
    max_index=-1
    ranges=[]
    for i in range(len(H_proj)):
        if (max-min)==H_proj[i]:
            if min_index==-1:
                min_index=i
            max_index=i
        elif  min_index !=-1:
            ranges.append((min_index,max_index))
            min_index=-1
    if len(ranges) > 0:
        counter_up=0
        counter_down=0

        aproxmate_pen_size=1
        for range_1 in ranges:
            if aproxmate_pen_size<(range_1[1]-range_1[0]+1):
                aproxmate_pen_size=range_1[1]-range_1[0]+1
        line_range=None
        for range_1 in ranges:
            for i in np.arange(word.shape[1]):
                if (range_1[0]-1)<0:
                    break
                if word.item(range_1[0]-1,i)==255:
                    counter_up+=1
            for i in np.arange(word.shape[1]):
                if (range_1[1]+1)>word.shape[0]:
                    break
                if word.item(range_1[1]+1,i)==255:
                    counter_down+=1
            if (counter_down+counter_up)<(aproxmate_pen_size*20*word.shape[1])/100:

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
                    img[line_range[0]:line_range[1]+1 , i]=0

    return img

def pen_size(part):
    # vertical projection is applied
    V_proj=vertical_projection(part)
    V_proj=[V_proj[i] for i in range(len(V_proj)) if V_proj[i]!=0]
    max_freq_V_proj=np.argmax(np.bincount(np.array(V_proj)))

    # horizontal projection is applied
    H_proj=horizontal_projection(part)

    H_proj=[H_proj[i] for i in range(len(H_proj)) if H_proj[i]!=0]
    max_freq_H_proj=np.argmax(np.bincount(np.array(H_proj)))
    if max_freq_H_proj>max_freq_V_proj:
        return max_freq_H_proj
    else:
        return max_freq_V_proj

def calculate_threshold_word_sigmentation(lines):
    total_spaces=np.empty((0,0))
    for line in lines:
        V_proj=vertical_projection(line)
        spaces=count_spaces_connected(V_proj)
        total_spaces=np.concatenate((total_spaces,spaces),None)
    if len(total_spaces)==0:
        return 1
    return int(round(np.mean(total_spaces)+1))

def check_one_dotted(img):
    shape_area=0

    im2, contours, hierarchy = cv2.findContours(np.copy(img),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    convex_hull_area=cv2.contourArea(cnt)

    for i in np.arange(img.shape[0]):
        for j in np.arange(img.shape[1]):
            if img.item(i,j)==255:
                shape_area+=1
    if shape_area/convex_hull_area>0.7:
        point_of_center_point=(int(img.shape[0]/2)+1,int(img.shape[1]/2)+1)
        if img.item(point_of_center_point[0]-1,point_of_center_point[1])==255 and img.item(point_of_center_point[0]+1,point_of_center_point[1])==255 and img.item(point_of_center_point[0],point_of_center_point[1]-1)==255 and img.item(point_of_center_point[0],point_of_center_point[1]+1)==255 :
            minor_axis_length=0
            major_axis_length=0
            for i in np.arange(img.shape[0]):
                if img.item(i,point_of_center_point[1])==255:
                    minor_axis_length+=1
            for i in np.arange(img.shape[1]):
                if img.item(point_of_center_point[0],i)==255:
                    major_axis_length+=1
            if round(major_axis_length/minor_axis_length)==1:
                return True
    return False

def check_dotted(img):
    if check_one_dotted(img):
        return True
    else:
        first_dotted=np.copy(img[:,0:int(img.shape[1]/2)])
        scand_dotted=np.copy(img[:,int(img.shape[1]/2)+2:])
        if check_one_dotted(first_dotted) and check_one_dotted(scand_dotted):
            return True
        else:
            return False
