import glob, os, time

# https://www.mclibre.org/consultar/python/lecciones/python-for.html
# https://j2logo.com/python/ordenar-una-lista-en-python/

def c1000_generator():
    """Generator Casillero 1000.
        
        - Script in python for generation of
          a 1000 peg system from mixing two
          systems:
           + number-form  (0-9)
           + number-peg (00-99)
        - Ensure you have in the same folder
          the folders called:
          + /numbers
          + /numforms
          + /c1000
          
    """
    try:
        filesB=glob.glob("./numbers/*.jpg")
        filesA=glob.glob("./numforms/*.jpeg")
        route="./c1000/"
        count=0
        filesA.sort()
        filesB.sort()
        for fileA in filesA:
            for fileB in filesB:
                fileC = route + fileA[-6:-5] + fileB[-6:-4]
                print(fileC)
                os.system("convert {} {} +append {}.jpg".format(fileA, fileB, fileC))
                time.sleep(0.25)
                count = count + 1

            print(count)
    except:
        print("Please, ensure you have the folders for number-form and peg-number and c!000 system available in the same folder.")

c1000_generator()