# TODO: Read the directory.
# TODO: Find all the files that are .xml
# TODO: Make sure that all the files are correct proposals or blocks.
# TODO: Use xml convertor from Christian.
# TODO: Might need to simplify results json
# TODO: Insert the results json to Mongo

import os
import re
from glob import glob
from pymongo import MongoClient
from typing import List, Dict, Any, OrderedDict, Optional
import collections

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


def remove_namespaces(data: Dict[str, Any]) -> OrderedDict[str, Any]:
    updated = collections.OrderedDict()
    for key, value in data.items():
        new_key = updated_key(key)
        new_value = updated_value(value)

        if re.match(r"^\@", str(new_key)):
            new_key = new_key[1:]
        if not (new_value == "Pass this value."):
            updated[new_key] = new_value
    return updated


def updated_key(key: str) -> str:
    if ":" in key:
        ns, tag = key.split(":", 1)
        return tag
    else:
        return key


def updated_value(value: Any) -> Any:
    if isinstance(value, dict):
        return remove_namespaces(value)
    elif isinstance(value, list) or isinstance(value, tuple):
        return [updated_value(item) for item in value]
    else:
        if not value:
            return value
        if re.match(r"^http", str(value)):
            return "Pass this value."
        return value


def is_number(value):
    try:
        float(value)
        return True
    except Exception:
        return False
