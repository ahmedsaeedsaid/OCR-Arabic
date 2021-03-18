# **Arabic OCR**
* OCR system for Arabic language that converts images (multi-fonts) of typed text to machine-encoded text.<br>
* The system currently supports only letters (29 letters) ا-ى , لا.
* The system aims to solve a simpler problem of OCR with images that contain only Arabic characters (check the dataset link below to see a sample of the images).

## Setup
Install python then run this command:
```shell
pip install -r requirements.txt
```

## Run
1. Put the images in src/test directory
2. Go to src directory and run the following command
    ```shell
    test.py
    ```
3. Output folder will be created with:
    - text folder which has text files corresponding to the images.
    - running_time file which has the time taken to process each image.



## Dataset
- Link to dataset of images and the corresponding text: [here](https://drive.google.com/open?id=1Nbp9ZXLlWV3n8yRMwj2gjs_rE6qGZU01).
- We used 15000 images to generate character dataset that we used for training.


Performance
===========
- Average accuracy: 95%.
- Average time per image: 3 seconds.
---
**NOTE**

We achieved these results when we used only the flatten image as feature.
