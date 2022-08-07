# ocpi
Python implementation of the Open Charge Point Interface (OCPI)

![Alt text](https://github.com/TECHS-Technological-Solutions/ocpi/blob/master/OCPI.png "feature development roadmap")


# How Does it Work?
Modules that communicate with central system will use crud for retrieving required data. the data that is retrieved from central system may
not be compatible with OCPI protocol. So the data will be passed to adapter to make it compatible with schemas defined by OCPI. User only needs to
modify crud and adapter based on central system architecture.

## License

This project is licensed under the terms of the MIT license.
