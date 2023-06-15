import os
import cv2
import multiprocessing

# Path to directory containing images
path_to_files = "C:/Users/epicm/Desktop/BabbleTraining/eyeimages/"

def process_file(filenameL):
    imgL = cv2.imread(path_to_files + filenameL)
    imgL = imgL[0:256, 0:256]
    imgL = cv2.resize(imgL, [128, 128])
    filenameR = filenameL.replace("_L.png", "_R.png")
    imgR = cv2.imread(path_to_files + filenameR)
    imgR = imgR[0:256, 0:256]
    imgR = cv2.resize(imgR, [128, 128])
    img = cv2.vconcat([imgL, imgR])
    filename = filenameL.replace("_L.png", ".png")
    cv2.imwrite('eyeimages/' + filename, img)
    return(img)


if __name__ == '__main__':
    # Get the list of files to process
    files = [filename for filename in os.listdir(path_to_files) if filename.endswith("L.png")]

    # Set the number of processes to use
    num_processes = multiprocessing.cpu_count()

    # Create a pool of processes
    pool = multiprocessing.Pool(processes=num_processes)

    # Process the files using the pool of processes
    results = pool.map(process_file, files)
