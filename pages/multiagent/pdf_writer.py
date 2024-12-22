import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    ListFlowable, ListItem
)
from reportlab.graphics.shapes import Drawing, Line

def generate_pdf(data):
    """Generate a PDF file from the json data"""
    title = re.sub(r'[^a-zA-Z0-9]', '_', data['header'])
    filename = title + '.pdf'
    pdf = SimpleDocTemplate(filename, pagesize=A4, title=title)

    styles = getSampleStyleSheet()
    story = []
    line = Drawing(450, 1)
    line.add(Line(0, 0, 450, 0))

    header = Paragraph(data['header'], styles['Title'])
    story.append(header)
    story.append(Spacer(1, 6))

    entry_paragraphs = parse_content(data['entry'], styles)
    story.extend(entry_paragraphs)
    story.append(Spacer(1, 6))

    for para in data['paragraphs']:
        sub_header = Paragraph(para['sub_header'], styles['Heading2'])
        story.append(sub_header)
        story.append(Spacer(1, 3))

        paragraph_content = parse_content(para['paragraph'], styles)
        story.extend(paragraph_content)
        story.append(Spacer(1, 6))

    # Conclusion
    conclusion_title = Paragraph('Conclusion', styles['Heading2'])
    story.append(conclusion_title)
    conclusion_content = parse_content(data['conclusion'], styles)
    story.extend(conclusion_content)
    story.append(Spacer(1, 6))

    # Summary
    summary_title = Paragraph('Summary', styles['Heading2'])
    story.append(summary_title)
    summary_content = parse_content(data['summary'], styles)
    story.extend(summary_content)
    story.append(Spacer(1, 6))

    story.append(line)
    story.append(Spacer(1, 3))

    seo_keywords = Paragraph("Seo Keywords: " + ", ".join(data['seo_keywords']), styles['BodyText'])
    story.append(seo_keywords)
    pdf.build(story)

    return filename

def parse_content(text, styles):
    """
    Parses the text and identifies bullet points to be converted into lists.
    """
    elements = []
    lines = text.split('\n')
    buffer = []

    ul_items = []

    for line in lines:
        line = line.strip()
        if line.startswith('- '):  # Detect bullet points
            # Add any buffered text as a paragraph before starting a list
            if buffer:
                paragraph = Paragraph(' '.join(buffer), styles['BodyText'])
                elements.append(paragraph)
                buffer = []
            # Add the bullet point to the list
            bullet_text = line[2:].strip()
            ul_items.append(ListItem(Paragraph(bullet_text, styles['BodyText'])))
        else:
            # If there is an existing list and we reach non-list text, add the list to elements
            if ul_items:
                bullet_list = ListFlowable(ul_items, bulletType='bullet', start='bulletchar')
                elements.append(bullet_list)
                ul_items = []
            buffer.append(line)

    # Add any remaining list items or text
    if ul_items:
        bullet_list = ListFlowable(ul_items, bulletType='bullet', start='bulletchar')
        elements.append(bullet_list)
    elif buffer:
        paragraph = Paragraph(' '.join(buffer), styles['BodyText'])
        elements.append(paragraph)

    return elements

'''from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.graphics.shapes import Drawing, Line
import re

def generate_pdf(data):
    """Generate a PDF file from the json data"""
    title = re.sub(r'[^a-zA-Z0-9]', '_', data['header'])
    filename = title + '.pdf'
    pdf = SimpleDocTemplate(filename, pagesize=A4, title=title)

    styles = getSampleStyleSheet()
    story = []
    line = Drawing(450, 1)
    line.add(Line(0, 0, 450, 0))

    header = Paragraph(data['header'], styles['Title'])
    story.append(header)
    story.append(Spacer(1, 6))

    entry = Paragraph(data['entry'], styles['BodyText'])
    story.append(entry)
    story.append(Spacer(1, 6))

    for para in data['paragraphs']:
        sub_header = Paragraph(para['sub_header'], styles['Heading2'])
        paragraph = Paragraph(para['paragraph'], styles['BodyText'])

        story.append(sub_header)
        story.append(Spacer(1, 3))
        story.append(paragraph)
        story.append(Spacer(1, 6))

    conclusion_title = Paragraph('Conclusion', styles['Heading2'])
    conclusion = Paragraph(data['conclusion'], styles['BodyText'])
    story.append(conclusion_title)
    story.append(conclusion)
    story.append(Spacer(1, 6))

    summary_title = Paragraph('Summary', styles['Heading2'])
    summary = Paragraph(data['summary'], styles['BodyText'])
    story.append(summary_title)
    story.append(summary)
    story.append(Spacer(1, 6))

    story.append(line)
    story.append(Spacer(1, 3))
    seo_keywords = Paragraph("Seo Keywords: "+", ".join( data['seo_keywords']), styles['BodyText'])
    story.append(seo_keywords)
    pdf.build(story)

    return filename
'''