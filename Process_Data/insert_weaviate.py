import uuid
import weaviate
from langchain.embeddings import OpenAIEmbeddings
import time

class WeaviateManager:
    def __init__(self, classNm):
        self.url = "YOUR_WEAVIATE_URL"
        self.embeddings = OpenAIEmbeddings(chunk_size=1, model="text-embedding-ada-002", openai_api_key="YOUR_OPENAI_API_KEY")
        self.client = weaviate.Client(
            url="YOUR_WEAVIATE_URL",
            additional_headers={"X-Azure-Api-Key": "YOUR_AZURE_API_KEY"}
        )
        self.schema = self.client.schema
        self.classNm = classNm
        self.check_class_exist()
        pass

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
                    "name": "content",
                    "dataType": ["text"]
                }
            ],
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "resourceName": "YOUR_RESOURCE_NAME",
                    "deploymentId": "text-embedding-ada-002"
                }
            }
        }
        print(f'creating {self.classNm}...')
        self.client.schema.create_class(schema)
        print(f'{self.classNm} is ready')
        return True
        
    def insert_data(self, content_text):
        data_object = {
            "uuid": str(uuid.uuid4()),
            "content": content_text
        }
        self.client.data_object.create(data_object, self.classNm)

if __name__ == "__main__":
    manager = WeaviateManager("Finaled")

    with open('Data/final_output.txt', 'r', encoding='utf-8') as file:
        contented = file.read()
        result = contented.split("\n\n")

    count = 0
    for cont in result:
        time.sleep(0.5)
        manager.insert_data(cont[:4000])
        count += 1
        print(count)
