from PIL import Image
import os

def convert_to_ico(input_image_path, output_icon_path, sizes=None):
    """
    Converts an image file to an .ico file using Pillow.

    Args:
        input_image_path (str): The path to the input image file (e.g., PNG, JPG).
        output_icon_path (str): The desired path for the output .ico file.
        sizes (list of tuples, optional): A list of (width, height) tuples for
                                          the icon sizes to include. Common sizes
                                          for Windows are (16,16), (32,32), (48,48), (256,256).
                                          If None, Pillow will use its default sizes.
    """
    try:
        img = Image.open(input_image_path)

        # Ensure the image has an alpha channel for transparency
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # Save the image as an ICO file
        if sizes:
            img.save(output_icon_path, format='ICO', sizes=sizes)
        else:
            img.save(output_icon_path, format='ICO')

        print(f"Successfully converted '{input_image_path}' to '{output_icon_path}'")
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_image_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define your input and output paths
    # You'll need to download the image I generated and place it in the same directory,
    # or provide its full path. Let's assume you save it as 'crossed_swords_shield.png'.
    
    input_file = 'crossed_swords_shield.png' # Make sure this matches your image file name
    output_file = 'icon.ico'

    # Common icon sizes for good compatibility across Windows
    # You can customize this list or set it to None to use Pillow's defaults.
    icon_sizes = [(16,16), (24,24), (32,32), (48,48), (64,64), (128,128), (256,256)]

    convert_to_ico(input_file, output_file, sizes=icon_sizes)

    # Optional: Clean up the generated PNG if you downloaded it just for this conversion
    # if os.path.exists(input_file):
    #     os.remove(input_file)
    #     print(f"Removed temporary input file: {input_file}")