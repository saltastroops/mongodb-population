# TODO: Read the directory.
# TODO: Find all the files that are .xml
# TODO: Make sure that all the files are correct proposals or blocks.
# TODO: Use xml convertor from Christian.
# TODO: Might need to simplify results json
# TODO: Insert the results json to Mongo

import os
import re
from glob import glob

from typing import List, Dict, Optional
import xmltodict

import click

from database import proposals_collections, blocks_collections
from generate_json import remove_namespaces


def get_proposal_and_blocks_xmls(xml_files: List[str])-> Dict[str, List[str]]:
    """
    Method that will verify the valid blocks and proposal for all proposal's xml_files
    Parameters
    ----------
    xml_files
        All the xml files in the proposal
    Returns
    -------
    Dict with a proposal xml file and blocks xml files

    """
    blocks = []
    proposal = ""
    for file in xml_files:
        basename = os.path.basename(file)
        if basename == "Proposal.xml":
            proposal = file
        if re.match(r"\bBlock-\b.*\b.xml\b", basename):
            blocks.append(file)
    return dict(proposal=proposal, blocks=blocks)


def read_director(proposal_dir: str) -> Optional[Dict[str, List[str]]]:
    """
    the method to read the directory and return all  the xml files in in
    Parameters
    ----------
    proposal_dir
        The directory where the xml files are

    Returns
    -------
    The list of all xml files in the directory

    """
    # Todo find all xml file
    proposal_path = proposal_dir + "/1/*.xml"
    proposal_xml = glob(proposal_path)

    blocks_path = proposal_dir + "/Included/Block-*.xml"
    blocks_xml = glob(blocks_path)
    # Ignore none phase2 proposals
    if not len(blocks_xml):
        return None
    return get_proposal_and_blocks_xmls(proposal_xml + blocks_xml)


def get_all_proposals(base_dir: str) -> List[str]:
    return [ f.path for f in os.scandir(base_dir) if f.is_dir() ]


@click.command()
@click.option(
    "--base_dir",
    "base_dir",
    type=click.Path(resolve_path=True),
    help="Path of the JSON file to create",
)
@click.option(
    "--min_blocks",
    "min_blocks",
    type=click.INT,
    help="The minimum number of blocks for a proposal version",
)
@click.option(
    "--proposal_loop",
    "proposal_loop",
    type=click.INT,
    help="The minimum number of blocks for a proposal version",
)
# @click.option(
#     "--max_block",
#     "max_block",
#     type=click.INT,
#     help="The maximum number of blocks for a proposal version",
# )
def main(base_dir, min_blocks, proposal_loop):
    proposals_dirs = get_all_proposals(base_dir)
    loop_count = 0
    print(loop_count <= proposal_loop, loop_count,  proposal_loop)
    while loop_count <= proposal_loop:
        for proposal in proposals_dirs:
            proposal_xml_files = read_director(proposal)
            if proposal_xml_files:
                with open(proposal_xml_files["proposal"]) as proposal_xml:
                    proposal_json = xmltodict.parse(proposal_xml.read())
                    without_namespaces = remove_namespaces(proposal_json)["Proposal"]
                    without_namespaces["code"] = without_namespaces["code"] + "-" + str(loop_count)

                    proposal_id = proposals_collections.insert_one(without_namespaces).inserted_id
                num_blocks = 0
                block_loop_count = 0
                while num_blocks < min_blocks:
                    for block in proposal_xml_files["blocks"]:
                        with open(block) as block_xml:
                            block_json = xmltodict.parse(block_xml.read())
                            without_namespaces = remove_namespaces(block_json)
                            without_namespaces["Block"]["proposal_id"] = proposal_id
                            without_namespaces["Block"]["id"] = without_namespaces["Block"]["id"] + f"-{block_loop_count}"
                            without_namespaces["Block"]["Name"] = without_namespaces["Block"]["Name"] + f"-{block_loop_count}"
                            without_namespaces["Block"]["BlockCode"] = without_namespaces["Block"]["BlockCode"] + f"-{block_loop_count}"
                            blocks_collections.insert_one(without_namespaces["Block"])
                    num_blocks = blocks_collections.count_documents({"proposal_id": proposal_id})
                    block_loop_count += 1
                print(num_blocks)
        loop_count += 1

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# scp -r piptweb@www.salt.ac.za:'/var/www/webmanager/replicate/proposals/2020-1-SCI-001 /var/www/webmanager/replicate/proposals/2020-1-SCI-002 /var/www/webmanager/replicate/proposals/2020-1-SCI-003 /var/www/webmanager/replicate/proposals/2020-1-SCI-004 /var/www/webmanager/replicate/proposals/2020-1-SCI-005 /var/www/webmanager/replicate/proposals/2020-1-SCI-006 /var/www/webmanager/replicate/proposals/2020-1-SCI-007 /var/www/webmanager/replicate/proposals/2020-1-SCI-008 /var/www/webmanager/replicate/proposals/2020-1-SCI-009 /var/www/webmanager/replicate/proposals/2020-1-SCI-010 /var/www/webmanager/replicate/proposals/2020-1-SCI-011 /var/www/webmanager/replicate/proposals/2020-1-SCI-012 /var/www/webmanager/replicate/proposals/2020-1-SCI-013 /var/www/webmanager/replicate/proposals/2020-1-SCI-014 /var/www/webmanager/replicate/proposals/2020-1-SCI-015 /var/www/webmanager/replicate/proposals/2020-1-SCI-016' ./proposals/
