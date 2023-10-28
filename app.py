import streamlit as st
from transformers import pipeline

# Load model
model = pipeline("summarization")

# Function to split text into chunks
def generate_chunks(inp_str):
    max_chunk = 500
    inp_str = inp_str.replace('.', '.<eos>')
    inp_str = inp_str.replace('?', '?<eos>')
    inp_str = inp_str.replace('!', '!<eos>')
    
    sentences = inp_str.split('<eos>')
    current_chunk = 0 
    chunks = []
    for sentence in sentences:
        if len(chunks) == current_chunk + 1: 
            if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                chunks[current_chunk].extend(sentence.split(' '))
            else:
                current_chunk += 1
                chunks.append(sentence.split(' '))
        else:
            chunks.append(sentence.split(' '))

    for chunk_id in range(len(chunks)):
        chunks[chunk_id] = ' '.join(chunks[chunk_id])
    return chunks


st.title("Summarize Text")
sentence = st.text_area('Please paste your article :', height=30)
button = st.button("Summarize")

max = st.sidebar.slider('Select max', 50, 500, step=10, value=150)
min = st.sidebar.slider('Select min', 10, 450, step=10, value=50)
do_sample = st.sidebar.checkbox("Do sample", value=False)
with st.spinner("Generating Summary.."):
    if button and sentence:
        chunks = generate_chunks(sentence)
        res = model(chunks,
                         max_length=max, 
                         min_length=min, 
                         do_sample=do_sample)
        text = ' '.join([summ['summary_text'] for summ in res])
        st.write(text)
