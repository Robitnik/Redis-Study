import os
import time
import random
import redis


def get_client() -> redis.Redis:
    host = os.getenv("REDIS_HOST", "redis")
    port = int(os.getenv("REDIS_PORT", "6379"))
    return redis.Redis(host=host, port=port, db=0)


def main() -> None:
    client = get_client()
    for attempt in range(1, 6):
        try:
            client.ping()
            break
        except redis.exceptions.ConnectionError:
            sleep_for = attempt
            print(f"Redis not ready, retrying in {sleep_for}s (attempt {attempt}/5)...")
            time.sleep(sleep_for)
    else:
        raise SystemExit("Could not connect to Redis after multiple attempts.")
    random_list = [random.randint(1, 10000) for _ in range(10)]
    random_dict = {str(i): random.randint(1, 10000) for i in range(10)}
    random_dict_with_lists = {str(i): [random.randint(1, 10000) for _ in range(5)] for i in range(10)}
    print(f"Generated random list: {type(random_list)}")
    print(f"Generated random dict: {type(random_dict)}")
    print(f"Generated random dict with lists: {type(random_dict_with_lists)}")
    print("Setting and getting a value from Redis...")
    client.set("random_list", str(random_list))
    client.set("random_dict", str(random_dict))
    client.set("random_dict_with_lists", str(random_dict_with_lists))
    print("Good")
    print("clearing...")
    random_list = None
    random_dict = None
    random_dict_with_lists = None
    print(f"{type(random_list)} {type(random_dict)} {type(random_dict_with_lists)}")
    print("Getting values from Redis...")
    random_list = client.get("random_list")
    random_dict = client.get("random_dict")
    random_dict_with_lists = client.get("random_dict_with_lists")
    print(f"Retrieved random list: {type(random_list)}")
    print(f"Retrieved random dict: {type(random_dict)}")
    print(f"Retrieved random dict with lists: {type(random_dict_with_lists)}")



if __name__ == "__main__":
    main()
