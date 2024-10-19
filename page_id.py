import httpx
from time import sleep
from os import environ
from data import fb_url, FB_TOKEN

# função para obter o id da pagina do facebook e armazenar na variável ambiente PAGE_ID


def get_id():

    if 'PAGE_ID' not in environ:
        retries: int = 0
        max_retries: int = 3
        while retries < max_retries:
            try:
                response = httpx.get(f'{fb_url}/me?access_token={FB_TOKEN}', timeout=5)
                if response.status_code != 200:
                    print(f"Failed to get page ID: {response.status_code} {response.content}")
                    retries += 1
                else:
                    PAGE_ID: str = response.json().get('id')
                    if PAGE_ID:
                        environ.setdefault("PAGE_ID", PAGE_ID)
                        print('Facebok PAGE_ID set successfully')
                        break
                    
            except httpx._exceptions as e:
                retries += 1
                print(f"Request error: {e}\n. Retrying...")
                sleep(3)
        
        if retries == max_retries:
            print("Failed to get page ID after maximum retries")