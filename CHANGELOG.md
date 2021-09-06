# SAMS Changelog

## [0.3.0] 2021-09-06
### Features
- [SDESK-6144] New endpoints for image renditions (#44)

### Improvements
- chore(docs): Update docs

## [0.2.4] 2021-06-23
### Improvements
- chore(docs): Update docs (#2113664)

### Fixes
- fix(docs): Fix documentation for StorageProviders (#e07d925)
- [SDESK-6002] fix: Slow responses due to mocked notification_client (#38)

## [0.2.3] 2021-05-06
### Improvements
- fix(run): Allow apps to be started without gunicorn (#91cdb3a)

### Fixes
- fix(file_server): Allow python modules for config (#48a9ef6)

## [0.2.2] 2021-05-06
### Improvements
- Support Python 3.8

### Fixes
- fix(api): Convert uploaded bytes to BytesIO before processing (#1428499)
- Use official pypi package for Superdesk-Core (#ee45aff)
- fix(docs): Fix building for readthedocs (#e2157f3)
- fix(behave-tests): Increase timedelta for __now__ value (#572db66)

## [0.2.1] 2021-05-04
### Improvements
- [SDESK-5581] Ability to add Tags to Asset Metadata (#37)

### Fixes
- Use superdesk-core/develop branch (#169fd8f)

## [0.2.0] 2021-02-17
### Features
- [SDESK-5638] New File Server app (#23)
- [SDESK-5668] Endpoints to lock and unlock assets (#30)

### Improvements
- [SDESK-5656] Client function to get list of Asset tags (#25)
- chore(packages): Clean up requirement and setup files (#28)
- [SDESK-5667] Provide external user IDs to requests. (#27)
- [SDESK-5710] Force attribute to unlock asset endpoint. (#35)
- [SDESK-5713] Endpoint to unlock assets based on user ID. (#36)

### Fixes
- [SDESK-5594] Custom elastic tokenizer for name and filename fields (#24)
- [SDESK-5265] updated asset name schema. (#26)
- fix(unit_tests): Add test request context (#29)
- [SDESK-5668] fix: Modified error description (#32)
- [SDESK-5668] fix: replaced #DATE# with __now__ in test features. (#34)

## [0.1.0] 2020-10-30
- [SDESK-5579] Configurable Asset size validation (#22)
- [SDESK-5291] Add AmazonS3 StorageProvider (#20)
- [SDESK-5480] Endpoint to compress and download multiple asset binaries (#19)
- [SDESK-5418] Improve response headers for Asset binary API (#18)
- [SDESK-5478] Delete disabled set with no asset (#17)
- [SDESK-5520] Add elastic manage commands (#16)
- [SDESK-5475] Get count of assets for given sets (#15)
- [SDESK-5476] Update: asset upload error if set state draft or disabled (#14)
- [SDESK-5473] Add custom SAMS Exception classes (#13)
- [SDESK-5472] Sort storage destinations alphabetically by _id (#12)
- fix(tests): Set API_VERSION to be empty (#11)
- [SDESK-5416] client for asset management (#10)
- [SDESK-5288] Asset resource and service (#9)
- [SDESK-5363] Add SAMS_ prefix to config env vars (#8)
- [SDESK-5360] Sets public interface (#7)
- [SDESK-5361] add basic auth in client and server (#6)
- [SDESK-5359] storage destinations public interface (#5)
- [SDESK-5358] Implement core sams client library (#4)
- [SDESK-5286] Storage and Destination providers (#3)
- [SDESK-5287] Set resource and service (#2)
- [SDESK-5285] Skeleton application structure (#1)

## June 2020
- Initial commit
