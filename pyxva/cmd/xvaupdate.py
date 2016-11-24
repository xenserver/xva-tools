#!/usr/bin/env python

import argparse
import tarfile

from xva import open_xva

def update(args):
    mxva = open_xva(args.xva_file)

    if args.product_version:
        mxva.set_version("product_version", args.product_version)

    if args.xapi_minor:
        mxva.set_version("xapi_minor", args.xapi_minor)

    with open(args.output, 'w') as fh:
        mxva.save(fh)

def main():
    parser = argparse.ArgumentParser(description="Tool for updating XVA metadata")
    parser.add_argument("-f", "--file",
                        dest="xva_file",
                        required=True,
                        help="XVA file to update")
    parser.add_argument("-o", "--output",
                        dest="output",
                        required=True,
                        help="Path to the output XVA")
    parser.add_argument("--product-version",
                        dest="product_version",
                        help="Update the minimum XenServer version.")
    parser.add_argument("--xapi-minor",
                        dest="xapi_minor",
                        help="Update the XAPI minor version.")

    args = parser.parse_args()
    update(args)
