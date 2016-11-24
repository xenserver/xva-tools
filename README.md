# xva-tools

[![Build Status](https://travis-ci.org/xenserver/xva-tools.svg?branch=master)](https://travis-ci.org/xenserver/xva-tools)
[![Coverage Status](https://coveralls.io/repos/xenserver/xva-tools/badge.png?branch=master)](https://coveralls.io/r/xenserver/xva-tools?branch=master)

Tools for creating and modifying XVA images.

# Examples

## Modifying XVA

In some cases, it may be necessery to alter metadata captured in an exported XVA file. In order to create a new XVA with updated metadata you can use `xva-update` like so:

    xva-update -f input.xva --product-version 6.5.0 --xapi-minor 4 -o output.xva
    
**Warning:** Modyfing an XVAs metadata may result in bad things happening on import, hence please use carefully.
