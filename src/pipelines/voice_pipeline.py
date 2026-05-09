from  resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np 
import io 
import librosa
import streamlit as st 


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio_array, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000 )
        wav = preprocess_wav(audio_array)
        embedding = encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return None
    
def identify_speaker(new_embbeding, candidate_dict, threshold = 0.65):
    if new_embbeding is None or not candidate_dict:
        return None
    
    best_sid = None
    best_score = -1.0
    
    for sid, stored_embedding in candidate_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embbeding, stored_embedding) / (np.linalg.norm(new_embbeding) * np.linalg.norm(stored_embedding))
            if similarity > best_score:
                best_score = similarity
                best_sid = sid
    
    if best_score >= threshold:
        return best_sid, best_score
    else:
        return None, best_score
    
    
def process_bulk_audio(audio_bytes, candidate_dict, threshold = 0.65):
    try:
        encoder = load_voice_encoder()
        audio_array, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000 )
        segments = librosa.effects.split(audio_array, top_db=30)
        
        indentified_results = {}
        for start, end in segments:
            if (end-start) < sr * 0.5:
                continue
            
            segment_audio = audio_array[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)
            sid, score = identify_speaker(embedding, candidate_dict, threshold)
            if sid:
                if sid not in indentified_results or score > indentified_results[sid]:
                    indentified_results[sid] = score
                    
        
        return indentified_results
    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return None

    

    


    