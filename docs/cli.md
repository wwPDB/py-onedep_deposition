# Wrapper and CLI

We provide a wrapper for the API that can be used both as a library and a command line application. The wrapper can be accessed on https://github.com/wwPDB/py-onedep_deposition.

## Installation
The wrapper is available on PyPI and can be installed via pip with

```pip install onedep-deposition```

## Configuration

To use the CLI, you need to set your API key either as an environment variable (`ONEDEP_API_KEY`) or store it in your home folder in a file named `onedepapi.jwt`. After this you'll be able to use the command line.

## Hostname choice
The CLI provides an option to specify the host to send requests to. If not specified, it will connect to production OneDep servers.

When using the test server, you should provide the `-h https://onedep-depui-test.wwpdb.org/deposition` option for every command.


## Depositions

### CLI

When creating a deposition, it's required to provide the experiment
type (`-t option`), email (`-e`), list of users (`-u`) and country
(`-c`). EM depositions also require a subtype (`-s`). Optionally, you
can provide an EMDB related entry id for EM/EC depositions (`-E`) or a
BMRB related entry id for NMR depositions (`-B`).

```
onedep-deposition -h https://onedep-depui-test.wwpdb.org/deposition deposition create -t xray -e wbueno@ebi.ac.uk -u 0000-0002-5109-8728 -c "United Kingdom"

onedep-deposition -h https://onedep-depui-test.wwpdb.org/deposition deposition create -t em -s helical -e wbueno@ebi.ac.uk -u 0000-0002-5109-8728 -c "United Kingdom"
```

To get details for a deposition, run the deposition get command and provide the deposition
identifier.

```
onedep-deposition -h https://onedep-depui-test.wwpdb.org/deposition deposition get <dep_id>
```

To submit files for processing, you can use:

```
onedep-deposition -h https://onedep-depui-test.wwpdb.org/deposition deposition process <dep_id>
```

It's also possible to copy metadata from a related deposition
using the `--copy-from-id <dep_id>` option. You need to provide which
metadata will be copied. Check the documentation for supported fields.

```
onedep-deposition -h https://onedep-depui-test.wwpdb.org/deposition deposition process --copy-from-id D_X --copy-all <dep_id>
```

The
processing progress can be check with the status command:

```
onedep-deposition -h https://onedep-depui-test.wwpdb.org/deposition deposition status <dep_id>
```

### API

It's possible to call the underlying API from a third-party code to create depositions. Example:

```
from onedep_deposition.deposit_api import DepositApi

api = DepositApi(hostname="<server_hostname>", api_key="<key>")
deposition = api.create_xray_deposition(email, users, country, password)
```

Documentation for the API is still under work, but the client wrapper https://github.com/wwPDB/py-onedep_deposition/blob/master/onedep_deposition/cli/cli.py  is a good example on how to call its methods from any other code.

## Files

The `files` command group is used to upload and remove files from
depositions, as well as get a list of files already uploaded and also
to provide metadata for EM entries.

The command to upload files is:

```
onedep-deposition files upload <dep_id> -f <file_path> -t <file_type>
```

Check the documentation for the allowed file types.

To remove files or update their metadata, it's required to provide a file identifier, which can be accessed through the `get` command.

```
onedep-deposition files get <dep_id>
```

### API

To use the files API for uploading files, you'll need to provide the proper enumeration type. An example can be seen below.

```
from onedep_deposition.enum import FileType
file = api.upload_file(dep_id, file_path, file_type, overwrite)
```

## Users

### CLI
Access to depositions can be managed using the `users` command group. 

```
onedep-deposition users get <dep_id> # list users
onedep-deposition users add <dep_id> <user_orcid> # add new user
onedep-deposition users remove <dep_id> <user_orcid> # remove user
```

### API
The API calls to manage users are:

```
users = api.get_users(dep_id)
users = api.add_user(dep_id, orcid=orcid)
used_deleted = api.remove_user(dep_id, orcid)
```

