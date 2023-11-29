import weaviate
from langchain.embeddings import OpenAIEmbeddings

class WeaviateSemanticSearch:
    def __init__(self, classNm):
        self.url = "YOUR_WEAVIATE_URL"
        self.embeddings = OpenAIEmbeddings(chunk_size=1, model="text-embedding-ada-002", openai_api_key="YOUR_OPENAI_API_KEY")
        self.client = weaviate.Client(
            url="YOUR_WEAVIATE_URL",
            additional_headers={"X-Azure-Api-Key": "YOUR_AZURE_API_KEY"}
        )
        self.classNm = classNm

    def semantic_search(self, query_text, num):
        query_vector = self.embeddings.embed_query(query_text)

        vector_str = ",".join(map(str, query_vector))

        gql_query = f"""
        {{
            Get {{
                {self.classNm}(nearVector: {{vector: [{vector_str}] }}, limit: {num}) {{
                    content
                    _additional {{
                        distance
                    }}
                }}
            }}
        }}
        """

        search_results = self.client.query.raw(gql_query)
        
        if 'errors' in search_results:
            raise Exception(search_results['errors'][0]['message'])
        
        results = search_results['data']['Get'][self.classNm]
        
        return results

def search_do(input_):
    searcher = WeaviateSemanticSearch("Finaled")
    results = searcher.semantic_search(input_, 1)

    # result_li = []
    for _, result in enumerate(results, 1):
        # result_li.append(result)
        response = result['content']

    return response

if __name__ == "__main__":
    print(search_do("中國信託"))
