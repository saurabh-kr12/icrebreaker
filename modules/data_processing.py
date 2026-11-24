"""Module for processing LinkedIn profile data."""

import json
import logging
import os
from typing import Dict, List, Any, Optional

from llama_index.core import Document, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from modules.llm_interface import create_watsonx_embedding
import config

logger = logging.getLogger(__name__)

def split_profile_data(profile_data: Dict[str, Any]) -> List:
    """Splits the LinkedIn profile JSON data into nodes.
    
    Args:
        profile_data: LinkedIn profile data dictionary.
        
    Returns:
        List of document nodes.
    """
    try:
        # Convert the profile data to a JSON string
        documents = []
        for section_name, section_value in profile_data.items():
            if section_value in (None, "", [], {}):
                continue
            text = f"{section_name}: {json.dumps(section_value, ensure_ascii=False)}"
            documents.append(Document(
                text=text,
                metadata={"section": section_name, "source": "LinkedIn profile"}
            ))

        splitter = SentenceSplitter(chunk_size=config.CHUNK_SIZE)
        nodes = splitter.get_nodes_from_documents(documents)
        
        logger.info(f"Created {len(nodes)} nodes from profile data")
        return nodes
    except Exception as e:
        logger.error(f"Error in split_profile_data: {e}")
        return []


def create_vector_database(
    nodes: List,
    persist_dir: Optional[str] = None,
    collection_name: str = "linkedin_profiles",
) -> Optional[VectorStoreIndex]:
    """Stores the document chunks (nodes) in a vector database.
    
    Args:
        nodes: List of document nodes to be indexed.
        
    Returns:
        VectorStoreIndex or None if indexing fails.
    """
    try:
        embedding_model = create_watsonx_embedding()
        if persist_dir:
            os.makedirs(persist_dir, exist_ok=True)
            chroma_client = chromadb.PersistentClient(path=persist_dir)
            chroma_collection = chroma_client.get_or_create_collection(
                name=collection_name
            )
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            index = VectorStoreIndex(
                nodes=nodes,
                embed_model=embedding_model,
                storage_context=storage_context,
                show_progress=True,
            )
        else:
            index = VectorStoreIndex(
                nodes=nodes,
                embed_model=embedding_model,
                show_progress=True,
            )
        
        logger.info(
            "ChromaDB vector database created successfully"
            if persist_dir else "In-memory vector database created successfully"
        )
        return index
    except Exception as e:
        logger.error(f"Error in create_vector_database: {e}")
        return None


def verify_embeddings(index: VectorStoreIndex) -> bool:
    """Verify that all nodes have been properly embedded.
    
    Args:
        index: VectorStoreIndex to verify.
        
    Returns:
        True if all embeddings are valid, False otherwise.
    """
    try:
        vector_store = index._storage_context.vector_store
        node_ids = list(index.index_struct.nodes_dict.keys())
        missing_embeddings = False

        for node_id in node_ids:
            embedding = vector_store.get(node_id)
            if embedding is None:
                logger.warning(f"Node ID {node_id} has a None embedding.")
                missing_embeddings = True
            else:
                logger.debug(f"Node ID {node_id} has a valid embedding.")
        
        if missing_embeddings:
            logger.warning("Some node embeddings are missing")
            return False
        else:
            logger.info("All node embeddings are valid")
            return True
    except Exception as e:
        logger.error(f"Error in verify_embeddings: {e}")
        return False
