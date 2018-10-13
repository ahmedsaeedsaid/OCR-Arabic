
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
        elif count>=threshold:
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







