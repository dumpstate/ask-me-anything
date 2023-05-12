# ask-me-anything

Post context and ask any question.

## Running Locally

It requires postgres with pgvector + a valid OpenAI API key.

One can use provided `docker-compose.yml`.

### Installation

```sh
pip install -e .
```

### Configuration

Provide the following environment variables:

```sh
export OPENAI_API_KEY="..."
export AMA__DB="..." # by default postgresql://ama:ama_pass@127.0.0.1:5432/ama_db
```


### Run

```sh
make run
```


## Usage

1. Build up the context:

e.g.,

```sh
curl -XPUT -H "Content-Type: application/json" "http://localhost:8000/api/v1/context" -d '{
    "url": "https://en.wikipedia.org/wiki/Printing_press"
}'
```

2. Ask a question:

e.g.,

```sh
curl -XPOST -H "Content-Type: application/json" "http://localhost:8000/api/v1/question" -d '{
    "question": "Who invented printing press?"
}'
```

the expected answer:
```json
{
    "answer": "Johann Gutenberg is credited for inventing the printing press."
}
```
