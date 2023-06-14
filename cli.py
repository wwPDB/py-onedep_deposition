import click
import re
import os
from typing import List
from onedep_deposition.deposit_api import DepositApi
from onedep_deposition.enum import Country

def get_api_key():
    """Get API key from the file system or environment variable"""
    if os.path.isfile(os.path.expanduser("~/onedepapi.jwt")):
        with open(os.path.expanduser("~/onedepapi.jwt"), "r") as f:
            api_key = f.read()
    else:
        api_key = os.environ.get("ONEDEP_API_KEY")
    if not api_key:
        raise click.BadParameter("API key not found. Please set the ONEDEP_API_KEY environment variable or create a "
                                 "file named onedepapi.jwt in your home directory with the API key.")
    return api_key

def get_country_enum(country_string: str):
    """Get Country enum from string"""
    for country in Country:
        if country.value == country_string:
            return country
    raise click.BadParameter("Invalid country, options are: " + ", ".join([country.value for country in Country]))

@click.group(name="deposition", help="Manage depositions")
def deposition_group():
    """`deposition` command group"""

@deposition_group.command(name="create", help="Generate the project structure and the command line interface from the CLI specification file pointed by FILENAME.")
@click.option("-t", "--type", "dep_type", help="Experiment type [em, xray, fiber, neutron, ec, nmr, ssnmr]")
@click.option("-e", "--email", "email", help="Main depositor email")
@click.option("-u", "--users", "users", multiple=True, help="List of users to add to the deposition")
@click.option("-c", "--country", "country_string", help="Country of the main depositor")
@click.option("-s", "--subtype", "subtype", help="Experiment subtype, only valid if type is EM")
@click.option("-E", "--related_emdb", "related_emdb", help="Related EMDB code. Only valid for EM and EC")
@click.option("-B", "--related_bmrb", "related_bmrb", help="Related BMRB code. Only valid for NMR")
@click.option("-p", "--password", "password", help="Deposition password")
@click.option("-h", "--hostname", "hostname", help="Deposition hostname (Default: defined from the country)")
@click.option("-v", "--ssl_verify", "ssl_verify", help="SSL verification (Default: True)")
def create(dep_type: str, email: str, users: List[str], country_string: str, subtype: str, related_emdb: str,
           related_bmrb: str, password: str, hostname: str, ssl_verify: bool):
    """`create` command handler"""
    if subtype:
        if subtype not in ["helical", "single", "subtomogram", "tomography"]:
            raise click.BadParameter("Invalid experiment subtype, options are: helical, single, subtomogram, tomography")
    if not email:
        raise click.BadParameter("Email is required")
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        raise click.BadParameter("Invalid email")
    if len(users) == 0:
        raise click.BadParameter("At least one user is required")
    if related_bmrb:
        if not re.match(r'^\d+$', related_bmrb):
            raise click.BadParameter("Invalid BMRB code")
    if related_emdb:
        if not re.match(r'^EMD-\d{4,5}$', related_emdb):
            raise click.BadParameter("Invalid EMDB code")
    country = get_country_enum(country_string)

    args= {
        "api_key": get_api_key()
    }
    if hostname:
        args["hostname"] = hostname
    if ssl_verify:
        args["ssl_verify"] = ssl_verify
    api = DepositApi(**args)

    if dep_type == "em":
        deposition = api.create_em_deposition(email, users, country, subtype, related_emdb, password)
    elif dep_type == "xray":
        deposition = api.create_xray_deposition(email, users, country, password)
    elif dep_type == "fiber":
        deposition = api.create_fiber_deposition(email, users, country, password)
    elif dep_type == "neutron":
        deposition = api.create_neutron_deposition(email, users, country, password)
    elif dep_type == "ec":
        deposition = api.create_ec_deposition(email, users, country, related_emdb, password)
    elif dep_type == "nmr":
        deposition = api.create_nmr_deposition(email, users, country, related_bmrb, password)
    elif dep_type == "ssnmr":
        deposition = api.create_ssnmr_deposition(email, users, country, related_bmrb, password)
    else:
        raise click.BadParameter("Invalid experiment type, options are: em, xray, fiber, neutron, ec, nmr, ssnmr")
    print(deposition)







@deposition_group.command(name="get", help="Get deposition info")
@click.argument("dep_id")
def get(dep_id):
    """`get` command handler"""


@deposition_group.command(name="status", help="Status of processing")
def status():
    """`status` command handler"""


@deposition_group.command(name="process", help="Process deposition. TODO.")
def process():
    """`process` command handler"""


@click.group(name="users", help="Manage deposition access")
def users_group():
    """`users` command group"""


@users_group.command(name="get", help="Get users in deposition")
@click.argument("dep_id")
def get(dep_id):
    """`get` command handler"""


@users_group.command(name="add", help="Add users to the deposition")
@click.argument("dep_id")
def add(dep_id):
    """`add` command handler"""


@users_group.command(name="remove", help="Remove an user from a deposition")
@click.argument("dep_id")
def remove(dep_id):
    """`remove` command handler"""


@users_group.command(name="summary", help="Generate a summary of the command line interface, to be used somewhere else, from the CLI specification file pointed by FILENAME.")
@click.argument("dep_id")
def summary(dep_id):
    """`summary` command handler"""


@click.group(name="files", help="Manage deposition files")
def files_group():
    """`files` command group"""


@files_group.command(name="upload", help="Upload a file to the deposition")
@click.argument("file_path")
@click.argument("file_type")
@click.argument("dep_id")
@click.option("-o", "--overwrite", "overwrite", help="Overwrite destination file if file with same name is present")
def upload(file_path, file_type, dep_id, overwrite):
    """`upload` command handler"""


@files_group.command(name="list", help="List files in deposition")
@click.argument("dep_id")
def list(dep_id):
    """`list` command handler"""


@files_group.command(name="remove", help="Remove a file from the deposition")
@click.argument("file_id")
@click.argument("dep_id")
def remove(file_id, dep_id):
    """`remove` command handler"""


@click.group()
def cli():
    """CLI entry point"""


@cli.command(name="version", help="Show the version and exit.")
def version():
    """`version` command handler"""


cli.add_command(deposition_group)
cli.add_command(users_group)
cli.add_command(files_group)


if __name__ == "__main__":
    cli()
