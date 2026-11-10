"""
Regulatory Document Retriever for Anna-Setu RAG Pipeline.
Indexes FSSAI and Lucknow Nagar Nigam statutory texts and performs
semantic & keyword retrieval using TF-IDF and Cosine Similarity.
"""

import os
import json
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class RegulatoryRetriever:
    """
    Retrieves official food safety clauses and municipal directives
    from FSSAI (2019) and Lucknow Nagar Nigam (LNN) knowledge bases.
    """

    def __init__(self, kb_dir: Optional[str] = None):
        if kb_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.kb_dir = os.path.join(base_dir, "knowledge_base")
        else:
            self.kb_dir = kb_dir

        self.documents: List[Dict[str, Any]] = []
        self.doc_texts: List[str] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None

        self._load_knowledge_base()
        self._build_index()

    def _load_knowledge_base(self):
        """Loads FSSAI and LNN statutory guidelines from JSON stores."""
        fssai_path = os.path.join(self.kb_dir, "fssai_guidelines.json")
        lnn_path = os.path.join(self.kb_dir, "lnn_guidelines.json")

        # Load FSSAI regulations
        if os.path.exists(fssai_path):
            with open(fssai_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                authority = data.get("authority", "FSSAI")
                framework = data.get("framework", "FSSAI Surplus Regulations 2019")
                for item in data.get("guidelines", []):
                    item["source_authority"] = authority
                    item["framework"] = framework
                    item["source_type"] = "FSSAI"
                    self.documents.append(item)

        # Load Lucknow Nagar Nigam bylaws
        if os.path.exists(lnn_path):
            with open(lnn_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                authority = data.get("authority", "Lucknow Nagar Nigam")
                framework = data.get("framework", "LNN Sanitation & Food By-Laws")
                for item in data.get("guidelines", []):
                    item["source_authority"] = authority
                    item["framework"] = framework
                    item["source_type"] = "LNN"
                    self.documents.append(item)

        # Prepare unified search documents
        for doc in self.documents:
            searchable_text = (
                f"{doc.get('title', '')} "
                f"{doc.get('clause', '')} "
                f"{doc.get('text', '')} "
                f"{' '.join(doc.get('keywords', []))} "
                f"{doc.get('category', '')} "
                f"{doc.get('source_type', '')}"
            )
            self.doc_texts.append(searchable_text)

    def _build_index(self):
        """Builds a TF-IDF vector matrix over the loaded regulatory documents."""
        if not self.doc_texts:
            return

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            stop_words="english",
            lowercase=True,
            sublinear_tf=True
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.doc_texts)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        filter_source: Optional[str] = None,
        min_score: float = 0.05
    ) -> List[Dict[str, Any]]:
        """
        Executes semantic retrieval for relevant regulatory clauses given a query.
        
        Args:
            query: Natural language query or scenario terms (e.g. "cooked rice holding time ambient")
            top_k: Number of highest ranking clauses to retrieve
            filter_source: Optional filter ('FSSAI' or 'LNN')
            min_score: Minimum cosine similarity score threshold
        
        Returns:
            List of matching regulation documents with similarity scores
        """
        if not self.vectorizer or self.tfidf_matrix is None or not self.documents:
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        # Sort indices by descending similarity score
        ranked_indices = np.argsort(similarities)[::-1]

        results = []
        for idx in ranked_indices:
            score = float(similarities[idx])
            doc = self.documents[idx]

            # Apply source filter if specified
            if filter_source and doc.get("source_type") != filter_source:
                continue

            if score < min_score and len(results) >= 1:
                # If we already have at least 1 result and score is below cutoff, break
                break

            doc_result = dict(doc)
            doc_result["relevance_score"] = round(score, 4)
            results.append(doc_result)

            if len(results) >= top_k:
                break

        return results

    def get_by_id(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """Direct lookup of a specific regulation clause by ID."""
        for doc in self.documents:
            if doc.get("id") == rule_id:
                return dict(doc)
        return None

