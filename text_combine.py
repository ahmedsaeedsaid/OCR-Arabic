from segmentation import *
from keras.models import load_model

def combine_text(allwordchars,chars,alllines,allwordsparts,allwordspartslens,loaded_model):
    real_chars=["ع","ح","ا","ب","ض","د","ف","غ","ه","ء","ئ","ج","ك","خ","ل","لا","م","ن","ق","ر","ص","ش","س","ت","ة","ط","ث","و","ي","ظ","ذ","ز"]
    text = ""
    char_resized = []
    chars.reverse()
    for char in chars:
        char_resized.append(cv2.resize(char,(16, 16)))

    char_resized = np.array(char_resized)
    char_resized = char_resized.reshape(char_resized.shape[0], (char_resized.shape[1] * char_resized.shape[2]))
    char_resized = char_resized.astype(np.float64)
    char_resized/=255
    text1=""
    z=0
    y=len(allwordchars)-1
    l=0
    v=0
    f=len(allwordspartslens)-1
    r=0
    f2=1
    for x in loaded_model.predict(char_resized):
        if alllines[l]==v:
            if l != len(alllines)-1:
                l=l+1
            if v!=0:
                text = text + "\n"
            v=0
        if allwordchars[y]==z :
             if y != 0:
                 y=y-1
             if z!= 0 :
                text1 = text1+ text+" "
                text=""
                f2=0
             z=0
        if allwordspartslens[f]==r:
            if f!=0:
                f=f-1
            if r!=0 and f2!=0:
                text1 = text1 +""+ text
                text=""
            f2=1
            r=0

        text= real_chars[np.argmax(x)]+text

        r=r+1
        z=z+1
        v=v+1
        f2=1

    text1 = text1+ text
    return text1
