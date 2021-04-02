# Preparing the dataset

To prepare the dataset, we will perform two steps:
1. download the zip archives
2. unzip all archives in a correct folder hierarchy

To help with these steps, the following short guide has been created:

## 1) Downloading the MIMII dataset

> **Note:** The 12 zip files in the dataset are between 6.5 and 11GB in size for **a total of 93.3GB**. Make sure your system and connection can handle the transfer.

### Using the homepage

The MIMII dataset can be downloaded from the [homepage](https://zenodo.org/record/3384388).

### Using cURL

An alternative is to use a data transfer tool like [cURL](https://curl.se/). Installation instructions for a multitude of systems can be found on their homepage.

To verify that cURL is installed, open a command prompt (Windows) or terminal (Linux), and type:

```cmd
curl --version
```

After that is ok, you can download the dataset with the following commands:

#### a) To download one zip file

```cmd
curl -# -O https://zenodo.org/record/3384388/files/6_dB_fan.zip
```

#### b) To download all audio samples for machines without added noise (6dB <abbr title="Signal-to-noise ratio">SNR</abbr>)

```cmd
curl -# -O https://zenodo.org/record/3384388/files/{6_dB_fan,6_dB_pump,6_dB_slide,6_dB_valve}.zip
```

and for the 0 dB and -6 dB SNR zip-files:

```cmd
curl -# -O https://zenodo.org/record/3384388/files/{6_dB_fan,6_dB_pump,6_dB_slide,6_dB_valve}.zip
curl -# -O https://zenodo.org/record/3384388/files/{0_dB_fan,0_dB_pump,0_dB_slide,0_dB_valve}.zip
curl -# -O https://zenodo.org/record/3384388/files/{-6_dB_fan,-6_dB_pump,-6_dB_slide,-6_dB_valve}.zip
```

#### c) To download the complete dataset at once

```cmd
curl -# -O https://zenodo.org/record/3384388/files/{6_dB_fan,6_dB_pump,6_dB_slide,6_dB_valve,0_dB_fan,0_dB_pump,0_dB_slide,0_dB_valve,-6_dB_fan,-6_dB_pump,-6_dB_slide,-6_dB_valve}.zip
```

## 2) Unzipping the archives

### Shell script for Linux

```sh
#!bin/sh
mkdir ./min6dB
mkdir ./0dB
mkdir ./6dB
7z -o6dB -y x ./6_dB_fan.zip
7z -o6dB -y x ./6_dB_pump.zip
7z -o6dB -y x ./6_dB_slider.zip
7z -o6dB -y x ./6_dB_valve.zip
7z -o0dB -y x ./0_dB_fan.zip
7z -o0dB -y x ./0_dB_pump.zip
7z -o0dB -y x ./0_dB_slider.zip
7z -o0dB -y x ./0_dB_valve.zip
7z -omin6dB -y x ./-6_dB_fan.zip
7z -omin6dB -y x ./-6_dB_pump.zip
7z -omin6dB -y x ./-6_dB_slider.zip
7z -omin6dB -y x ./-6_dB_valve.zip
```

### Batch script for Windows

```cmd
md 6dB
md 0dB
md min6dB
7z.exe -o6dB -y x .\6_dB_fan.zip
7z.exe -o6dB -y x .\6_dB_pump.zip
7z.exe -o6dB -y x .\6_dB_slider.zip
7z.exe -o6dB -y x .\6_dB_valve.zip
7z.exe -o0dB -y x .\0_dB_fan.zip
7z.exe -o0dB -y x .\0_dB_pump.zip
7z.exe -o0dB -y x .\0_dB_slider.zip
7z.exe -o0dB -y x .\0_dB_valve.zip
7z.exe -omin6dB -y x .\-6_dB_fan.zip
7z.exe -omin6dB -y x .\-6_dB_pump.zip
7z.exe -omin6dB -y x .\-6_dB_slider.zip
7z.exe -omin6dB -y x .\-6_dB_valve.zip
```