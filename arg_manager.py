import argparse

def parser():
    parser = argparse.ArgumentParser(
        prog='PROGRAM',
        description='Download images from Google.',
        usage='%(prog)s search-query num_of_images'
    )

    parser.add_argument(
        'search_query',
        help='query for google image search'
    )

    parser.add_argument(
        'num_of_images',
        type=int,
        help='amount of images needed'
    )

    # store arguments in object
    args = parser.parse_args()
    QUERY = args.search_query
    NUM_IMAGES = args.num_of_images

    return QUERY, NUM_IMAGES
