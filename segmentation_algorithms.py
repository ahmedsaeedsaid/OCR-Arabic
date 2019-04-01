from pre_processing import *

def calculate_threshold_word_sigmentation(lines):
    total_spaces=np.empty((0,0))
    for line in lines:
        V_proj=vertical_projection(line)
        spaces=count_spaces_connected(V_proj)
        total_spaces=np.concatenate((total_spaces,spaces),None)
    if len(total_spaces)==0:
        return 1
    return int(round(np.mean(total_spaces)+1))

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

def separation_indices(list):
    Separation_indices=[i for i in range(len(list)) if list[i]>0]
    return Separation_indices

def separate_regions(Separation_indices,threshold):
    separated_regions=[]
    min=Separation_indices[0]
    preavis_index=Separation_indices[0]
    for index in Separation_indices:
        if index==preavis_index:
            continue
        elif index==(preavis_index):
            preavis_index=index

        elif (index-preavis_index) > threshold:
            separated_regions.append((min,preavis_index+2))
            min=index
            preavis_index=index
        else:
            preavis_index=index
    separated_regions.append((min,preavis_index+2))
    return separated_regions

def count_spaces_connected(list):
    count_spaces=[]
    count=0
    start_zero = not (list[0]==0)
    for value in list :
        if value==0 and start_zero:
            count+=1
        elif value!=0:
            start_zero=True
            if count!=0:
                count_spaces.append(count)
                count=0
    return count_spaces

def find_peaks(listY):
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

def find_max( listOfY , indexes, numOfMax):
    'This method finds the maximum values in the list of peaks'
    listMax = []
    xList = []
    for c in range(0,numOfMax):
        listMax.append(max(listOfY))
        index = listOfY.index(max(listOfY))
        xList.append(indexes[index])
        listOfY.pop(index)
    return listMax, xList

def pen_size(part):
    max_freq_V_proj=10
    max_freq_H_proj=10
    # vertical projection is applied
    V_proj=vertical_projection(part)

    V_proj=[V_proj[i] for i in range(len(V_proj)) if V_proj[i]!=0]
    if len(V_proj)>0:
        max_freq_V_proj=np.argmax(np.bincount(np.array(V_proj)))
    # horizontal projection is applied
    H_proj=horizontal_projection(part)
    H_proj=[H_proj[i] for i in range(len(H_proj)) if H_proj[i]!=0]
    if len(H_proj)>0:
        max_freq_H_proj=np.argmax(np.bincount(np.array(H_proj)))
    if max_freq_H_proj>max_freq_V_proj:
        return max_freq_V_proj
    else:
        return max_freq_H_proj

def points_clockwise_diraction(point):
    list=[]
    list.append((point[0],point[1]+1))
    list.append((point[0]-1,point[1]+1))
    list.append((point[0]-1,point[1]))
    list.append((point[0]-1,point[1]-1))
    list.append((point[0],point[1]-1))
    list.append((point[0]+1,point[1]-1))
    list.append((point[0]+1,point[1]))
    list.append((point[0]+1,point[1]+1))
    return list

def insertionSort(list  , AS):
    for i in range(1, len(list)):

        key = list[i]
        j = i-1
        while j >=0 and ((key < list[j] and AS) or (key > list[j] and not AS)) :
                list[j+1] = list[j]
                j -= 1
        list[j+1] = key

def marge_two_image(Fimage,Simage):
    for i in np.arange(Fimage.shape[0]):
        for j in np.arange(Fimage.shape[1]):
            if Simage.item(i,j)==255:
                Fimage[i,j]=255

def mean_pens(words):
    pens=[]
    for word_parts in words:
        for part in word_parts:
                    pens.append(pen_size(part[1]))
    return round(np.mean(np.array(pens)))

def increase_shape(img,value):
    image=np.zeros((img.shape[0]+(2*value),img.shape[1]+(2*value)))
    for j in np.arange(img.shape[1]):
        for i in np.arange(img.shape[0]):
            image[i+value][j+value]=img.item(i,j)
    return image

def calculate_number_white_pixels(image):
    count=0
    for j in np.arange(image.shape[1]):
        for i in np.arange(image.shape[0]):
            if image[i][j]==255:
                count+=1
    return count
