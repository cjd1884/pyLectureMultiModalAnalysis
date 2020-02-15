# pyLectureMultiModalAnalysis - A project for lecture classification

## General
This a project for the "Multimodal information processing and analysis" lesson of the MSc Data Science program between the National Centre for Scientific Research "Demokritos" and the University of the Peloponnese. The goal is to classify a target lecture video into 3 different categories (boring, neutral, interesting) based on viewers stimulation. A sample collection of manually annotated videos used as training and evaluation dataset. The algorithm used for training is the [SVM](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html) from [sklearn](https://scikit-learn.org/) library. For audio feature extraction [pyAudioAnalysis](https://github.com/tyiannak/pyAudioAnalysis/blob/master/README.md) library used. For video feature extraction [VGG16](https://keras.io/applications/#vgg16) is used from [Keras](https://keras.io/applications/) library.

## Prerequesites
- Python 3.7.6
- pip 20.0.2
- Supported video format: `.mp4`
- Supported audio format: `.wav`

## Installation
 - Clone the source:
 ```shell
git clone https://github.com/cjd1884/pyLectureMultiModalAnalysis.git
 ```

 - Install dependencies
 ```shell
 pip install -r ./requirements.txt
 ```

## Usage
The main file is `lecture_classifier.py`. It can be run in 3 different modes:

### Mode 1: Training evaluation
This is the primary evaluation mode used to assess SVM algorithm performance on training data. Accuracy is calculated using leave-one-video-out cross validation (different video is same as different speaker - we assume one video per speaker).

Video files to be used for training need to be placed in `data/source/` folder. Format to be used is `.mp4`. Annotation file should be provided and placed under `data/` folder named as `index.csv`. Index file should have the following format:

```
FILE;SEG;CLASS_1
video_0;part_0;boring
video_0;part_1;interesting
video_0;part_2;boring
video_0;part_3;interesting
video_1;part_0;interesting
video_1;part_1;neutral
video_1;part_2;interesting
video_1;part_3;boring
```

```shell
lecture_classifier.py -a eval_train
```

### Mode 2: Training
In this mode, the SVM model is trained on the entire training dataset and it is then saved to disk.
```shell
lecture_classifier.py -a train
```

### Mode 3: Target evaluation
The trained model (loaded from disk) is used to evaluate the target video provided for classification.
Target video to be annotated by the algorithm should be placed under `data/target/` folder.
```shell
lecture_classifier.py -a eval_target
```

## Authors
 - Konstantinos Dimitros | [email](k.dimitros@gmail.com) | [github](https://github.com/cjd1884/)
 - Karozis Stelios | [email](skarozis@gmail.com) | [github](https://github.com/skarozis)
 - Karousis Konstantinos | [email](kkarousis@gmail.com) | [github](https://github.com/kkarousis)
 - Mastrapas Anastasios | [email](anastasios.mastrapas@gmail.com)
 - Nikoloutsakos Nikos | [email](nikoloutsa@gmail.com) | [github](https://github.com/nikoloutsa)
