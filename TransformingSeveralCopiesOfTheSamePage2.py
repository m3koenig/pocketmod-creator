from pypdf import PdfReader, PdfWriter, Transformation, PaperSize

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
    print("width_in_points: " + str(width_in_points))

    # # Get height in points
    # width_in_height = sourcepage.mediabox.upper_right[0]
    # print("width_in_height: " + str(width_in_height))

    width = 300 #width_in_points/3.5 #300
    height = 600
    # print("width: " + str(width))    


    #  Inside Page 1 | Inside Page 2 | Inside Page 3 | Inside Page 4 |
    # -------------- | ------------- | ------------- | ------------- |
    #  Right Flap    | Back Cover    | Front Cover   | Left Flap     |

    if pageNo == 1:
        # Right Flap
        x = 5
        y = 10
    if pageNo == 7:
        # Back Cover
        x = 215
        y = 10
    if pageNo == 0:
        # Front Cover
        x = 415
        y = 10
    if pageNo == 2:
        # Left Flap
        x = 615
        y = 10
    
    if pageNo == 6:
        # Inside Page 4
        x = 5
        y = 300
    if pageNo == 4:
        # Inside Page 3
        x = 215
        y = 300  
    if pageNo == 3:
        # Inside Page 2
        x = 415
        y = 300 
    if pageNo == 5:
        # Inside Page 4
        x = 615
        y = 300
    
    print("Page: " + str(pageNo))    
    print(">x: " + str(x))    
    print(">y: " + str(y))    

    # print("sourcepage.mediabox.width: " + str(sourcepage.mediabox.width))
    # print("sourcepage.mediabox.height: " + str(sourcepage.mediabox.height))
    

    # Transformation().rotate(10).translate( # rotate without cut
    # if pageNo == 1 or pageNo == 7 or pageNo == 0 or pageNo == 2:
    # if pageNo == 0 or pageNo == 7:
    # if pageNo == 1 or pageNo == 7 or pageNo == 0:
    # if pageNo == 0:
    destpage.merge_transformed_page(
        sourcepage,
        Transformation().translate(
            x,
            y,
        ),
    )

# Write file
with open("output.pdf", "wb") as fp:
    writer.write(fp)
