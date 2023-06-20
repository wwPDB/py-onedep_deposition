import click
import re
import os
import json
from typing import List, Union, Dict
from onedep_deposition.deposit_api import DepositApi
from onedep_deposition.enum import Country, FileType

VERSION = "1.0.0"


def get_api_key():
    """Get API key from the file system or environment variable"""
    if os.path.isfile(os.path.expanduser("~/onedepapi.jwt")):
        with open(os.path.expanduser("~/onedepapi.jwt"), "r") as f:
            api_key = f.read().strip()
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


def get_file_type_enum(file_type_string: str):
    """Get FileType enum from string"""
    for file_type in FileType:
        if file_type.value == file_type_string:
            return file_type
    raise click.BadParameter("Invalid file type, options are: " + ", ".join([file_type.value for file_type in FileType]))


def create_api(func):
    """Decorator to create the API object"""
    def decorator(ctx, *args, **kwargs):
        hostname = ctx.obj["hostname"]
        no_ssl_verify = ctx.obj["no_ssl_verify"]
        no_redirect = ctx.obj["no_redirect"]

        api_args = {
            "api_key": get_api_key()
        }
        if hostname:
            api_args["hostname"] = hostname
        if no_ssl_verify:
            api_args["ssl_verify"] = False
        else:
            api_args["ssl_verify"] = True
        if no_redirect:
            api_args["redirect"] = False
        else:
            api_args["redirect"] = True
        api = DepositApi(**api_args)

        return func(api, ctx, *args, **kwargs)

    return decorator


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
@click.pass_context
@create_api
def create(api: DepositApi, ctx: Dict, dep_type: str, email: str, users: List[str], country_string: str, subtype: str,
           related_emdb: str, related_bmrb: str, password: str):
    """`create` deposition command handler"""
    if subtype:
        if subtype not in ["helical", "single", "subtomogram", "tomography"]:
            raise click.BadParameter("Invalid experiment subtype, options are: helical, single, subtomogram, tomography")
    if not email:
        raise click.BadParameter("Email is required")
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        raise click.BadParameter("Invalid email")
    if len(users) == 0:
        raise click.BadParameter("At least one user is required")
    else:
        for orcid in users:
            if not re.match(r'^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$', orcid):
                raise click.BadParameter(f"Invalid ORCID: {orcid}")
    if related_bmrb:
        if not re.match(r'^\d+$', related_bmrb):
            raise click.BadParameter("Invalid BMRB code")
    if related_emdb:
        if not re.match(r'^EMD-\d{4,5}$', related_emdb):
            raise click.BadParameter("Invalid EMDB code")
    country = get_country_enum(country_string)

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
    click.echo(deposition)


@deposition_group.command(name="get", help="Get deposition info")
@click.argument("dep_id")
@click.pass_context
@create_api
def get_deposition(api: DepositApi, ctx: Dict, dep_id: str):
    """`get` deposition command handler"""
    deposition = api.get_deposition(dep_id)
    click.echo(deposition)


@deposition_group.command(name="status", help="Status of processing")
@click.argument("dep_id")
@click.pass_context
@create_api
def status(api: DepositApi, ctx: Dict, dep_id: str):
    """`status` command handler"""
    response = api.get_status(dep_id)
    click.echo(response)


@deposition_group.command(name="process", help="Process deposition.")
@click.argument("dep_id")
@click.option("-V", "--voxels-json", "voxels_json", help='JSON file including the list of voxel values in the following format ([{"file_id": X, "spacing": Y, "contour": Z}, ...])')
@click.option("-c", "--copy-from-id", "copy_dep_id", help='Deposition ID to copy metadata from')
@click.option("--copy-all", "copy_all", is_flag=True, help="Copy all metadata from a previous deposition")
@click.option("--copy-contact", "copy_contact", is_flag=True, help="Copy contact metadata from a previous deposition")
@click.option("--copy-authors", "copy_authors", is_flag=True, help="Copy authors metadata from a previous deposition")
@click.option("--copy-citation", "copy_citation", is_flag=True, help="Copy citation metadata from a previous deposition")
@click.option("--copy-grant", "copy_grant", is_flag=True, help="Copy grant metadata from a previous deposition")
@click.option("--copy-em-exp", "copy_em_exp", is_flag=True, help="Copy EM experiment metadata from a previous deposition")
@click.pass_context
@create_api
def process(api: DepositApi, ctx: Dict, dep_id: str, voxels_json: str, copy_dep_id: str, copy_all: bool = False,
            copy_contact: bool = False, copy_authors: bool = False, copy_citation: bool = False,
            copy_grant: bool = False, copy_em_exp: bool = False):
    """`process` command handler"""
    copy_elements = {"copy_contact": False, "copy_authors": False, "copy_citation": False, "copy_grant": False, "copy_em_exp_data": False}
    if copy_dep_id:
        copy_elements = {"copy_contact": copy_contact, "copy_authors": copy_authors, "copy_citation": copy_citation,
                         "copy_grant": copy_grant, "copy_em_exp_data": copy_em_exp}
        if copy_all:
            copy_elements = {"copy_contact": True, "copy_authors": True, "copy_citation": True, "copy_grant": True, "copy_em_exp_data": True}

    if voxels_json:
        if not os.path.isfile(voxels_json):
            raise click.BadParameter("Voxel file not found")
        with open(voxels_json) as f:
            voxel = json.load(f)
    else:
        voxel = None

    response = api.process(dep_id, voxel=voxel, copy_from_id=copy_dep_id, **copy_elements)
    click.echo(response)


