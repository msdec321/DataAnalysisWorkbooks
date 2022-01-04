import os
from datetime import date

from pptx import Presentation
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN


# Delete the powerpoint if it already exists
if os.path.exists(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Covid19_dashboard.pptx"):
    os.remove(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Covid19_dashboard.pptx")
    
    
# Initialize a presentation object (Note: close all open instances of powerpoint)
prs = Presentation()

# Set slide dimensions to widescreen
prs.slide_width = Inches(16)
prs.slide_height = Inches(9)

# Other configs
slide_numbers = True
rice_logo = True


# Useful functions

def slide_title(l, t, w, h, text, textFont, textSize):  # Text for title slide
    left = Inches(l)
    top = Inches(t)
    width = Inches(w)
    height = Inches(h)
    
    text_box = slide.shapes.add_textbox(left, top, width, height)
    tb = text_box.text_frame
    tb.word_wrap = True
    
    p = tb.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    
    font = run.font
    font.name = textFont
    font.size = Pt(textSize)
    
    return None


def slide_image(img_name, l, t, w, slideTitle, caption):
    
    path = 'C:/Users/Matth/git/DataAnalysisWorkbooks/Covid19/Figures/' + img_name + '.png'
    
    left = l
    top = t
    img = slide.shapes.add_picture(path, left, top, w)
    
    slide_title(2.3, 0.6, 11, 3, slideTitle, 'Arial', 35)  # Title
    slide_title(1.6, 6.6, 13, 5, caption, 'Arial', 25)
    
    return None


# Title slide

blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

slide_title(2.3, 2.45, 11, 3, 'Covid-19 Daily Statistics Dashboard', 'Arial', 60)  # Title
slide_title(3.5, 5, 8.4, 3, 'Matthew Decaro, Rice University', 'Arial', 30)  # Subtitle (name)
slide_title(3.5, 7.3, 8.4, 3, date.today().strftime('%B %#d, %Y'), 'Arial', 30) # Date


# Create a basic image slide with a caption

# Image slides (Note: blade_slide_layout cannot be called in a function. Must manually call it each time a new slide is made.)
continents = ['Africa', 'Asia', 'Europe', 'NorthAmerica', 'SouthAmerica', 'Oceania']
cont_caption = ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']

for i, continent in enumerate(continents):
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    slide_image(f'newCases_{continent}', Inches(0.1), Inches(1.2), Inches(15.4), f'Daily Covid-19 Cases in {cont_caption[i]}', 
                'Caption: This is a caption for my image. This is a caption for my image. This is a caption for my image. This is a caption for my image.')

    
for i, continent in enumerate(continents):
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)
    slide_image(f'newDeaths_{continent}', Inches(0.1), Inches(1.2), Inches(15.4), f'Daily Covid-19 Deaths in {cont_caption[i]}', 
                'Caption: This is a caption for my image. This is a caption for my image. This is a caption for my image. This is a caption for my image.')

    
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)
slide_image('rollingCases_Africa', Inches(0.1), Inches(1.2), Inches(15.4), 'Total Covid-19 Cases in Africa', 
           'Caption: This is a caption for my image. This is a caption for my image. This is a caption for my image. This is a caption for my image.')


blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)
slide_image('rollingDeaths_Africa', Inches(0.1), Inches(1.2), Inches(15.4), 'Total Covid-19 Cases in Africa', 
           'Caption: This is a caption for my image. This is a caption for my image. This is a caption for my image. This is a caption for my image.')



# Add slide numbers to footers

if slide_numbers:
    slides = prs.slides

    # Hand-picked positions based on choice of slide size (widescreen) and fontsize (27)
    left = Inches(15.1)
    top = Inches(8.1)
    width = Inches(1)
    height = Inches(1)

    for slide in slides:
        if slides.index(slide) == 0: continue  # Skip labelling the title slide number as '0'

        # Initialize the text box. Set the text, font, and fontsize
        text_box = slide.shapes.add_textbox(left, top, width, height)
        tb = text_box.text_frame
        
        p = tb.paragraphs[0]
        run = p.add_run()
        run.text = str(slides.index(slide))
        
        font = run.font
        font.name = 'Arial'
        font.size = Pt(27)
        
        #TODO: Add a toggle for other slide number positions (bottom left, bottom center, etc.)


skip_slides = []  # Add slides to skip logo here.

if rice_logo:
    slides = prs.slides

    # Hand-picked positions based on choice of slide size (widescreen) and fontsize (27)
    left = Inches(0.3)
    top = Inches(0.2)
    path = r"C:\Users\Matth\Documents\saved_images\rice_logo.png"

    for index, slide in enumerate(slides):
        if index in skip_slides: continue
        img = slide.shapes.add_picture(path, left, top)
        
        #TODO: Add a toggle for other logo positions (top-right, bottom-left, etc.)        
        
prs.save(r"C:\Users\Matth\git\DataAnalysisWorkbooks\Covid19\Covid19_dashboard.pptx")  # Save the file