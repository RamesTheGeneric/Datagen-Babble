import pandas as pd
from PIL import Image
from multiprocessing import Pool

# Function to load image and handle exceptions
def load_image(filename):
    try:
        img = Image.open(filename)
        return None  # Return None if image is loaded successfully
    except Exception as e:
        return {'filename': filename, 'error': str(e)}  # Return filename and error if loading fails

# Function to process each row in parallel
def process_row(row):
    filename = row['filename']
    #print(filename)
    #filename = f'C:\Users\epicm\Desktop\Dataset\{filename}'
    return load_image(filename)

def main():
    # Load CSV file into a pandas DataFrame
    csv_filename = 'combined_blendshapes.csv'  # Change this to your CSV file
    df = pd.read_csv(csv_filename)

    # Use multiprocessing to load images in parallel
    with Pool() as pool:
        results = pool.map(process_row, df.to_dict(orient='records'))

    # Filter out successful loads (None) and collect errors
    errors = [result for result in results if result is not None]

    # Save errors to "missingimages.csv"
    missing_images_df = pd.DataFrame(errors)
    missing_images_csv = 'missingimages.csv'
    missing_images_df.to_csv(missing_images_csv, index=False)

if __name__ == "__main__":
    main()