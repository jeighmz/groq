from mem0 import MemoryClient
import os

api_key_mem = os.environ.get('MEM0_API_KEY')

memory_client = MemoryClient(api_key=api_key_mem)

query = "What color should my first car be?"
x = memory_client.search(query, user_id="default_user")
print(x)
