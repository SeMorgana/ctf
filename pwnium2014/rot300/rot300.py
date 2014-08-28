#7/5/2014
import Image
from pytesser import *
import telnetlib
import base64
import StringIO

def main():
    tn = telnetlib.Telnet("41.231.53.40",9090)
    ret = tn.read_until("\n")
    print ret
    base64_str = ret.strip()
    decode = base64.b64decode(base64_str)

    buff = StringIO.StringIO()
    buff.write(decode)
    buff.seek(0)
    img = Image.open(buff)
    
    #construct new image
    img = img.rotate(90)
    img2 = img.rotate(180)
    new_img = Image.blend(img,img2,0.5)
    new_img = new_img.convert("RGBA")
    pixels = new_img.load()
    width, height = new_img.size
    for x in range(width):
            for y in range(height):
                r, g, b, a = pixels[x, y]
                #print r,g,b
                if g==255 and b==127:
                    pixels[x,y] = (255,255,255,a)

    new_img.save("newnew.png")
    text = image_file_to_string("newnew.png")#read text from the image
    #new_img.show()
    text = text.split("\n")[1]
    text = "".join(text.split())
    #print text,

    ret = tn.read_until("Answer:")
    print ret,
    print text
    tn.write(text + "\n")
    ret = tn.read_all()
    print ret
    
if __name__ == "__main__":
    main()
