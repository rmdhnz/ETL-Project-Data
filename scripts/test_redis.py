from etl.cache.redis import redis_client


def main() -> None:
    try:
        redis_client.set("etl:test", "Hello from the etl")

        value = redis_client.get("etl:test")

        print(f"Redis value : {value}")
    except Exception as e:
        print(f"Error : {e}")


if __name__ == "__main__":
    main()
