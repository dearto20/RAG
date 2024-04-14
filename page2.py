import streamlit as st
import llmmanager
import pandas as pd

db = llmmanager.get_database()

def get_chunk_infos(query):
    query_embedding = llmmanager.get_embedding(query)
    collection = db.get_or_create_collection('context')
    result = collection.peek(0)
    chunk_infos = []
    for id, embedding, metadata in zip(result['ids'], result['embeddings'], result['metadatas']):
        chunk_infos.append([llmmanager.get_distance(query_embedding, embedding), metadata['chunk'], metadata['sentence'], metadata['source']])
    chunk_infos.sort(key=lambda x: x[0])
    return chunk_infos[:100]

def app():
    st.title('Retrieve Context and Query the LLM')
    st.write('Enter a Query to Ask the LLM')

    query = st.text_input('Query')
    if query:
        print('Query: ', query)
        chunk_infos = get_chunk_infos(query)
        chunk_infos = chunk_infos[:10]
    else:
        return

    st.write('Top 10 Chunks with Highest Similarity from Personal Context')
    st.table(pd.DataFrame(chunk_infos, columns=['distance', 'chunk', 'sentence', 'source']))

    query_type = st.radio("Ask the LLM", ["With RAG", "Don't Use RAG"])
    prompt = ''
    if query_type == "With RAG":
        visited = set()
        context = []
        for chunk_info in chunk_infos:
            current_context = chunk_info[1]
            if current_context in visited:
                continue
            visited.add(current_context)
            context.append(current_context)
        queried_context = '\n'.join(['- ' + chunk_info for chunk_info in context])
        prompt += f'Based on Queried Context,\n\n{queried_context}\n\n'
    prompt += f'Answer the Question, {query}'
    st.write(prompt)
    st.divider()
    answer = llmmanager.get_completions(prompt)
    st.write(answer)
