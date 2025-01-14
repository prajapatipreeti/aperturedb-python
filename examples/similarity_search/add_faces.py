import argparse
from aperturedb import Utils, ParallelLoader
from facenet import generate_embedding
import dbinfo
from CelebADataKaggle import CelebADataKaggle

search_set_name = "similar_celebreties"


def main(params):
    utils = Utils.Utils(dbinfo.create_connector())
    utils.remove_descriptorset(search_set_name)
    utils.add_descriptorset(search_set_name, 512,
                            metric="L2", engine="FaissFlat")

    dataset = CelebADataKaggle(
        records_count=params.images_count,
        embedding_generator=generate_embedding,
        search_set_name=search_set_name
    )
    print(len(dataset))

    loader = ParallelLoader.ParallelLoader(dbinfo.create_connector())
    loader.ingest(dataset, stats=True)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-images_count', type=int, required=True,
                        help="The number of images to ingest into aperturedb")
    return parser.parse_args()


if __name__ == "__main__":
    main(get_args())
