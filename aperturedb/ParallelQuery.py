from aperturedb import Parallelizer
import numpy as np
import json
import logging
import math

logger = logging.getLogger(__name__)


class ParallelQuery(Parallelizer.Parallelizer):

    """**Parallel and Batch Querier for ApertureDB**"""

    def __init__(self, db, dry_run=False):

        super().__init__()

        self.db = db.create_new_connection()

        self.dry_run = dry_run

        self.type = "query"

        self.responses = []

    def generate_batch(self, data):
        """
            Here we flatten the individual queries to run them as
            a single query in a batch
        """
        q     = [cmd for query in data for cmd in query[0]]
        blobs = [blob for query in data for blob in query[1]]

        return q, blobs

    def call_response_handler(self, r, b):

        try:
            self.generator.response_handler(r, b)
        except BaseException as e:
            print("handler error:", r)
            print(e)

    def do_batch(self, db, data):

        q, blobs = self.generate_batch(data)

        query_time = 0

        if not self.dry_run:
            r, b = db.query(q, blobs)
            if db.last_query_ok():
                if hasattr(self, "response_handler") and callable(self.response_handler):
                    # We could potentially always call this handler function
                    # and let the user deal with the error cases.

                    cmds_per_query = math.ceil(len(r) / self.batchsize)
                    for i in range(self.batchsize):
                        start = i * cmds_per_query
                        end = start + cmds_per_query
                        self.call_response_handler(
                            r[start:end], b[start:end])
            else:
                # Transaction failed entirely.
                logger.error(f"Failed query = {q} with response = {r}")
                self.error_counter += 1

            if isinstance(r, list) and not all([v['status'] == 0 for i in r for k, v in i.items()]):
                logger.warning(
                    f"Partial errors:\r\n{json.dumps(q)}\r\n{json.dumps(r)}")
            query_time = db.get_last_query_time()
        else:
            query_time = 1

        # append is thread-safe
        self.times_arr.append(query_time)

    def worker(self, thid, generator, start, end):

        # A new connection will be created for each thread
        db = self.db.create_new_connection()

        total_batches = (end - start) // self.batchsize

        if (end - start) % self.batchsize > 0:
            total_batches += 1

        for i in range(total_batches):

            batch_start = start + i * self.batchsize
            batch_end   = min(batch_start + self.batchsize, end)

            try:
                self.do_batch(db, generator[batch_start:batch_end])
            except Exception as e:
                logger.exception(e)
                self.error_counter += 1

            if thid == 0 and self.stats:
                self.pb.update((i + 1) / total_batches)

    def query(self, generator, batchsize=1, numthreads=4, stats=False):

        self.run(generator, batchsize, numthreads, stats)

    def print_stats(self):

        times = np.array(self.times_arr)
        total_queries_exec = len(times)

        print("============ ApertureDB Parallel Query Stats ============")
        print("Total time (s):", self.total_actions_time)
        print("Total queries executed:", total_queries_exec)

        if total_queries_exec == 0:
            print("All queries failed!")

        else:
            print("Avg Query time (s):", np.mean(times))
            print("Query time std:", np.std(times))
            print("Avg Query Throughput (q/s)):",
                  1 / np.mean(times) * self.numthreads)

            msg = "(" + self.type + "/s):"
            print("Overall throughput", msg,
                  self.total_actions / self.total_actions_time)

            if self.error_counter > 0:
                print("Total errors encountered:", self.error_counter)
                print("Errors (%):", 100 *
                      self.error_counter / total_queries_exec)

        print("=========================================================")
