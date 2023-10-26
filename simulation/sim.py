# sim.py
# Authors:
#   Jason Howe
#   Anirdh Sursh
#   Bailey Powers

from sarpy.io.complex.sicd import SICDReader, SICDWriter
from sarpy.io.complex.converter import open_complex
from matplotlib import pyplot
from sarpy.visualization.remap import Density
import os

# Do basic file opening
def open_file(path : str) -> SICDReader:
    """ opens the file and returns a reader object
    
    Parameters
    ----------
    path : str
        path to the file to open. assumes the file is in the "data" directory

    Returns
    -------
    SICDReader
        the reader object for the file
    None
        if there are errors
    """
    
    # check that the file exist
    full_path = os.path.join("data", path)
    if os.path.exists(full_path) == False:
        print("[-] File Path Not Found")
        return None
    
    # try to make the reader
    try:
        reader = open_complex(full_path)
    except:
        print("[-] Error in making reader")
        
    if reader != None:
        # return reader object
        return reader
    else:
        #return None in order to be explicit
        return None


def read_image(reader: SICDReader) -> None:
    """ read image and print to terminal

    Parameters
    ----------
    reader : SICDReader
        an SICDReader object

    Returns
    -------
    None    
    """

    print("[+] Print Image: ", reader.file_name)
    # get all of the data from the reader
    image = reader[:,:]
    # set the standard remap
    remap_function = Density()
    # configure pyploy
    fig, axs = pyplot.subplots(nrows=1, ncols=1, figsize=(5, 5))
    # show the image
    axs.imshow(remap_function(image), cmap='gray')
    pyplot.show()


def copy_sicd_file(input_file: str, output_file: str) -> None:
    """ copy the contents of one SICD file into another
    
    Parameters
    ----------
    input_file : str
        the first file to open
    output_file : str
        the destination to copy the file into
    
    Returns
    -------
    None
    """

    input_path = os.path.join("data", input_file)
    output_path = os.path.join("data", output_file)
    print("[+] Copying data from {} to {}".format(input_path, output_path))
    # Open the input SICD file for reading
    reader = SICDReader(input_path)
    # Read the SICD structure from the input file
    sicd_meta = reader.sicd_meta

    # If destination exists, delete it
    if os.path.exists(output_path):
        os.remove(output_path)

    # Create a new SICDWriter to write the data to the output file
    writer = SICDWriter(output_path, sicd_meta)
    # close writer
    writer.close()
    print("[+] Copy Complete")


# simulatate the stuff
def simulate() -> None:
    """ run the simulation
        # CURRENT STATE: attempt to open a SICD file and make a copy of it
        # NEXT STEP: modify pixels in image and write to copy (simulate an interference attack)
    
    Parameters
    ----------
        None
    
    Returns
    -------
        None
    
    """
    # Open and Display First Image
    reader = open_file("sicd1.nitf")
    read_image(reader)
    # Copy File
    copy_sicd_file("sicd1.nitf", "copy1.nitf")
    
    # Open and Display Copy Image
    reader2 = open_file("copy1.nitf")
    read_image(reader2)

# Main Handler
if __name__ == "__main__":
    print("[+] Starting SAR Simulation")
    simulate()
    print("[+] Ending SAR Simulation")