import os
from typing import Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import Batch
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import OptimizersConfigDiff


class Qdrant(QdrantClient):
    
    def __init__(self, url: Optional[str] = None, port: Optional[int] = 6333, grpc_port: int = 6334, prefer_grpc: bool = False, https: Optional[bool] = None, api_key: Optional[str] = None, prefix: Optional[str] = None, timeout: Optional[float] = None, host: Optional[str] = None, **kwargs: Any):
        super().__init__(url, port, grpc_port, prefer_grpc, https, api_key, prefix, timeout, host, **kwargs)

    def create_collection(self, collection_name, dim=768):
        self.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.DOT),
        )
        self.update_collection(collection_name=collection_name,
            optimizer_config=OptimizersConfigDiff(indexing_threshold=50000)
            )
        
    def get_points_count(self, collection_name):
        return self.get_collection(collection_name=collection_name).points_count

    def check_collection(self, collection):
        res = self.get_collection(collection_name=collection)
        return res.status == "green"

    def drop(self, name):
        self.delete_collection(collection_name=name)

    def insert_batch(self, rec, size=12):
        self.upsert(
                collection_name="hai",
                points=Batch(ids=rec["idx"], vectors=rec["vectors"], payloads=rec["payloads"]),
                wait=True,
            )
    
    def insert_one(self, rec, size=12):
        self.upsert(
                collection_name="hai",
                points=Batch(ids=rec["idx"], vectors=rec["vectors"], payloads=rec["payloads"]),
                wait=True,
            )
        
    def search_answer(self, l, topk=5):
        search_result = self.search(
            collection_name="hai",
            query_vector=l,
            # with_vectors=True,
            limit=topk
        )
        
        return search_result

if __name__ == "__main__":
    client = Qdrant(
        url=os.environ.get("QDRANT_URL"), 
        prefer_grpc=True,
        api_key=os.environ.get("QDRANT_API_TOKEN"),
    )
    client.drop("hai")
    
    client.create_collection("hai")
    print(client.check_collection("hai"))

    del client