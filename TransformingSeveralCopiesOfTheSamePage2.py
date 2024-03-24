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
    scale = 0.4 #scale and width calc...does not work well...
    op = Transformation().scale(sx=scale, sy=scale)
    sourcepage.add_transformation(op)
    
    # Get width in points
    width_in_points = sourcepage.mediabox.upper_right[0] - sourcepage.mediabox.upper_left[0]
    # print("width_in_points: " + str(width_in_points))

    width = 300 #width_in_points/3.5 #300
    height = 600
    # print("width: " + str(width))    

    if pageNo == 0:
        x = 5
        y = -30
    if pageNo == 1:
        x = 205
        y = -30
    if pageNo == 2:
        x = 405
        y = -30
    if pageNo == 3:
        x = 605
        y = -30
    
    if pageNo == 4:
        x = 0
        y = 260   
    if pageNo == 5:
        x = 200
        y = 260    
    if pageNo == 6:
        x = 400
        y = 260  
    if pageNo == 7:
        x = 600
        y = 260
    
    print("Page: " + str(pageNo))    
    print(">x: " + str(x))    
    print(">y: " + str(y))    

    # print("sourcepage.mediabox.width: " + str(sourcepage.mediabox.width))
    # print("sourcepage.mediabox.height: " + str(sourcepage.mediabox.height))
    

    # Transformation().rotate(10).translate( # rotate without cut
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
