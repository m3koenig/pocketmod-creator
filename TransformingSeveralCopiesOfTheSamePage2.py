import datetime

from pypdf import PdfReader, PdfWriter, Transformation, PaperSize
from pypdf.annotations import Line

# Read source file
reader = PdfReader("input.pdf")

# Create a destination file, and add a blank page for each source page
writer = PdfWriter()
destpage = writer.add_blank_page(width=PaperSize.A4.height, height=PaperSize.A4.width)
for pageNo in range(len(reader.pages)):  # Loop through all source pages
    # Copy the current source page to the destination page, 16 times in a grid
    sourcepage = reader.pages[pageNo]

    # Scale
    # 0.3528 is the mm approximation of 1/72 of an inch
    # PyPDF2 uses increments of 1/72 of an inch for sizing
    scale = 0.3528
    op = Transformation().scale(sx=scale, sy=scale)
    sourcepage.add_transformation(op)
    
    # Get width in points
    width_in_points = sourcepage.mediabox.upper_right[0] - sourcepage.mediabox.upper_left[0]
    # print("width_in_points: " + str(width_in_points))

    # # Get height in points
    # width_in_height = sourcepage.mediabox.upper_right[0]
    # print("width_in_height: " + str(width_in_height))

    width = 300
    height = 600
    # print("width: " + str(width))    


    #  Inside Page 1 | Inside Page 2 | Inside Page 3 | Inside Page 4 |
    # -------------- | ------------- | ------------- | ------------- |
    #  Right Flap    | Back Cover    | Front Cover   | Left Flap     |

    upperY = 590
    lowerY = 0

    lowerStartX = 0
    lowerNextPartX = 200

    upperStartX = 200
    upperNextPartX = 200

    if pageNo == 1:
        # Right Flap
        x = lowerStartX
        y = lowerY
        rotation = 0
    if pageNo == 7:
        # Back Cover
        x = lowerStartX + (lowerNextPartX * 1)
        y = lowerY
        rotation = 0
    if pageNo == 0:
        # Front Cover
        x = lowerStartX + (lowerNextPartX * 2)
        y = lowerY
        rotation = 0
    if pageNo == 2:
        # Left Flap
        x = lowerStartX + (lowerNextPartX * 3)
        y = lowerY
        rotation = 0
    
    if pageNo == 6:
        # Inside Page 1
        x = upperStartX + (upperNextPartX * 0)
        y = upperY
        rotation = 180
    if pageNo == 4:
        # Inside Page 3
        x = upperStartX + (upperNextPartX * 1)
        y = upperY
        rotation = 180
    if pageNo == 3:
        # Inside Page 2
        x = upperStartX + (upperNextPartX * 2)
        y = upperY
        rotation = 180
    if pageNo == 5:
        # Inside Page 4
        # x = 820 # -200  if not rotated
        x = upperStartX + (upperNextPartX * 3)
        y = upperY # half if not rotated
        rotation = 180
    
    print("Page: " + str(pageNo))    
    print(">x: " + str(x))    
    print(">y: " + str(y))    
    print(">rotation: " + str(rotation))    

    # print("sourcepage.mediabox.width: " + str(sourcepage.mediabox.width))
    # print("sourcepage.mediabox.height: " + str(sourcepage.mediabox.height))
    

    # Transformation().rotate(10).translate( # rotate without cut
    # if pageNo == 1 or pageNo == 7 or pageNo == 0 or pageNo == 2:
    # if pageNo == 0 or pageNo == 7:
    # if pageNo == 1 or pageNo == 7 or pageNo == 0:
    # if pageNo == 0:    
    destpage.merge_transformed_page(
        sourcepage,
        Transformation().rotate(rotation).translate(
            x,
            y,
        ),
    )




# Get page width and height
page_width = destpage.artbox.width
page_height = destpage.artbox.height

# Calculate fold line coordinates
fold_lines = []
for i in range(1, 4):
    fold_lines.append((i * page_width / 4, 0, i * page_width / 4, page_height))  # Horizontal lines

for i in range(1, 2):
    fold_lines.append((0, i * page_height / 2, page_width, i * page_height / 2))  # Vertical lines
    
# Add fold lines as annotations
for start_x, start_y, end_x, end_y in fold_lines:
    annotation = Line(
        rect=(start_x, start_y, end_x, end_y),
        p1=(start_x, start_y),
        p2=(end_x, end_y)
    )
    writer.add_annotation(page_number=0, annotation=annotation)


        

# Write file
current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
output_pdf = 'output_{}.pdf'.format(current_time)
with open(output_pdf, "wb") as fp:
    writer.write(fp)

