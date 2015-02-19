# Contributing

## Requirements

You need to have Python 2.7 installed with jsonschema.
The easy way to install the jsonchema package is through `pip`.
This is achieved with the following command from the repository root:

```sh
pip install -r 'requirements.txt'
```

> Note: You may need to run the pip installation as root using `sudo` or similar methods.

## Which branch?

Please submit all requests against the master branch.

## Add a new device

1. Add a new folder that follows the [naming contention](#folder-naming-convention)
2. In that folder add a `device.json` file that fulfills the required [scheme](#scheme).
3. To verify your device will be properly see [test changes](#test-changes).
4. Submit a pull request.

## Update an existing device

Modify the existing `devices.json` file to reflect the latest correct information about a device.
Then [test the changes](#test-changes) before submitting a pull request.

## Folder naming convention

Folders for device information follow this naming pattern: `{vendor}-{device}-{version}`.
For example:

* Google Nexus 7 - `google-nexus-7`
* Samsung Galaxy S4 - `samsung-galaxy-s4` 

## What not to commit

Do not commit the `devices.json` file in the root folder.
Other than this one limitation, you may submit edits to any other files.

If you have added the file to be commited already, you can do `git reset devices.json` to remove it from the add.
If you have already commited the addition, then you will need to [modify the commit](http://stackoverflow.com/a/1186549).

## Scheme

The following are allowed properties within a `device.json` file.

- **`type`** should be one of the `phone`, `tablet`, `notebook`, `desktop`, `unknown`;
- **`capabilities`** should listen enabled capabilities for the device (currently supported: `mobile`, `touch`);
- **`screen`** describes the physical device screen size and dpr in horizontal and vertical orientations;
- **`outline`** provides an image to draw around the screen;
- **`modes`** represent different browser states on the screen (e.g. with/without on-screen keyboard);
- **`page-rect`** is the rect relative to the `screen` size (see above), where web page is displayed; this rect will be emulated;
- **`title`** values should be user-readable.

All sizes in should be in device independent pixels

The following code sample is a minimum viable `device.json`:

```json
{
    "title": "My Awesome Device",
    "type": "notebook",
    "screen": {
        "horizontal": {
            "width": 1024, 
            "height": 968
        }, 
        "device-pixel-ratio": 1, 
        "vertical": {
            "width": 968, 
            "height": 1024
        }
    },
    "user-agent": "Latest UA for given device",
    "show-by-default": false
}
```

## Test changes

To test that your changes will work run `generate_devices_list.py`.
