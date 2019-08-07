import logging
import time
from datetime import datetime
import sys
import os
from bz2 import BZ2File
import json
import multiprocessing
from wikidata import parse

def parse_dump(dump_path):
    start_time = datetime.now()

    corpus_dir = './corpus'
    if not os.path.exists(corpus_dir):
        os.makedirs(corpus_dir)
        logger.debug('make dir: {}'.format(corpus_dir))

    target_pair_file = "./filters/target_pairs.json"
    manager = multiprocessing.Manager()

    with open(target_pair_file, 'r') as f:
        target_pairs = json.load(f)
        processes = []
        queues = []
        # Make queues and processes for each pair.
        for target_pair in target_pairs:
            queues.append(manager.Queue())
            processes.append(multiprocessing.Process(target=parse, args=(target_pair, queues[-1])))
            processes[-1].name = '-'.join(target_pair)
            processes[-1].start()

    # Read dump file line by line and parse.
    with BZ2File(dump_path, 'r') as bzfin:
        for i, line in enumerate(bzfin):
            line = line.decode('utf-8')
            if i % 10000 == 0: 
                logger.debug("Processing {}th element. Time elapsed (hh:mm:ss.ms) {}"
                        .format(i, datetime.now() - start_time))

            line = line.strip().rstrip(',')
            for q in queues:
                # while q.qsize() > 10000:
                    # logger.warning('q size grows more than {}. sleep reading for 0.5s.'.format(q.qsize()))
                    # time.sleep(0.5)
                q.put(line)

    # close queues and join processes
    for q in queues:
        q.close()
        q.join_thread()

    for p in processes:
        p.join()


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    stream_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler('./run_parse_wiki.log')

    stream_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.DEBUG)

    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    if (len(sys.argv) != 2):
        print("usage: python3 run_parse_wiki.py WIKIDATA_DUMP_DIR (latest-all.json.bz2)\n")
    else:
        dump_path = sys.argv[1]
        parse_dump(dump_path)
