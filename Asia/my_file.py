import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
import subprocess
import os


def run_script(filename,path):
    # Arguments for the bash script
    bash_script_path = ".\Release\\fnvfilenetExample.exe"
    arg1="open \"" +filename + "\"\n"
    arg2 = "first"+ "\n"
    arg3="unit"+ "\n"
    arg4 = "update"+ "\n"
    arg5 = "savecsv \"" + path+ "\" \n"
    exit = "exit\n"
    # Command to execute the bash script with arguments
    commands = [arg1,arg2,arg3,"3\n",arg4,arg5,exit]
    process = subprocess.Popen(bash_script_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        for command in commands:
            process.stdin.write(command)
            process.stdin.flush()
        print("Bash script executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error executing bash script:", e)

def open_csv(path:str):
    with open(path, 'r') as csvfile:
        # Create a NumPy array to store the data
        data = []
        # Iterate over each line in the CSV file
        for line in csvfile:
            # Split the line into fields using comma as the delimiter
            fields = line.strip().split(',')
            temp = [float(x) for x in fields]
            # Convert the fields to numerical values if needed
            # For example, you can use list comprehension to convert strings to floats:
            # fields = [float(field) for field in fields]
            # Append the row to the data array
            data.append(temp)
    array = np.array(data)
    return array # return data of size x,y

def plot_heat_map(data):
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.colorbar()

def load_files(directory:str, extension:str="jpg"):
    file_names = []
    
    # Iterate over files in the directory
    for filename in os.listdir(directory):
        # Check if the file has the desired extension
        if filename.endswith(extension):
            # Add the file name to the list
            file_names.append(filename)
    
    return file_names

def transform_and_save(input_folder:str,folder_name:str):
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data\\"+folder_name):
        os.makedirs("data\\"+folder_name)
        
    paths = load_files(input_folder)
    for path in paths:
        print(path)
        run_script(input_folder + "\\" +path, ".\data\\" +folder_name +"\\"+ str(path).replace(".jpg","") + ".csv")

    
def info_reg(img, x,y,r):
    sel_reg = img[y-r:y+r,x-r:x+r].flatten()
    a=np.max(sel_reg)
    b=np.min(sel_reg)
    c=np.mean(sel_reg)
    return a,b,c

def analyse_all(path_to_folder:str, x,y,r):
    files = load_files(path_to_folder,"csv")
    for file in files:
        img = open_csv(path_to_folder+"\\"+file)
        sel_reg = info_reg(img, x,y,r)
        np.savetxt(path_to_folder+"\\ANALYSED_"+file, sel_reg, delimiter=',')




#
OUTPUT_FOLDER = "dd"

def step1():
    PATH_TO_IMAGES = "images"
    transform_and_save(PATH_TO_IMAGES, OUTPUT_FOLDER)


### Try first image

def step2():
    PATH_TO_IMAGE = ".\\data\\"+OUTPUT_FOLDER+"\\f2.csv" ## path to first image in a batch
    img = open_csv(PATH_TO_IMAGE)
    plot_heat_map(img)
    plt.show()


### SELECT REGION

def step3():
    X_VAL = 240 # center
    Y_VAL = 340
    A_SQUARE = 5
    PATH_TO_FOLDER = "data\\"+OUTPUT_FOLDER # Folder with CSVs
    analyse_all(PATH_TO_FOLDER,X_VAL,Y_VAL,A_SQUARE)

### Load all images in a batch
#   analyse_all(PATH_TO_FOLDER,X_VAL,Y_VAL,A_SQUARE)

# STEPS

step1()
#step2()
#step3()