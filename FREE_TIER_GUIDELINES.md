# Free-Tier Resource Guidelines

This document outlines how the AI-Native Textbook project operates within free-tier resource limits.

## Backend Service (FastAPI)

### Memory and CPU Usage
- The application is designed to be lightweight using efficient libraries
- Sentence transformers model `all-MiniLM-L6-v2` is used (384-dimensional embeddings) instead of heavier models
- Embeddings are generated on-demand rather than pre-computed for large datasets

### Database (Neon Postgres)
- Uses connection pooling to minimize active connections
- Queries are optimized to retrieve only necessary data
- Data is paginated where appropriate

### Vector Database (Qdrant)
- Uses efficient indexing strategies
- Limits the number of results returned per query (default: 5)
- Embeddings are 384-dimensional (lightweight model) to reduce storage and computation

## Frontend (Docusaurus)

### Build Optimizations
- Disabled blog functionality to reduce build size
- Uses minimal theme with custom CSS overrides only where necessary
- Optimized image loading and asset compression

### Resource Usage
- Client-side only for the RAG chatbot UI
- API calls are limited and efficient
- Text selection and context extraction are performed client-side

## Deployment

### GitHub Pages (Frontend)
- Static site generation keeps hosting costs at $0
- Optimized build process for fast loading
- CDN distribution through GitHub's infrastructure

### Free-Tier Cloud Options (Backend)
The application is designed to work with various free-tier cloud providers:

- **Render**: Provides 100 hours/month free tier
- **Railway**: Offers $5/month in free credits
- **Fly.io**: Provides 225 CPU hours/month free tier
- **Heroku**: Free tier available (though limited)

## Cost Optimization Strategies

### Embedding Model
- Using `all-MiniLM-L6-v2` which is a lightweight model (27MB) that can run efficiently on CPU
- Model can be cached in memory to avoid repeated loading

### API Rate Limiting
- The system is designed to handle moderate traffic efficiently
- Caching can be added for frequently requested content

### Data Storage
- Only textbook content is stored, which is finite and static
- Chat history can be optionally stored but is not required for core functionality

## Performance Considerations

### Loading Speed
- Frontend is optimized for fast loading (<2s)
- Backend response times are optimized for <3s response
- Docusaurus build times are optimized to be under 5 minutes

### Resource Limits
- The system is designed to work within typical free-tier limits:
  - CPU: < 1 vCPU
  - RAM: < 512MB-1GB (depending on provider)
  - Storage: < 1GB for the application
  - Bandwidth: Optimized to minimize usage

## Free-Tier Compatible Alternatives

### Vector Database Alternatives
- If Qdrant cloud is not available, the system can work with local Qdrant or alternative vector stores
- In-memory solutions for small datasets

### Database Alternatives
- SQLite for very small deployments
- PostgreSQL on free-tier cloud providers

This design ensures the application can run on free-tier resources while providing full functionality.