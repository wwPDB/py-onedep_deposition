# OneDep Deposition API Wrapper

This wrapper comes with a command line interface that can be executed by running `python cli.py <command>`.

## API Key

Go to the DepUI in the test server, login to ORCID and then on the left, below the map, click on `Generate Key`. Either copy the key to a file in `~/onedepapi.jwt` in your local laptop, or set it as an environment variable with `export ONEDEP_API_KEY=<key>`.

## Options

**Important!**

Be mindful of the options we use in the commands here. If you are running in a test server, you will have to explicitly set the hostname and SSL verification flag for every command. The options are `--hostname <host>` and `--no_ssl_verify`.

## Deposition creation

The command deposition create to start a new deposition:

`python cli.py deposition create -t <exp type> -e <email> -u <users comma separated> -c <country>`

For example, to create an x-ray deposition:

`python cli.py -h http://local.wwpdb.org:12000/deposition --no_ssl_verify deposition create -t xray -e wbueno@ebi.ac.uk -u 0000-0001-6872-1814,0000-0003-0599-3569 -c "United Kingdom"`

Allowed experiment types are `xray`, `fiber`, `neutron`, `em`, `ec`, `nmr`, `ssnmr`.

If you are creating an EM deposition, you also MUST specify the subtype using the `-s` option. Allowed subtypes are `helical`, `single`, `subtomogram`, `tomography`. Example:

`python cli.py -h http://local.wwpdb.org:12000/deposition --no_ssl_verify deposition create -t em -s helical -e wbueno@ebi.ac.uk -u 0000-0001-6872-1814,0000-0003-0599-3569 -c "United Kingdom"`

Also, for EM and EC depositions, you may specify a related EMDB code using the `-E` option.

For NMR depositions, you may specify a related BMRB code using the `-B` option.

## Deposition details

Use the command `python cli.py deposition get <dep_id>` to get details of a deposition.

## Users

The commands below can be used to manage users access for a deposition (add, remove, get):

```
python cli.py users get <dep_id>
python cli.py users add <dep_id> <user_orcid>
python cli.py users remove <dep_id> <user_orcid>
```

## Files

As it is with users, files have their own command group. To upload a file, you need to run:

`python cli.py files upload <dep_id> <file_path> <file_type>`

Allowed file types are:

- `layer-lines`: Layer line data
- `fsc-xml`: FSC file (XML format)
- `co-pdb`: Coordinates (PDB format)
- `co-cif`: Coordinates (mmCIF format)
- `vo-map`: EM map (MRC/CCP4 format)
- `img-emdb`: Entry image for public display
- `add-map`: Additional EM map (MRC/CCP4 format)
- `mask-map`: EM mask (MRC/CCP4 format)
- `half-map`: EM half map (MRC/CCP4 format)
- `co-cif`: Coordinates (mmCIF format)
- `vo-map`: EM map (MRC/CCP4 format)
- `img-emdb`: Entry image for public display
- `add-map`: Additional EM map (MRC/CCP4 format)
- `mask-map`: EM mask (MRC/CCP4 format)
- `half-map`: EM half map (MRC/CCP4 format)
- `xs-cif`: mmCIF (structure factors)
- `xs-mtz`: MTZ
- `co-cif`: Coordinates (mmCIF format)
- `xs-cif`: mmCIF (structure factors)
- `xs-mtz`: MTZ
- `xa-par`: Parameter file
- `xa-top`: Topology file
- `xa-mat`: Virus matrix
- `co-pdb`: Coordinates (PDB format)
- `co-cif`: Coordinates (mmCIF format)
- `nm-shi`: Assigned chemical shift file (NMR-STAR V3.1 format)
- `nm-res-amb`: Restraint file (AMBER format)
- `nm-aux-amb`: Topology file (AMBER format)
- `nm-res-bio`: Restraint file (BIOSYM format)
- `nm-res-cha`: Restraint file (CHARMM format)
- `nm-res-cns`: Restraint file (CNS format)
- `nm-res-cya`: Restraint file (CYANA format)
- `nm-res-dyn`: Restraint file (DYNAMO/PALES/TALOS format)
- `nm-res-gro`: Restraint file (GROMACS format)
- `nm-aux-gro`: Topology file (GROMACS format)
- `nm-res-isd`: Restraint file (ISD format)
- `nm-res-ros`: Restraint file (ROSETTA format)
- `nm-res-syb`: Restraint file (SYBYL format)
- `nm-res-xpl`: Restraint file (XPLOR-NIH format)
- `nm-res-oth`: Restraint file (other format)
- `nm-pea-any`: Spectral peak list file (any format)
- `nm-uni-nef`: NMR Unified Data (NEF, NMR Exchange Format)
- `nm-uni-str`: NMR Unified Data (NMR-STAR V3.2 format)

## Process

After uploading files, we can start the processing step with the `deposition process` command. To get the status of the processing step, run the `deposition status` command.

`python cli.py deposition process <dep_id>`
`python cli.py deposition status <dep_id>`

To process EM data, you will need to provide a JSON file informing the pixel spacing and contour level for each uploaded map. This file must be in the following format: [{"file_id": X, "spacing": Y, "contour": Z}, ...]

`python cli.py deposition process <dep_id> -V <path_to_json_file>`
