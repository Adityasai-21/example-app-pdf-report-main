import pdfkit
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(layout="centered", page_icon="🎓", page_title="Diploma Generator")
st.title("🎓 Diploma PDF Generator")

# Introduction
st.write(
    "This app shows you how you can use Streamlit to make a PDF generator app in just a few lines of code!"
)

# Create two columns for layout
left, right = st.columns(2)

# Display the template image
right.write("Here's the template we'll be using:")
right.image("template.png", width=300)

# Initialize Jinja2 template environment
env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")

# Left column for form input
left.write("Fill in the data:")
form = left.form("template_form")

# Form fields for student information
student = form.text_input("Student name")
course = form.selectbox(
    "Choose course",
    ["Report Generation in Streamlit", "Advanced Cryptography"],
    index=0,
)
grade = form.slider("Grade", 1, 100, 60)

# Checkbox to show/hide text in the PDF
show_text = form.checkbox("Show Text in PDF", True)

# Submit button
submit = form.form_submit_button("Generate PDF")

# Additional text and font size settings
st.text("Text and font size settings:")
text_to_display = st.text_input("Text to display")
font_size = st.slider("Font Size", 8, 36, 16)

if submit:
    # Generate the HTML content with Jinja2
    html = template.render(
        student=student,
        course=course,
        grade=f"{grade}/100",
        date=date.today().strftime("%B %d, %Y"),
    )

    # Add text and QR code to the HTML content if requested
    if show_text:
        html += f"<p>Student: {student}</p>"
        html += f"<p>Course: {course}</p>"
        html += f"<p>Grade: {grade}/100</p>"

    # Add additional text with specified font size
    if text_to_display:
        html += f"<p style='font-size: {font_size}px;'>{text_to_display}</p>"

    # Generate PDF from the HTML content
    pdf = pdfkit.from_string(html, False)

    # Display balloons animation
    st.balloons()

    # Success message and download button
    right.success("🎉 Your diploma was generated!")
    right.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name="diploma.pdf",
        mime="application/octet-stream",
    )

# Add text at the top-left corner
st.text("Text at the top-left corner of the page")

# Render text with specified font size
if text_to_display:
    st.write(text_to_display, {"fontSize": font_size})

