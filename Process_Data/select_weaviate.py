import weaviate

PROPERITIES = ["uuid", "content"]
classNm = "Finaled"

# 統計筆數
if __name__ == "__main__1":
    client = weaviate.Client(url="YOUR_WEAVIATE_URL",
                             additional_headers={"X-Azure-Api-Key": "YOUR_AZURE_API_KEY"})
    print(client.query.aggregate(classNm).with_meta_count().do())

# 顯示所有資料
if __name__ == "__main__":
    client = weaviate.Client(url="YOUR_WEAVIATE_URL",
                             additional_headers={"X-Azure-Api-Key": "YOUR_AZURE_API_KEY"})
    client.schema.exists(classNm)

    result = client.query.get(class_name=classNm, properties=PROPERITIES).with_limit(10000).do()

    print(str(result))
