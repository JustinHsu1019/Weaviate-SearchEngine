import os, uuid, weaviate
from langchain_openai import AzureOpenAIEmbeddings

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.config_log as config_log
config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

os.environ["OPENAI_API_TYPE"] = config.get('Azure_Open_AI_0912', 'api_type')
os.environ["AZURE_OPENAI_ENDPOINT"] = config.get('Azure_Open_AI_0912', 'azure_endpoint')
os.environ["OPENAI_API_VERSION"] = config.get('Azure_Open_AI_0912', 'api_version')
os.environ["OPENAI_API_KEY"] = config.get('Azure_Open_AI_0912', 'api_key')

class WeaviateBase:
    def __init__(self, classNm):
        self.client = self.setup_weaviate_client()
        self.classNm = classNm
        self.embeddings = AzureOpenAIEmbeddings(
            chunk_size=1,
            model=config.get('Azure_Open_AI_0912', 'embedding_model_search')
        )

    @staticmethod
    def setup_weaviate_client():
        return weaviate.Client(
            url=config.get('Weaviate', 'weaviate_url'),
            additional_headers={"X-Azure-Api-Key": f"{config.get('Azure_Open_AI_0912', 'api_key')}"}
        )

class WeaviateManager(WeaviateBase):
    def __init__(self, classNm):
        super().__init__(classNm)
        self.check_class_exist()

    def check_class_exist(self):
        if self.client.schema.exists(self.classNm):
            print(f'{self.classNm} is ready')
            return True
        schema = {
            "class": self.classNm,
            "properties": [
                {
                    "name": "uuid",
                    "dataType": ["text"]
                },
                {
                    "name": "aaa",
                    "dataType": ["text"]
                },
                {
                    "name": "bbb",
                    "dataType": ["text"]
                }
            ],
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "resourceName": config.get("Azure_Open_AI_0912", 'resourcename'),
                    "deploymentId": config.get("Azure_Open_AI_0912", 'embedding_model_search')
                }
            }
        }
        print(f'creating {self.classNm}...')
        self.client.schema.create_class(schema)
        print(f'{self.classNm} is ready')
        return True
        
    def insert_data(self, aaa, bbb):
        data_object = {
            "uuid": str(uuid.uuid4()),
            "aaa": aaa,
            "bbb": bbb,
        }
        self.client.data_object.create(data_object, self.classNm)

class WeaviateSemanticSearch(WeaviateBase):
    def semantic_search(self, query_text, num):
        query_vector = self.embeddings.embed_query(query_text)

        vector_str = ",".join(map(str, query_vector))

        gql_query = f"""
        {{
            Get {{
                {self.classNm}(nearVector: {{vector: [{vector_str}] }}, limit: {num}) {{
                    aaa
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

def main():
    class_name = config.get('Weaviate', 'classnm')

    # Insert
    manager = WeaviateManager(class_name)
    manager.insert_data("標題一", "這是第一筆資料的內容。")
    manager.insert_data("標題二", "這是第二筆資料的內容。")
    manager.insert_data("標題三", "這是第三筆資料的內容。")

    # Get Top10
    searcher = WeaviateSemanticSearch(class_name)
    results = searcher.semantic_search("標題1", 10)

    for idx, result in enumerate(results, 1):
        print(f"Top{idx} Result: {result}")
        print(f"Vector Distance: {result['_additional']['distance']}")

if __name__ == "__main__":
    main()
