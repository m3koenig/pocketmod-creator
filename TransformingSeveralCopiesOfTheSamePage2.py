from pypdf import PdfReader, PdfWriter, Transformation, PaperSize

# Read source file
reader = PdfReader("input.pdf")

# Create a destination file, and add a blank page for each source page
writer = PdfWriter()
destpage = writer.add_blank_page(width=PaperSize.A4.height, height=PaperSize.A4.width)
for i in range(len(reader.pages)):  # Loop through all source pages
    # Copy the current source page to the destination page, 16 times in a grid
    sourcepage = reader.pages[i]

    # Scale
    scale = 0.3 #scale and width calc...does not work well...
    op = Transformation().scale(sx=scale, sy=scale)
    sourcepage.add_transformation(op)
    
    # Get width in points
    width_in_points = sourcepage.mediabox.upper_right[0] - sourcepage.mediabox.upper_left[0]
    print("width_in_points: " + str(width_in_points))

    width = width_in_points/3.5 #300
    height = 180
    print("width: " + str(width))    

    x = (width) * i
    y = height

    print("sourcepage.mediabox.width: " + str(sourcepage.mediabox.width))
    print("sourcepage.mediabox.height: " + str(sourcepage.mediabox.height))
    

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
