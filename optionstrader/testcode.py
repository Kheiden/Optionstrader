import logging
import threading
import time

def worker(arg, i):
    while not arg['stop']:
        logging.debug('Hi from myfunc {0}'.format(i))
        time.sleep(0.5)

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(relativeCreated)6d %(threadName)s %(message)s')
    #info = {'stop': False}
    for i in range(2):
        thread = threading.Thread(target=worker, args=(info, i,))
        thread.start()
    while True:
        try:
            logging.debug('Hello from main')
            time.sleep(0.75)
        except KeyboardInterrupt:
            info['stop'] = True
            break
    thread.join()

if __name__ == '__main__':
    main()
