# CHANGELOG


## v0.3.4 (2025-06-19)

### Bug Fixes

- **logging**: Fix typo
  ([`3515379`](https://github.com/raider444/psytican-bot/commit/3515379b3816f2dee1c2c52dd8ab49a41d63cab0))


## v0.3.3 (2025-06-19)

### Bug Fixes

- **logging**: Exclude metrics endpoint from logs
  ([`41b9096`](https://github.com/raider444/psytican-bot/commit/41b90964d4008942a7182b48a94bc8319a2f762a))


## v0.3.2 (2025-06-19)

### Bug Fixes

- **deps**: Update dependencies
  ([`9f898ae`](https://github.com/raider444/psytican-bot/commit/9f898ae0f439b68ee2e4282b9545ec239637dfd6))

### Chores

- **deps**: Bump requests in the pip group across 1 directory
  ([`8c48c33`](https://github.com/raider444/psytican-bot/commit/8c48c3320bf115e0cfd37d41ab37f52fcbe5a2c9))

Bumps the pip group with 1 update in the / directory: [requests](https://github.com/psf/requests).

Updates `requests` from 2.32.3 to 2.32.4 - [Release notes](https://github.com/psf/requests/releases)
  - [Changelog](https://github.com/psf/requests/blob/main/HISTORY.md) -
  [Commits](https://github.com/psf/requests/compare/v2.32.3...v2.32.4)

--- updated-dependencies: - dependency-name: requests dependency-version: 2.32.4

dependency-type: indirect

dependency-group: pip

...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump urllib3 in the pip group across 1 directory
  ([`e86592e`](https://github.com/raider444/psytican-bot/commit/e86592e3dc2f1ad127b0ef281739141e4a0ad84d))

Bumps the pip group with 1 update in the / directory: [urllib3](https://github.com/urllib3/urllib3).

Updates `urllib3` from 2.3.0 to 2.5.0 - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst) -
  [Commits](https://github.com/urllib3/urllib3/compare/2.3.0...2.5.0)

--- updated-dependencies: - dependency-name: urllib3 dependency-version: 2.5.0

dependency-type: indirect

dependency-group: pip

...

Signed-off-by: dependabot[bot] <support@github.com>


## v0.3.1 (2025-01-16)

### Bug Fixes

- **cicd**: Fix semantic-relese
  ([`670cfe4`](https://github.com/raider444/psytican-bot/commit/670cfe4cc4b91b02055a6c61826c57ba2130a1e9))

- **dependencies**: Update ci/cd
  ([`109ca40`](https://github.com/raider444/psytican-bot/commit/109ca409ff2af727a338b6be62d15ee70e535835))

### Chores

- **deps-dev**: Bump jinja2 in the pip group across 1 directory
  ([`5f634e0`](https://github.com/raider444/psytican-bot/commit/5f634e0c64e138ea793b3253653aaf01dd242ae1))

Bumps the pip group with 1 update in the / directory: [jinja2](https://github.com/pallets/jinja).

Updates `jinja2` from 3.1.4 to 3.1.5 - [Release notes](https://github.com/pallets/jinja/releases) -
  [Changelog](https://github.com/pallets/jinja/blob/main/CHANGES.rst) -
  [Commits](https://github.com/pallets/jinja/compare/3.1.4...3.1.5)

--- updated-dependencies: - dependency-name: jinja2 dependency-type: indirect

dependency-group: pip

...

Signed-off-by: dependabot[bot] <support@github.com>


## v0.3.0 (2024-11-27)

### Bug Fixes

- **#27**: Fixed stcuks and wrong menu drops on conversations
  ([`eaa78ba`](https://github.com/raider444/psytican-bot/commit/eaa78bac95b8a2434053a62b7b7f68600cac8146))

- **converstions**: Fix "cancel" stuck #27
  ([`f2f29c6`](https://github.com/raider444/psytican-bot/commit/f2f29c693db285d58cff859aefe635343409a4b8))

- **converstions**: Fix stcuks and wrong menu drops on conversations #27
  ([`b9c33d1`](https://github.com/raider444/psytican-bot/commit/b9c33d194d8b2c57e7ab39075c8f651c7b760650))

- **gcalendar**: Implement credentials memory cache
  ([`2d04b3e`](https://github.com/raider444/psytican-bot/commit/2d04b3e710b6d9cdffdadcf462b009b5bd0201f9))

### Cicd

- **helm**: Update helm chart
  ([`a282690`](https://github.com/raider444/psytican-bot/commit/a2826900025fb4a7f285f5cf42fa4342f1494d17))

### Features

- **booking**: Implement fast one command booking #34
  ([`a99cd1d`](https://github.com/raider444/psytican-bot/commit/a99cd1ded237e1c4370e2d41dae0e95707ab576c))

feat(booking): Implement fast one command booking #34

- **booking**: Implement fast one command booking #34
  ([`88b3c97`](https://github.com/raider444/psytican-bot/commit/88b3c9732ac1677fe9365698c1481c8d4760fb27))

- **event_list**: Add information about booking owner in "get events" #31
  ([`9390778`](https://github.com/raider444/psytican-bot/commit/9390778839820f6e5bfda21ee41ad2510cd8b5c7))

- **event_list**: Foreign event is now clickable #32
  ([#37](https://github.com/raider444/psytican-bot/pull/37),
  [`c70f8e7`](https://github.com/raider444/psytican-bot/commit/c70f8e7f081fc6eb17d29a8950b937b3ab82e544))

- **persistense**: Implement bot persistence #3
  ([`1a2982e`](https://github.com/raider444/psytican-bot/commit/1a2982e10f5a02507cdafc13c62e9f948c37d7a3))

- **tg_wrapper**: Implemented silent replies to avoid notification spam #30
  ([`3d04231`](https://github.com/raider444/psytican-bot/commit/3d042319f53e2d5211f495454d1132c82297e8a1))


## v0.2.7 (2024-10-16)

### Bug Fixes

- **update_acls #18**: Fix broken update_acls
  ([`3a12e48`](https://github.com/raider444/psytican-bot/commit/3a12e484d120c74ff851046168f214c1a2dc4fb5))


## v0.2.6 (2024-10-16)

### Bug Fixes

- **logger #18**: Prettify logging
  ([`b07c24c`](https://github.com/raider444/psytican-bot/commit/b07c24c587a69139978d71493be5dcc2e6961fef))


## v0.2.5 (2024-10-15)

### Bug Fixes

- **security**: Update starlette and dependencies
  ([`2fe4ed6`](https://github.com/raider444/psytican-bot/commit/2fe4ed64408e349d456289041e1495f6a4a64258))

### Cicd

- **#4**: Make possible to build dev docker image without args and target definitions
  ([`b891a67`](https://github.com/raider444/psytican-bot/commit/b891a67e7be9fb3b73112b98c6314c12940d07c0))

- **Dockerfile**: Merge pull request #22 from raider444:migrate-to-alpine
  ([`fbd7501`](https://github.com/raider444/psytican-bot/commit/fbd7501082aee0c84d2757a691e279e8c8626228))

cicd(Dockerfile): Migrate to alpine

- **Dockerfile**: Migrate to alpine
  ([`ffcbbbb`](https://github.com/raider444/psytican-bot/commit/ffcbbbb649baf79ad0e70816e3b5c321e14faf91))

- **helm**: Fix container image in values
  ([`3d64c3a`](https://github.com/raider444/psytican-bot/commit/3d64c3af59c08b6803e553b67cc89825a9a7231d))


## v0.2.4 (2024-10-15)


## v0.2.4-rc.3 (2024-10-15)

### Bug Fixes

- **Implement bot persistence #3**: Bump rc version
  ([`0b67166`](https://github.com/raider444/psytican-bot/commit/0b67166b46484a755111e1a66f457ca00ad65a53))

### Cicd

- **Create pipeline #4**: Don't build images if no new version created
  ([`f5516a5`](https://github.com/raider444/psytican-bot/commit/f5516a5abb8be33943ee3bdea6ab7678ef7f7e39))

- **Create pipeline #4**: Fix pypi access
  ([`b18cd56`](https://github.com/raider444/psytican-bot/commit/b18cd56bdc95bca311d33b17f8763bb43da662d3))

- **Create pipeline #4**: Fix pypi access and remove docker push from ci workflow
  ([`b2d06e8`](https://github.com/raider444/psytican-bot/commit/b2d06e83fa509dedfb09d5076b15333fc96e5d1d))

- **Create pipeline #4**: Update semantic-release pat
  ([`83f0ce7`](https://github.com/raider444/psytican-bot/commit/83f0ce74576e2b276a17e0fe94ccb76a628b6ec2))

- **Create pipeline #4**: Update semantic-release pat for checkout step
  ([`19fd477`](https://github.com/raider444/psytican-bot/commit/19fd47739932ce2f5cda115ec74fc7a90c81eca8))


## v0.2.4-rc.2 (2024-10-15)

### Bug Fixes

- **tg_wrapper**: Fix release workflow
  ([`b1b61c7`](https://github.com/raider444/psytican-bot/commit/b1b61c7cc4b9f0f746e6dcf2f31dd248f9e529c6))


## v0.2.4-rc.1 (2024-10-15)

### Bug Fixes

- **all**: Increase INFO log verbosity
  ([`14e10d5`](https://github.com/raider444/psytican-bot/commit/14e10d5403e06e40a3d4c9a827af190062e855b4))

- **tg_wrapper**: Move pencil to the beginning of the button
  ([`e88bead`](https://github.com/raider444/psytican-bot/commit/e88bead471e52039a12bf33afe00f66c15ecc1c9))

### Chores

- **code of conduct**: Add conditions
  ([`42606ea`](https://github.com/raider444/psytican-bot/commit/42606eadae3c437ca845fc5447c3321f2e72aae2))

- **code of conduct**: Add trailing cr
  ([`ffd69fa`](https://github.com/raider444/psytican-bot/commit/ffd69faa0106e33a8551f263b04940048b7e3178))

- **code of conduct**: Fix workflow description
  ([`ea84317`](https://github.com/raider444/psytican-bot/commit/ea84317e397f03c88978eb002e961280e411bdbb))

- **code of conduct**: Remove all jobs conditions
  ([`4fb99e7`](https://github.com/raider444/psytican-bot/commit/4fb99e7c149f38b97a71747454c5eca0a8474115))

- **code of conduct**: Rename workflows
  ([`743a93d`](https://github.com/raider444/psytican-bot/commit/743a93db258ce2f66f3fca03d45610489a953a6c))

- **code of conduct**: Sequential workflow run
  ([`8a7846b`](https://github.com/raider444/psytican-bot/commit/8a7846bc388560bba09066ba60b5573248630ec3))

- **code of conduct**: Test job conditions
  ([`bd45300`](https://github.com/raider444/psytican-bot/commit/bd453001c0fa71341a053a308643fa397f0da672))

- **code of conduct**: Test job sequence
  ([`42c1d9f`](https://github.com/raider444/psytican-bot/commit/42c1d9fc4ec040c74fd98bf99d918a49dfa9f843))

- **code of conduct**: Test job sequence 2
  ([`2566e93`](https://github.com/raider444/psytican-bot/commit/2566e93513b2d878f8165c7679563f4ff64e01e4))

### Cicd

- **Create pipeline #4**: Add dockerfile labels
  ([`bf2c240`](https://github.com/raider444/psytican-bot/commit/bf2c2408336c371e12e034007613724d924bd384))

- **Create pipeline #4**: Add junit reports
  ([`2cfee7e`](https://github.com/raider444/psytican-bot/commit/2cfee7e6a6114163d43579b836bca84e56337fcd))

- **Create pipeline #4**: Add pre-build checks
  ([`8004eda`](https://github.com/raider444/psytican-bot/commit/8004edafc93f95238c4370d83b473846697f2552))

- **Create pipeline #4**: Check helm chart build
  ([`dcbfce2`](https://github.com/raider444/psytican-bot/commit/dcbfce275b22c2ea89a2b8160c377091adc47fe0))

- **Create pipeline #4**: Check semantic-release
  ([`84f897e`](https://github.com/raider444/psytican-bot/commit/84f897e1be4525e4db60f965cfae6b5128573c99))

- **Create pipeline #4**: Dirty implementation of semantic-release
  ([`8bf4a4d`](https://github.com/raider444/psytican-bot/commit/8bf4a4d55c08163653203eaadb00517a4e5a7208))

- **Create pipeline #4**: Fix bad outputs
  ([`03a78b0`](https://github.com/raider444/psytican-bot/commit/03a78b0c73a5db60c82b7e5b2ce9044867704e03))

- **Create pipeline #4**: Fix Check helm chart build
  ([`bbab8b2`](https://github.com/raider444/psytican-bot/commit/bbab8b2a079ad7a6bca7ff5918d676d73e96ae9d))

- **Create pipeline #4**: Fix docker registry permissions
  ([`f2537d2`](https://github.com/raider444/psytican-bot/commit/f2537d299a6ea32affd9a33aba1b299f361acffb))

- **Create pipeline #4**: Fix env varables for pytest
  ([`10d81fd`](https://github.com/raider444/psytican-bot/commit/10d81fd447368a4edeae5c92379a2026ced2ae2a))

- **Create pipeline #4**: Fix junit reports
  ([`af234fa`](https://github.com/raider444/psytican-bot/commit/af234faf9e71e7cf9f3d777b211698d792663b37))

- **Create pipeline #4**: Fix permissions
  ([`6da49be`](https://github.com/raider444/psytican-bot/commit/6da49be4c3fa4c6c895bd4b784ac95ce1d7659a3))

- **Create pipeline #4**: Fix some small problems
  ([`125c17c`](https://github.com/raider444/psytican-bot/commit/125c17c1f52d904366b56b4eab278808541d6afb))

- **Create pipeline #4**: Follow semantic-release deprecation notes
  ([`d36c0f5`](https://github.com/raider444/psytican-bot/commit/d36c0f565af44c868a11a70f85c1731e079c68da))

- **Create pipeline #4**: Limit token permissions
  ([`d482a72`](https://github.com/raider444/psytican-bot/commit/d482a727a4b1b9a9b6804505a168d9af6db3867f))

- **Create pipeline #4**: Re pre-release
  ([`4dece1c`](https://github.com/raider444/psytican-bot/commit/4dece1ce7b46f40a2f6e2f0ccd65239a1c4d7ec2))

- **Create pipeline #4**: Re pre-release attepmt 2
  ([`9645710`](https://github.com/raider444/psytican-bot/commit/9645710e0fe48d85946ad20170cd4e192ce25d47))

- **Create pipeline #4**: Re pre-release attepmt 3
  ([`ec719f6`](https://github.com/raider444/psytican-bot/commit/ec719f68ba39622216a624168f3319f9a999dd70))

- **Create pipeline #4**: Re pre-release attepmt 4
  ([`b974072`](https://github.com/raider444/psytican-bot/commit/b974072221510bd8221b8fda2fe12f550c7e2078))

- **Create pipeline #4**: Re pre-release attepmt 5
  ([`716cf35`](https://github.com/raider444/psytican-bot/commit/716cf35295935814d24ef89efcdc4628d609c23f))

- **Create pipeline #4**: Re pre-release attepmt 6
  ([`e56576f`](https://github.com/raider444/psytican-bot/commit/e56576f5889829feb6eb4eb829186c668e9e3d7e))

- **Create pipeline #4**: Semantic release implemented
  ([`6ac8756`](https://github.com/raider444/psytican-bot/commit/6ac87567b8f71ae864495a3f90866ff3d8eb980a))

- **Create pipeline #4**: Try another reporter
  ([`69b2b64`](https://github.com/raider444/psytican-bot/commit/69b2b64511310a47fa89c3a8efdf412a401fc0b7))

- **Create pipeline #4**: Try another reporter 2
  ([`f810f13`](https://github.com/raider444/psytican-bot/commit/f810f132d0db8adb0988471abb466b396a09f15c))

- **Create pipeline #4**: Update cache version
  ([`0f6fd44`](https://github.com/raider444/psytican-bot/commit/0f6fd44e4d403bb4a42e2d1311a12ccd75fe180a))

- **github actions**: Build and images and charts, semantic-release
  ([`4fc80ed`](https://github.com/raider444/psytican-bot/commit/4fc80ed93bb25cc5bec8ce0bece69fba0a9aeca6))

* chore(code of conduct): Remove comments from workflow

* chore(code of conduct): Merge all to one workflow

* chore(code of conduct): run

* cicd(Create pipeline #4): Disable pypi publish on pre-releases

* cicd(Create pipeline #4): Understand what this does

* cicd(Create pipeline #4): Add workflow for image build on tags

* cicd(Create pipeline #4): Fix typo

* cicd(Create pipeline #4): Fix output definition

* cicd(Create pipeline #4): Add docker cache

* cicd(Create pipeline #4): Use oci cache

* cicd(Create pipeline #4): Setup buildx builder

* cicd(Create pipeline #4): Fix dockerfile for prod

* cicd(Create pipeline #4): Fix dockerfile for develop

* cicd(Create pipeline #4): CD part done


## v0.2.3 (2024-10-01)

### Bug Fixes

- **tg_wrapper**: Add text description of events, fix regex
  ([`2f271c5`](https://github.com/raider444/psytican-bot/commit/2f271c5d9e0e451e631823c2943cf23ffc44ed3f))


## v0.2.2 (2024-10-01)

### Bug Fixes

- **calendar**: Fix bug with month selecting
  ([`57f428d`](https://github.com/raider444/psytican-bot/commit/57f428dac369061f42ee5229c9ba1a94894658de))

### Feature

- **telegram**: #2 Dirty implementation of acl draft
  ([`e4f3a5d`](https://github.com/raider444/psytican-bot/commit/e4f3a5dd195e4d38fcbc47f39d229691bdaea5d7))