@click.group(name="users", help="Manage deposition access")
def users_group():
    """`users` command group"""


@users_group.command(name="get", help="Get users in deposition")
@click.argument("dep_id")
@click.pass_context
@create_api
def get_users(api: DepositApi, ctx: Dict, dep_id: str):
    """`get` users command handler"""
    users = api.get_users(dep_id)
    for user in users:
        click.echo(user)
        click.echo("---------------------------------")


@users_group.command(name="add", help="Add users to the deposition")
@click.argument("dep_id")
@click.option("-O", "--orcid", "orcid", multiple=True, help="User orcid to be removed from the deposition")
@click.pass_context
@create_api
def add(api: DepositApi, ctx: Dict, dep_id: str, orcid: Union[List, str]):
    """`add` users command handler"""
    if len(orcid) == 1:
        orcid = orcid[0]
    else:
        orcid = list(orcid)
    users = api.add_user(dep_id, orcid=orcid)
    for user in users:
        click.echo(user)
        click.echo("---------------------------------")


@users_group.command(name="remove", help="Remove an user from a deposition")
@click.argument("dep_id")
@click.option("-O", "--orcid", "orcid", multiple=False, help="User orcid to be removed from the deposition")
@click.pass_context
@create_api
def remove_user(api: DepositApi, ctx: Dict, dep_id: str, orcid: str):
    """`remove` command handler"""
    used_deleted = api.remove_user(dep_id, orcid)
    if used_deleted:
        click.echo(f"User {orcid} was removed from the deposition {dep_id}.")


@click.group(name="files", help="Manage deposition files")
def files_group():
    """`files` command group"""


@files_group.command(name="upload", help="Upload a file to the deposition")
@click.argument("dep_id")
@click.option("-f", "--file_path", "file_path", help="File path to be uploaded")
@click.option("-t", "--file_type", "file_type", help="File type to be uploaded")
@click.option("--overwrite", "overwrite", is_flag=True, help="Overwrite destination file if file with same name is present")
@click.pass_context
@create_api
def upload(api: DepositApi, ctx: Dict, dep_id: str, file_path: str, file_type: str, overwrite: bool = False):
    """`upload` command handler"""
    if not file_path:
        raise click.BadParameter("File path is required")
    if not file_type:
        raise click.BadParameter("File type is required")
    if not os.path.exists(file_path):
        raise click.BadParameter("File does not exist")

    file_type = get_file_type_enum(file_type)
    file = api.upload_file(dep_id, file_path, file_type, overwrite)
    click.echo(f"Uploaded file: {file}")


@files_group.command(name="get", help="Get files in deposition")
@click.argument("dep_id")
@click.pass_context
@create_api
def get_files(api: DepositApi, ctx: Dict, dep_id: str):
    """`list` command handler"""
    files = api.get_files(dep_id)
    for file in files:
        click.echo(file)
        click.echo("---------------------------------")


@files_group.command(name="remove", help="Remove a file from the deposition")
@click.argument("dep_id")
@click.argument("file_id")
@click.pass_context
@create_api
def remove_file(api: DepositApi, ctx: Dict, dep_id: str, file_id: int):
    """`remove` command handler"""
    file_removed = api.remove_file(dep_id, file_id)
    if file_removed:
        click.echo(f"File {file_id} was removed from the deposition {dep_id}.")


@click.group()
@click.option("-h", "--hostname", "hostname", help="Deposition hostname (Default: defined from the country)")
@click.option("--no_ssl_verify", "no_ssl_verify", is_flag=True, help="Disable SSL verification")
@click.option("--no_redirect", "no_redirect", is_flag=True, help="Disable site redirection (Default: enabled)")
@click.pass_context
def cli(ctx: dict, hostname: str, no_ssl_verify: bool, no_redirect: bool):
    """CLI entry point"""
    ctx.ensure_object(dict)
    ctx.obj["hostname"] = hostname
    ctx.obj["no_ssl_verify"] = no_ssl_verify
    ctx.obj["no_redirect"] = no_redirect


@cli.command(name="version", help="Show the version and exit.")
@click.version_option(f"{VERSION}")
def version():
    """`version` command handler"""
    click.echo(f"OneDep Deposition API version {VERSION}")


cli.add_command(deposition_group)
cli.add_command(users_group)
cli.add_command(files_group)


if __name__ == "__main__":
    cli(obj={})
