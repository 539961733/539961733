# Generate captchas
import random
import numpy as np
import cv2
from PIL import Image,ImageDraw,ImageFont,ImageFilter
# picture saving address
filepath="D:/python project/ECEN765_Project/train/"
# font address
font_path = 'C:/Windows/Fonts/Georgia.ttf'
# number of characters in the captcha
number = 4
# the size of captcha
size = (129,53)
# background color (White)
bgcolor = (255,255,255)
# font color (Black)
fontcolor = (0,0,0)
# line color (Black)
linecolor = (0,0,0)
# line exists or not
draw_line = True

dict = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,\
        'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, \
        'H':0, 'I':0, 'J':0, 'K':0, 'L':0, 'M':0, 'N':0,\
        'O':0, 'P':0, 'Q':0, 'R':0, 'S':0, 'T':0,\
        'U':0, 'V':0, 'W':0, 'Z':0,'X':0, 'Y':0}
# Generate random string
def gene_text():
    source = ['0','1','2','3','4','5','6','7','8','9','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I','J', 'K','L', 'M', 'N','O','P','Q','R',
              'S', 'T', 'U', 'V', 'W', 'Z','X', 'Y']
    return ''.join(random.sample(source,number))

# Generate line
def gene_line(draw,width,height):
    begin = (0, random.randint(0, height))
    end = (74, random.randint(0, height))
    draw.line([begin, end], fill = linecolor,width=3)

# Generate captcha
def gene_captcha (text,line_number):  # get string
    width, height = size
    image = Image.new('RGBA',(width,height),bgcolor) # new picture
    font = ImageFont.truetype(font_path,40) # type of captcha
    draw = ImageDraw.Draw(image)
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number),text,
            font= font,fill=fontcolor) # fill string
    if draw_line:
        index = 1
        while index <= line_number:
            gene_line(draw,width,height)
            index += 1
        index = 0
    image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  # change captcha
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) # get filter
    aa = str(".png")
    path = filepath + text + aa  # picture path
    image.save(path)
    return text

# Generate captcha return the label
def gene_captcha_set(setsize,text,random,line_number):
    if random == 1 :
        index = 1
        label = []
        while index < setsize + 1:
            text_random = gene_text()
            label.append( gene_captcha(text_random,line_number))
            index = index + 1
        return label  # label is the list of string
    else :
        gene_captcha(text,line_number)
        return text

# Transfer png picture to binary picture
def get_dynamic_binary_image(label):
    filename = filepath + label + '_binary1.jpg'
    img_name = filepath + label + '.png'
    im = cv2.imread(img_name)
    im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    #  Transfer to binary
    th1 = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    #cv2.imwrite(filename,th1)
    return th1  # the picture is 63* 159 picture 0-black 255- white

# delete the frame of captcha
def delete_frame(label,jpg_picture):
    test_data_size = 1  # data size
    test_label = gene_captcha_set(test_data_size,'    ',0,0) # data label
    frame = get_dynamic_binary_image(test_label)
    no_frame_picture =1-(jpg_picture//255) ^ (frame//255)
    filename = filepath + label + '_binary.jpg'
    #cv2.imwrite(filename,(no_frame_picture)*255)
    return no_frame_picture

# test for dividing digits
def divide_digit(label,no_frame_picture):
    width = len(no_frame_picture)
    index = 0
    divide_picture = []
    while index < width :
        divide_picture.append(no_frame_picture[index][10:130])
        index += 1
    divide_picture=np.array(divide_picture)
    filename = filepath + label + '_divide.jpg'
    #cv2.imwrite(filename,divide_picture*255)
    return divide_picture

# dive picture to 4 digits
def divide_four_digits(label,divide_picture):
    # picture size is 119 columns * 63 rows
    # matrix_whole=np.array(divide_picture) # make the list to matrix
    four_digits = []
    index = 0
    data=np.array(divide_picture)
    data_test = []
    label_list=list(label)
    while index < 4 :
        temp_digit = []
        for rows in data :
             temp_digit.append( rows[index*30:(index+1)*30])
        four_digits.append(np.array(temp_digit))
        index += 1
    return label_list,four_digits


# Main program
def main():
    # number of lines
    line_number = random.randint(1,3)
    # picture number
    picture_number = 200
    label = gene_captcha_set(picture_number-1,'    ',1,line_number)
    print('txt starts')
    for index in label :
        jpg = get_dynamic_binary_image(index)
        no_frame = delete_frame(index,jpg)
        divide_pic = divide_digit(index,no_frame)
        [digits_label,digit_matrix]=divide_four_digits(index,divide_pic)
        index1=0
        while index1 < 4:
            dict[digits_label[index1]]+= 1
            filename_txt = filepath +digits_label[index1] +'_ '+str(dict[digits_label[index1]])+'.txt'
            np.savetxt(filename_txt,digit_matrix[index1],fmt='%d',delimiter=" ")
            index1 +=1
    for char,numbers in dict.items():
        if numbers == 0 :
            print(char)
main()
