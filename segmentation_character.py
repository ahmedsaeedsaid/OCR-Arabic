from segmentation_filtering import *

class Char:
    def __init__(self, upContourChar,upgradeChar,char,startPoint,endPoint,ignore):
        self.upContourChar = upContourChar
        self.upgradeChar = upgradeChar
        self.char = char
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.ignore = ignore

def contour_extraction(img):

    image=img.copy()
    # Enhancements are applied to the sub-word’s main-body by filling the holes
    binary_image=np.array([[1 if pixel == 255 else 0 for pixel in row ] for row in image])
    binary_image= ndimage.binary_fill_holes(binary_image)
    for j in np.arange(image.shape[1]):
        for i in np.arange(image.shape[0]):
            if image.item(i,j)==0:
               if binary_image.item(i,j)==1:
                   image[i][j]=255

    # dilation by two pixels
    kernel = np.ones((3,3),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image=np.uint8(image)

    # get counter image
    _ ,counters ,_=cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    counter = max(counters, key=cv2.contourArea)


    # draw counter image
    empty_image =np.zeros(image.shape, np.uint8)
    counter_image = cv2.drawContours(empty_image, [counter], 0, (255, 255), 0)
    counter=counter[:,0]
    #cv2.imwrite('result_image/a'+str(counter.shape)+'.jpg',counter_image)
    return (counter_image,counter)

def up_contour(img_contour,contour,pen):

    # get counter first and last part
    contour_columns_indeces=contour[:,0]
    TV =pen
    column_1=max(contour_columns_indeces)
    column_2=column_1-TV
    CFP=[]
    CLP=[]
    for point in contour :
        if point[0]>=column_2 and point[0]<=column_1+1:

            CFP.append(point)
        elif point[0]>=0 and point[0]<=TV+1:

            CLP.append(point)
    CFP=np.array(CFP)
    CLP=np.array(CLP)

    # get start point
    row_indces=np.unique(CFP[:,1])
    sorted_indces=np.sort(row_indces)
    col_index_option1=np.max(CFP[CFP[:,1]==sorted_indces[0]][:,0])
    col_index_option2=np.max(CFP[CFP[:,1]==sorted_indces[1]][:,0])

    if col_index_option1 > col_index_option2:
        start_point_x=sorted_indces[0]
        start_point_y=col_index_option1
    else:
        start_point_x=sorted_indces[1]
        start_point_y=col_index_option2

    # get end point
    row_indces=np.unique(CLP[:,1])
    sorted_indces=np.sort(row_indces)
    col_index_option1=np.max(CLP[CLP[:,1]==sorted_indces[0]][:,0])
    col_index_option2=np.max(CLP[CLP[:,1]==sorted_indces[1]][:,0])
    if col_index_option1 > col_index_option2:
        end_point_x=sorted_indces[1]
        end_point_y=col_index_option2
    else:
        end_point_x=sorted_indces[0]
        end_point_y=col_index_option1

    # crop up counter
    start_point=(start_point_x,start_point_y)
    end_point=(end_point_x,end_point_y)
    img_upcontour=crop_two_point(img_contour,start_point,end_point)
    #cv2.imwrite('result_image/a'+str(img_upcontour.shape)+'.jpg',img_upcontour)
    return (img_upcontour,start_point,end_point)

def crop_two_point(image,start_point,end_point):
    result=np.zeros(image.shape)
    result[start_point[0],start_point[1]]=255
    point_counter=start_point
    visited=[start_point]
    while (point_counter!=end_point):
        all_pos_points=points_clockwise_diraction(point_counter)
        flag=False
        for point in all_pos_points:
                if image.item(point[0],point[1])==255 and not (point in visited):
                    result[point[0],point[1]]=255
                    point_counter=point
                    flag=True
                    visited.append(point)
                    break
        if not flag:
            point_counter=visited[len(visited)-3]

    return result

def seperated_region_area(image,start_point,end_point):


    # get all continuous_region_area
    continuous_region_areas=[]
    continuous_regions=[]
    for i in np.arange(image.shape[0]):
        continuous_region=[]
        for j in np.arange(image.shape[1]):
            if image.item(i,j)==255:
                continuous_region.append((i,j))
            elif len(continuous_region)>0:
                continuous_regions.append(continuous_region)
                continuous_region=[]
            else:
                continuous_region=[]



    # get valid continuous_region_area
    for continuous_region in continuous_regions:
        size_continuous_region=len(continuous_region)

        if size_continuous_region==1:
            if image.item(continuous_region[0][0]-1,continuous_region[0][1]-1)==255  :
                if  image.item(continuous_region[size_continuous_region-1][0]-1,continuous_region[size_continuous_region-1][1]+1)==255:
                    continuous_region_areas.append((continuous_region[0],continuous_region[size_continuous_region-1]))
        elif size_continuous_region==2:
            if image.item(continuous_region[0][0]-1,continuous_region[0][1]-1)==255 or image.item(continuous_region[0][0]-1,continuous_region[0][1])==255:
                if image.item(continuous_region[size_continuous_region-1][0]-1,continuous_region[size_continuous_region-1][1])==255 or image.item(continuous_region[size_continuous_region-1][0]-1,continuous_region[size_continuous_region-1][1]+1)==255:
                    continuous_region_areas.append((continuous_region[0],continuous_region[size_continuous_region-1]))
        else:
            if image.item(continuous_region[0][0]-1,continuous_region[0][1]-1)==255 or image.item(continuous_region[0][0]-1,continuous_region[0][1])==255 or image.item(continuous_region[0][0]-1,continuous_region[0][1]+1)==255:
                if image.item(continuous_region[size_continuous_region-1][0]-1,continuous_region[size_continuous_region-1][1]-1)==255 or image.item(continuous_region[size_continuous_region-1][0]-1,continuous_region[size_continuous_region-1][1])==255 or image.item(continuous_region[size_continuous_region-1][0]-1,continuous_region[size_continuous_region-1][1]+1)==255:
                    continuous_region_areas.append((continuous_region[0],continuous_region[size_continuous_region-1]))

    # sort  continuous_region_area
    size_continuous_region_areas = len(continuous_region_areas)
    if size_continuous_region_areas ==0:
        return ([(image,start_point,end_point)],-1)
    for i in range(size_continuous_region_areas):
        for j in range(0, size_continuous_region_areas-i-1):
            if continuous_region_areas[j][0][1] < continuous_region_areas[j+1][0][1] :
                continuous_region_areas[j], continuous_region_areas[j+1] = continuous_region_areas[j+1], continuous_region_areas[j]

    # get baseline
    all_x=[]
    for continuous_region_area in continuous_region_areas:
        all_x.append(continuous_region_area[0][0])
    all_x=np.array(all_x)
    baseline=np.argmax(np.bincount(all_x))

    # skip overlapped area
    continuous_region_areas_temp=[]
    for i in range(len(continuous_region_areas)):
        flag=True
        for j in range(len(continuous_region_areas)):
            if i!=j:
                y11=continuous_region_areas[i][0][1]
                y12=continuous_region_areas[i][1][1]
                y21=continuous_region_areas[j][0][1]
                y22=continuous_region_areas[j][1][1]
                x1=continuous_region_areas[i][0][0]
                x2=continuous_region_areas[j][0][0]

                org_list=np.concatenate((np.arange(y11,y12),np.arange(y21,y22)),axis=None)
                unic_list=np.unique(np.concatenate((np.arange(y11,y12),np.arange(y21,y22)),axis=None))

                if len(org_list)>len(unic_list) and x1<x2 and x1<baseline:
                    flag=False
                    break
        if flag:
            continuous_region_areas_temp.append(continuous_region_areas[i])
    continuous_region_areas=continuous_region_areas_temp

    # cut all chars
    prev_region=continuous_region_areas[0]
    char=crop_two_point(image,start_point,prev_region[0])
    chars=[(char,start_point,prev_region[0])]
    for i in range(1,len(continuous_region_areas)):

        curr_region=continuous_region_areas[i]
        end_point_char=curr_region[0]
        start_point_char=prev_region[1]
        temp_image=image.copy()
        temp_image[start_point_char[0],start_point_char[1]+1]=0
        temp_image[start_point_char[0]-1,start_point_char[1]+1]=0
        char=crop_two_point(temp_image,start_point_char,end_point_char)
        #cv2.imwrite('result_image/upchar'+str(char.shape)+'.jpg',char)
        chars.append((char,start_point_char,end_point_char))
        prev_region=curr_region

    if end_point[1]<prev_region[0][1]-1:
        char=crop_two_point(image,end_point,prev_region[1])
        #cv2.imwrite('result_image/upchar'+str(char.shape)+'.jpg',char)
        chars.append((char,prev_region[1],end_point))
    return (chars,baseline)

def cut_original_sub_word(image,upgrade_image,contour_image,chars):

    clear_chars=[]
    chars_dir=[]

    for k in range(len(chars)):

        char=chars[k][0]
        start_point=chars[k][1]
        end_point=chars[k][2]
        start_point_down=(0,0)
        end_point_down=(0,0)
        contour_char=np.copy(char)

        if k ==0:
            contour_char[:,end_point[1]:]=contour_image[:,end_point[1]:]
            # add boundry Y

            for i in range(end_point[0]+1,contour_image.shape[0]):
                contour_char[i,end_point[1]]=255
                if contour_image[i,end_point[1]]==255:
                    break

        elif k==len(chars)-1:

            contour_char[:,0:start_point[1]]=contour_image[:,0:start_point[1]]

            # add boundry Y
            for i in range(start_point[0]+1,contour_image.shape[0]):

                contour_char[i,start_point[1]]=255
                if contour_image[i,start_point[1]]==255:
                    break


        else:
            # add boundry Y

            for i in range(start_point[0]+1,contour_image.shape[0]):
                if contour_image[i,start_point[1]]==255:
                    start_point_down=(i,start_point[1])
                    break

            for i in range(end_point[0]+1,contour_image.shape[0]):
                if contour_image[i,end_point[1]]==255:
                    end_point_down=(i,end_point[1])
                    break
            for i in range(start_point[0]+1,contour_image.shape[0]):
                contour_char[i,start_point[1]]=255
                if i==start_point_down[0]:
                    break
            for i in range(end_point[0]+1,contour_image.shape[0]):
                contour_char[i,end_point[1]]=255
                if i==end_point_down[0]:
                    break
            # add down counter for char
            temp_contour_image=contour_image.copy()
            temp_contour_image[:,end_point_down[1]-1]=0
            temp_contour_image[:,start_point_down[1]+1]=0

            cv2.imwrite('result_image/temp_contour_image'+str(end_point_down)+'.jpg',temp_contour_image)

            down_contour=crop_two_point(temp_contour_image,end_point_down,start_point_down)


            marge_two_image(contour_char,down_contour)

        # full holes in counter
        #cv2.imwrite('contour_char'+str(k)+'.jpg',contour_char)
        binary_image=np.array([[1 if pixel == 255 else 0 for pixel in row ] for row in contour_char])
        binary_image= ndimage.binary_fill_holes(binary_image).astype(int)

        clear_char=np.zeros(upgrade_image.shape)

        # extract char from image
        if k !=0 and k!=len(chars)-1:
            for j in np.arange(upgrade_image.shape[1]-1):
                for i in np.arange(upgrade_image.shape[0]):
                    if upgrade_image.item(i,j)==255 and binary_image.item(i,j+1)==1 :
                       clear_char[i,j]=255
        else:
            for j in np.arange(upgrade_image.shape[1]):
                for i in np.arange(upgrade_image.shape[0]):
                    if upgrade_image.item(i,j)==255 and binary_image.item(i,j)==1 :
                       clear_char[i,j]=255

        clear_chars.append(clear_char)
        chars_dir.append(np.copy(clear_char))

    diacritics_image , _=filtering_diacritics(image,upgrade_image)
    # calculate rate for each diacritic
    diacritics_image=np.uint8(diacritics_image)
    number_of_diacritic, labels_of_diacritics = cv2.connectedComponents(diacritics_image,connectivity=8)
    V_proj_chars=[]
    diacritics=[]
    for char in clear_chars:
        V_proj_chars.append(vertical_projection(char))

    for i in range(1,number_of_diacritic):
        diacritics.append([])
        for j in range(len(clear_chars)):
            diacritics[i-1].append(0)

    for i in np.arange(labels_of_diacritics.shape[0]):
        for j in np.arange(labels_of_diacritics.shape[1]):
            if labels_of_diacritics.item(i,j)!=0:
                for k in range(len(V_proj_chars)):
                    if V_proj_chars[k][j]!=0:
                        diacritics[labels_of_diacritics.item(i,j)-1][k]+=1

    # get part of maximum rate
    for i in range(len(diacritics)):
        diacritics[i]=diacritics[i].index(max(diacritics[i]))

    # add diacritics to parts
    for i in np.arange(labels_of_diacritics.shape[0]):
        for j in np.arange(labels_of_diacritics.shape[1]):
            if labels_of_diacritics.item(i,j)!=0:
                chars_dir[diacritics[labels_of_diacritics.item(i,j)-1]][i][j]=255


    output_chars=[]

    for i in range(len(clear_chars)):
        #cv2.imwrite('clear_char'+str(i)+'.jpg',clear_chars[i])
        #cv2.imwrite('char'+str(i)+'.jpg',clear_chars[i])
        output_chars.append((chars_dir[i],clear_chars[i]))
    return output_chars

def formation_char_data(output_chars,chars):

    formation_chars=[]
    for i in range(len(chars)):
        formation_chars.append(Char(chars[i][0],output_chars[i][1],output_chars[i][0],chars[i][1],chars[i][2],False))
    return formation_chars

def check_hole_found(image):

    binary_image=np.array([[1 if pixel == 255 else 0 for pixel in row ] for row in image])
    binary_image= ndimage.binary_fill_holes(binary_image).astype(int)
    for j in np.arange(image.shape[1]):
        for i in np.arange(image.shape[0]):
            if image.item(i,j)==0 and binary_image.item(i,j)==1:
                return True
    return False

def check_one_dotted(img):
    shape_area=0
    for i in np.arange(img.shape[0]):
        for j in np.arange(img.shape[1]):
            if img.item(i,j)==255:
                shape_area+=1
    try:
        im2, contours, hierarchy = cv2.findContours(np.copy(img),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        convex_hull_area=cv2.contourArea(cnt)
        if shape_area/convex_hull_area>0.8:

            point_of_center_point=(int(img.shape[0]/2),int(img.shape[1]/2))
            controid=[img.item(point_of_center_point[0]-1,point_of_center_point[1])==255,img.item(point_of_center_point[0]+1,point_of_center_point[1])==255,img.item(point_of_center_point[0],point_of_center_point[1]-1)==255,img.item(point_of_center_point[0],point_of_center_point[1]+1)==255]
            num_of_true=0
            for flag in controid:
                if flag:
                    num_of_true+=1
            if num_of_true>2:

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
    except:
        return False
    return False

def check_dotted(img):
    if check_one_dotted(img):
        return 1
    else:
        first_dotted=np.copy(img[:,0:int(img.shape[1]/2)])
        scand_dotted=np.copy(img[:,int(img.shape[1]/2):])
        if check_one_dotted(first_dotted) or check_one_dotted(scand_dotted):
            return 2
        else:
            return 0

def check_hamza(char,upgrade_char):
    diacritics_image,found=filtering_diacritics(char,upgrade_char)
    if not found:
        return False
    diacritics_image = np.uint8(diacritics_image)
    number_of_diacritic, labels_of_diacritics = cv2.connectedComponents(diacritics_image,connectivity=8)
    if number_of_diacritic != 2:
        return False

    component=filtering_component(diacritics_image,labels_of_diacritics,1)
    img=determination_image(component)
    shape_area=0
    for i in np.arange(img.shape[0]):
        for j in np.arange(img.shape[1]):
            if img.item(i,j)==255:
                shape_area+=1
    try:
        im2, contours, hierarchy = cv2.findContours(np.copy(img),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        convex_hull_area=cv2.contourArea(cnt)
        if shape_area/convex_hull_area>0.5:
            return True
    except:
        return False
    return False

def calculate_part_height(upgrade_char,x1,x2,index,baseline,pen,size):
    if index==0 :
        base = x2
    else:
        base = x1
    if index==size-2 and x2>baseline+pen:
        return pen * 3
    test_image=upgrade_char.copy()
    for i in np.arange(upgrade_char.shape[0]):
        for j in np.arange(upgrade_char.shape[1]):
            if upgrade_char.item(i,j) == 255:
                test_image[baseline,:]=255
                test_image[i,:]=255
                return baseline-i
    return 0

def get_number_of_dotted(char,upgrade_char):
    dotted_image=np.zeros(char.shape)
    diacritics_image,found=filtering_diacritics(char,upgrade_char)
    if not found:
        return 0 , dotted_image
    diacritics_image = np.uint8(diacritics_image)
    number_of_diacritic, labels_of_diacritics = cv2.connectedComponents(diacritics_image,connectivity=8)
    number_of_dotted=0
    for i in range(1,number_of_diacritic):
        component=filtering_component(diacritics_image,labels_of_diacritics,i)
        determinate_component=determination_image(component)
        number= check_dotted(determinate_component)
        if number>0:
            marge_two_image(dotted_image,component)
        number_of_dotted+=number
    return number_of_dotted,dotted_image

def character_satisfied(char,upgrade_char,x1,x2,pen,index,baseline,size):

    found_hole=check_hole_found(upgrade_char)
    found_hamza=check_hamza(char,upgrade_char)
    height=calculate_part_height(upgrade_char,x1,x2,index,baseline,pen,size)
    number_of_dotted, _ =get_number_of_dotted(char,upgrade_char)

    if not found_hole and number_of_dotted==0 and (height < 2 * pen) and not found_hamza:
        return True
    return False

def check_sheen(part1,part2,pen,index,baseline,size):
    combine_char=part1.char.copy()
    combine_upgrade_char=part1.upgradeChar.copy()
    found_hole1=check_hole_found(part1.upgradeChar)
    found_hole2=check_hole_found(part2.upgradeChar)
    height1=calculate_part_height(part1.upgradeChar,part1.startPoint[0],part1.endPoint[0],index,baseline,pen,size)
    height2=calculate_part_height(part2.upgradeChar,part2.startPoint[0],part2.endPoint[0],index,baseline,pen,size)

    if not found_hole1 and not found_hole2 and (height1 < 2 * pen) and (height2 < 2 * pen):
        marge_two_image(combine_char,part2.char)
        marge_two_image(combine_upgrade_char,part2.upgradeChar)
        number_of_dotted , dotted_image =get_number_of_dotted(combine_char,combine_upgrade_char)

        if number_of_dotted==3:
            dotted_image=determination_image(dotted_image)
            V_proj=vertical_projection(dotted_image)
            Separation_indices=separation_indices(V_proj)

            if len(Separation_indices)>0:
                separated_regions=separate_regions(Separation_indices,1)
                if len(separated_regions)==1:
                    return True

    return False
