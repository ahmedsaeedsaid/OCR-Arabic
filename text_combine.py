from segmentation import *
from keras.models import load_model

def combine_text(allwordchars,chars,alllines):
    loaded_model=load_model('models/NN_Model.h5')
    real_chars=["ع","ح","ا","ب","ض","د","ف","غ","ه","ء","ئ","ج","ك","خ","ل","لا","م","ن","ق","ر","ص","ش","س","ت","ة","ط","ث","و","ي","ظ","ذ","ز"]
    text = " "
    char_resized = []
    chars.reverse()
    for char in chars:
        char_resized.append(cv2.resize(char,(16, 16)))

    char_resized = np.array(char_resized)
    char_resized = char_resized.reshape(char_resized.shape[0], (char_resized.shape[1] * char_resized.shape[2]))
    char_resized = char_resized.astype(np.float64)
    char_resized/=255

    z=0
    y=0
    l=0
    v=0
    for x in loaded_model.predict(char_resized):
        if alllines[l]==v:
            if l != len(alllines)-1:
                l=l+1
            if v!=0:
                text = "\n" + text
            v=0
        if allwordchars[y]==z :
             if y != len(allwordchars)-1:
                 y=y+1
             if z!= 0 :
                text = " " + text
             z=0
        text= real_chars[np.argmax(x)]+text
        z=z+1
        v=v+1

    print(text)
