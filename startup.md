Start qdrant
```
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant:latest
```

Start backend
```
uvicorn main:app --port 8001 --reload
```

Add backend url to .env

For ingesting files to the vector db knowledge base
```
python -m rag.ingest --uploads
```

