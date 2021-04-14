import time
import threading

def greeter(name: str, count: int):
    for _ in range(0,count):
        print(f'Hello {name}')
        time.sleep(1)


def main():
    threads =[
        threading.Thread(target=greeter, args=('test 1', 3), daemon=True),
        threading.Thread(target=greeter, args=('test 2', 3), daemon=True),
        threading.Thread(target=greeter, args=('test 3', 3), daemon=True),
    ]
    [thread.start() for thread in threads]
    print('Main')
    [thread.join() for thread in threads]
    print('Done!')

if __name__ == '__main__':
    main()