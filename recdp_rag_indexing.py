from pyrecdp.primitives.operations import DirectoryLoader, DocumentSplit, DocumentIngestion
from pyrecdp.LLM import TextPipeline
import os

def load_embedding_path():
    # Create embeddings and store in vectordb
    if ('RECDP_CACHE_HOME' not in os.environ) or (not os.environ['RECDP_CACHE_HOME']):
        os.environ['RECDP_CACHE_HOME'] = os.path.join(os.getcwd(), "models")
    #embedding_model_name = "sentence-transformers/all-mpnet-base-v2"
    embedding_model_name = "all-MiniLM-L6-v2"
    local_embedding_model_path = os.path.join(os.environ['RECDP_CACHE_HOME'], embedding_model_name)
    print(local_embedding_model_path)
    if os.path.exists(local_embedding_model_path):
        return local_embedding_model_path
    else:
        raise FileNotFoundError(local_embedding_model_path)

def main(folder, db_location): 
    embeddings_path = load_embedding_path()
    pipeline = TextPipeline()
    ops = [
        DirectoryLoader(folder, glob="**/*.pdf"),
        DocumentSplit(),
        DocumentIngestion(
            vector_store='chroma',
            vector_store_args={
                "output_dir": db_location
            },
            embeddings='HuggingFaceEmbeddings',
            embeddings_args={
                'model_name': embeddings_path
            },
        ),
    ]
    pipeline.add_operations(ops)
    pipeline.execute()
    
if __name__ == "__main__":   
    import argparse
    import os

    parser = argparse.ArgumentParser(
        description="script to run RAG indexing", add_help=True
    )
    parser.add_argument(
        "--folder", default="intel_on", type=str, help="folder to do rag indexing"
    )
    parser.add_argument(
        "--db_location", default="intel_on_db", type=str, help="folder to do rag indexing"
    )
    args = parser.parse_args()
    main(args.folder, args.db_location)