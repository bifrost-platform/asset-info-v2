from argparse import ArgumentParser

from libraries.preprocess.runner import run_preprocess
from libraries.puller.runner import run_token_puller

OPERATION_DICT = {"preprocess": run_preprocess, "pull_token": run_token_puller}
"""The dictionary of operations application supports."""


if __name__ == "__main__":
    parser = ArgumentParser(description="Run application for asset-info-v2.")
    parser.add_argument(
        "operation",
        type=str,
        choices=OPERATION_DICT.keys(),
        help="The operation to run.",
    )
    args = parser.parse_args()
    OPERATION_DICT[args.operation]()
