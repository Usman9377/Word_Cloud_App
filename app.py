import streamlit as st

from wordcloud import WordCloud, STOPWORDS

import matplotlib.pyplot as plt

import pandas as pd

import PyPDF2

from docx import Document

from io import BytesIO

import base64



# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Word Cloud Generator",
    layout="wide"
)



# -----------------------------
# FILE READING FUNCTIONS
# -----------------------------


def read_text(file):

    return file.getvalue().decode(
        "utf-8",
        errors="ignore"
    )



def read_pdf(file):

    pdf_reader = PyPDF2.PdfReader(file)

    text = ""

    for page in pdf_reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text


    return text




def read_docx(file):

    doc = Document(file)

    text = ""


    for para in doc.paragraphs:

        text += para.text + "\n"


    return text





# -----------------------------
# STOP WORD FUNCTION
# -----------------------------


def filter_stop_words(
        text,
        additional_stop_words=[]
):


    words = text.split()


    stop_words = STOPWORDS.union(
        set(additional_stop_words)
    )


    filtered = [

        word

        for word in words

        if word.lower() not in stop_words

    ]


    return " ".join(filtered)




# -----------------------------
# WORD FREQUENCY
# -----------------------------


def word_frequency(text):


    words=text.split()


    freq=pd.Series(words).value_counts()


    df=pd.DataFrame(

        {
        "Word":freq.index,
        "Frequency":freq.values
        }

    )


    return df




# -----------------------------
# DOWNLOAD WORD CLOUD
# -----------------------------


def download_image(fig):


    buffer=BytesIO()


    fig.savefig(

        buffer,

        format="png",

        bbox_inches="tight"

    )


    buffer.seek(0)


    return buffer




# -----------------------------
# STREAMLIT APP
# -----------------------------


st.title(
    "☁️ Word Cloud Generator"
)


st.write(

"Upload TXT, PDF or Word document to generate word cloud"

)



uploaded_file = st.file_uploader(

    "Upload File",

    type=[
        "txt",
        "pdf",
        "docx"
    ]

)



additional_words = st.text_input(

    "Additional Stop Words (comma separated)"

)



if uploaded_file:


    try:


        # Read file


        if uploaded_file.type=="text/plain":


            text=read_text(
                uploaded_file
            )


        elif uploaded_file.type=="application/pdf":


            text=read_pdf(
                uploaded_file
            )


        else:


            text=read_docx(
                uploaded_file
            )




        st.subheader(
            "Original Text"
        )


        st.text_area(

            "Text",

            text,

            height=200

        )




        # Stop words


        extra=[]


        if additional_words:


            extra=[

                x.strip()

                for x in additional_words.split(",")

            ]



        cleaned_text=filter_stop_words(

            text,

            extra

        )




        # Generate WordCloud


        wordcloud=WordCloud(

            width=900,

            height=500,

            background_color="white"

        ).generate(cleaned_text)



        fig,ax=plt.subplots()


        ax.imshow(

            wordcloud,

            interpolation="bilinear"

        )


        ax.axis("off")



        st.subheader(

            "Generated Word Cloud"

        )


        st.pyplot(fig)



        # Download Image


        image_buffer=download_image(fig)


        st.download_button(

            "Download Word Cloud",

            image_buffer,

            file_name="wordcloud.png",

            mime="image/png"

        )




        # Frequency table


        st.subheader(

            "Word Frequency"

        )


        freq_df=word_frequency(

            cleaned_text

        )



        st.dataframe(

            freq_df

        )




        csv=freq_df.to_csv(

            index=False

        ).encode()



        st.download_button(

            "Download Word Frequency CSV",

            csv,

            "word_frequency.csv",

            "text/csv"

        )



    except Exception as e:


        st.error(

            f"Error: {e}"

        )
