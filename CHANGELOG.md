# CHANGELOG


## v0.3.0 (2024-11-27)

### Cicd

* cicd(helm): Update helm chart ([`a282690`](https://github.com/raider444/psytican-bot/commit/a2826900025fb4a7f285f5cf42fa4342f1494d17))

### Features

* feat(booking): Implement fast one command booking  #34

feat(booking): Implement fast one command booking  #34 ([`a99cd1d`](https://github.com/raider444/psytican-bot/commit/a99cd1ded237e1c4370e2d41dae0e95707ab576c))

* feat(booking): Implement fast one command booking  #34 ([`88b3c97`](https://github.com/raider444/psytican-bot/commit/88b3c9732ac1677fe9365698c1481c8d4760fb27))

* feat(event_list): Foreign event is now clickable #32 (#37) ([`c70f8e7`](https://github.com/raider444/psytican-bot/commit/c70f8e7f081fc6eb17d29a8950b937b3ab82e544))

* feat(event_list): Add information about booking owner in "get events" #31 ([`9390778`](https://github.com/raider444/psytican-bot/commit/9390778839820f6e5bfda21ee41ad2510cd8b5c7))

* feat(tg_wrapper): Implemented silent replies to avoid notification spam #30 ([`3d04231`](https://github.com/raider444/psytican-bot/commit/3d042319f53e2d5211f495454d1132c82297e8a1))

* feat(persistense): Implement bot persistence #3 ([`1a2982e`](https://github.com/raider444/psytican-bot/commit/1a2982e10f5a02507cdafc13c62e9f948c37d7a3))

### Fixes

* fix(#27): Fixed stcuks and wrong menu drops on conversations ([`eaa78ba`](https://github.com/raider444/psytican-bot/commit/eaa78bac95b8a2434053a62b7b7f68600cac8146))

* fix(converstions): Fix "cancel" stuck #27 ([`f2f29c6`](https://github.com/raider444/psytican-bot/commit/f2f29c693db285d58cff859aefe635343409a4b8))

* fix(converstions): Fix stcuks and wrong menu drops on conversations #27 ([`b9c33d1`](https://github.com/raider444/psytican-bot/commit/b9c33d194d8b2c57e7ab39075c8f651c7b760650))

* fix(gcalendar): Implement credentials memory cache ([`2d04b3e`](https://github.com/raider444/psytican-bot/commit/2d04b3e710b6d9cdffdadcf462b009b5bd0201f9))

### Unknown

* Merge pull request #38 from raider444/develop

feat(bot): Multiple features and fixes ([`be0b5b4`](https://github.com/raider444/psytican-bot/commit/be0b5b41b103035af1e15db7cf44666caf705931))

* Merge pull request #36 from raider444:feature/event-owner-information

feat(event_list): Add information about booking owner in "get events" #31 ([`c5d5901`](https://github.com/raider444/psytican-bot/commit/c5d590124623137ffc58b831489a011aa25aa474))

* Merge pull request #35 from raider444:silent-notifications

feat(tg_wrapper): Implemented silent replies to avoid notification spam #30 ([`435cea1`](https://github.com/raider444/psytican-bot/commit/435cea1a4c6d3af279ad71da23e4f1eaef44584f))

* Merge pull request #29 from raider444/fix-converstation-stuck

fix(conversations): Fix stcuks and wrong menu drops on conversations #27 ([`e5d9a3d`](https://github.com/raider444/psytican-bot/commit/e5d9a3d0413981bb6d3c25f28387b1f2b2887634))

* Merge branch 'develop' into fix-converstation-stuck ([`f358aea`](https://github.com/raider444/psytican-bot/commit/f358aea339974514b8565c3b71efaee0fb65ba4d))

* Merge pull request #28 from raider444/feat-presistence

feat(persistense): Implement persistense ([`25b2b36`](https://github.com/raider444/psytican-bot/commit/25b2b3603109460c306f1363440dbba481d97560))


## v0.2.7 (2024-10-16)

### Fixes

* fix(update_acls #18): Fix broken update_acls ([`3a12e48`](https://github.com/raider444/psytican-bot/commit/3a12e484d120c74ff851046168f214c1a2dc4fb5))

### Unknown

* Merge pull request #26 from raider444:fix/update-acls-bug

fix(update_acls #18): Fix broken update_acls ([`867488e`](https://github.com/raider444/psytican-bot/commit/867488ea00e528306873d14df90b39aacd98e74b))


## v0.2.6 (2024-10-16)

### Fixes

* fix(logger #18): Prettify logging ([`b07c24c`](https://github.com/raider444/psytican-bot/commit/b07c24c587a69139978d71493be5dcc2e6961fef))

### Unknown

* Merge pull request #25 from raider444:fix/prettify-logs ([`c501d3c`](https://github.com/raider444/psytican-bot/commit/c501d3c732636f0b533ccffeb0aa21c4c38605d6))


## v0.2.5 (2024-10-15)

### Cicd

* cicd(#4): Make possible to build dev docker image without args and target definitions ([`b891a67`](https://github.com/raider444/psytican-bot/commit/b891a67e7be9fb3b73112b98c6314c12940d07c0))

* cicd(Dockerfile): Merge pull request #22 from raider444:migrate-to-alpine

cicd(Dockerfile): Migrate to alpine ([`fbd7501`](https://github.com/raider444/psytican-bot/commit/fbd7501082aee0c84d2757a691e279e8c8626228))

* cicd(Dockerfile): Migrate to alpine ([`ffcbbbb`](https://github.com/raider444/psytican-bot/commit/ffcbbbb649baf79ad0e70816e3b5c321e14faf91))

* cicd(helm): Fix container image in values ([`3d64c3a`](https://github.com/raider444/psytican-bot/commit/3d64c3af59c08b6803e553b67cc89825a9a7231d))

### Fixes

* fix(security): Update starlette and dependencies ([`2fe4ed6`](https://github.com/raider444/psytican-bot/commit/2fe4ed64408e349d456289041e1495f6a4a64258))

### Unknown

* Merge pull request #24 from raider444:hotfix/CVE-2024-47874

fix(security): Update starlette and dependencies ([`32b7f79`](https://github.com/raider444/psytican-bot/commit/32b7f791fa17d85686f79b7c4c7ad494ea0e4be6))

* Merge pull request #23 from raider444:refactor-dockerfile

cicd(#4): Refactor dockerfile ([`c48d831`](https://github.com/raider444/psytican-bot/commit/c48d831e1be9d045cfbc655b2e1b1f66240dfe97))

* Merge pull request #21 from raider444/ci/fix-docker-and-helm

cicd(helm): Fix container image in values ([`b23e03a`](https://github.com/raider444/psytican-bot/commit/b23e03a3739f5daf9e3182413ac262d50a1fa626))


## v0.2.4 (2024-10-15)

### Unknown

* Merge pull request #20 from raider444/release/0.2.4

Release/0.2.4 ([`e5cafb4`](https://github.com/raider444/psytican-bot/commit/e5cafb4bf363d556d0ae87d52db3604e7e4a510a))

* Merge branch 'main' into release/0.2.4 ([`a9a1f15`](https://github.com/raider444/psytican-bot/commit/a9a1f156dbdea1643d004b01601309b12eb1387b))


## v0.2.4-rc.3 (2024-10-15)

### Cicd

* cicd(Create pipeline #4): Fix pypi access and remove docker push from ci workflow ([`b2d06e8`](https://github.com/raider444/psytican-bot/commit/b2d06e83fa509dedfb09d5076b15333fc96e5d1d))

* cicd(Create pipeline #4): Fix pypi access ([`b18cd56`](https://github.com/raider444/psytican-bot/commit/b18cd56bdc95bca311d33b17f8763bb43da662d3))

* cicd(Create pipeline #4): Update semantic-release pat for checkout step ([`19fd477`](https://github.com/raider444/psytican-bot/commit/19fd47739932ce2f5cda115ec74fc7a90c81eca8))

* cicd(Create pipeline #4): Update semantic-release pat ([`83f0ce7`](https://github.com/raider444/psytican-bot/commit/83f0ce74576e2b276a17e0fe94ccb76a628b6ec2))

* cicd(Create pipeline #4): Don't build images if no new version created ([`f5516a5`](https://github.com/raider444/psytican-bot/commit/f5516a5abb8be33943ee3bdea6ab7678ef7f7e39))

### Fixes

* fix(Implement bot persistence #3): bump rc version ([`0b67166`](https://github.com/raider444/psytican-bot/commit/0b67166b46484a755111e1a66f457ca00ad65a53))

### Unknown

* Merge pull request #19 from raider444/fix-logs-and-text-refactor

fix(all): Increase INFO log verbosity and change pencil position ([`b14160b`](https://github.com/raider444/psytican-bot/commit/b14160b8bb0121ab77416468f2fcf237a3770cb7))


## v0.2.4-rc.2 (2024-10-15)

### Fixes

* fix(tg_wrapper): Fix release workflow ([`b1b61c7`](https://github.com/raider444/psytican-bot/commit/b1b61c7cc4b9f0f746e6dcf2f31dd248f9e529c6))


## v0.2.4-rc.1 (2024-10-15)

### Chores

* chore(code of conduct): Add conditions ([`42606ea`](https://github.com/raider444/psytican-bot/commit/42606eadae3c437ca845fc5447c3321f2e72aae2))

* chore(code of conduct): Rename workflows ([`743a93d`](https://github.com/raider444/psytican-bot/commit/743a93db258ce2f66f3fca03d45610489a953a6c))

* chore(code of conduct): Fix workflow description ([`ea84317`](https://github.com/raider444/psytican-bot/commit/ea84317e397f03c88978eb002e961280e411bdbb))

* chore(code of conduct): Remove all jobs conditions ([`4fb99e7`](https://github.com/raider444/psytican-bot/commit/4fb99e7c149f38b97a71747454c5eca0a8474115))

* chore(code of conduct): Test job sequence 2 ([`2566e93`](https://github.com/raider444/psytican-bot/commit/2566e93513b2d878f8165c7679563f4ff64e01e4))

* chore(code of conduct): Test job sequence ([`42c1d9f`](https://github.com/raider444/psytican-bot/commit/42c1d9fc4ec040c74fd98bf99d918a49dfa9f843))

* chore(code of conduct): Test job conditions ([`bd45300`](https://github.com/raider444/psytican-bot/commit/bd453001c0fa71341a053a308643fa397f0da672))

* chore(code of conduct): Sequential workflow run ([`8a7846b`](https://github.com/raider444/psytican-bot/commit/8a7846bc388560bba09066ba60b5573248630ec3))

* chore(code of conduct): Add trailing cr ([`ffd69fa`](https://github.com/raider444/psytican-bot/commit/ffd69faa0106e33a8551f263b04940048b7e3178))

### Cicd

* cicd(Create pipeline #4): Fix bad outputs ([`03a78b0`](https://github.com/raider444/psytican-bot/commit/03a78b0c73a5db60c82b7e5b2ce9044867704e03))

* cicd(github actions): Build and images and charts, semantic-release

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

* cicd(Create pipeline #4): CD part done ([`4fc80ed`](https://github.com/raider444/psytican-bot/commit/4fc80ed93bb25cc5bec8ce0bece69fba0a9aeca6))

* cicd(Create pipeline #4): Add dockerfile labels ([`bf2c240`](https://github.com/raider444/psytican-bot/commit/bf2c2408336c371e12e034007613724d924bd384))

* cicd(Create pipeline #4): Semantic release implemented ([`6ac8756`](https://github.com/raider444/psytican-bot/commit/6ac87567b8f71ae864495a3f90866ff3d8eb980a))

* cicd(Create pipeline #4): Fix docker registry permissions ([`f2537d2`](https://github.com/raider444/psytican-bot/commit/f2537d299a6ea32affd9a33aba1b299f361acffb))

* cicd(Create pipeline #4): Re pre-release attepmt 6 ([`e56576f`](https://github.com/raider444/psytican-bot/commit/e56576f5889829feb6eb4eb829186c668e9e3d7e))

* cicd(Create pipeline #4): Re pre-release attepmt 5 ([`716cf35`](https://github.com/raider444/psytican-bot/commit/716cf35295935814d24ef89efcdc4628d609c23f))

* cicd(Create pipeline #4): Re pre-release attepmt 4 ([`b974072`](https://github.com/raider444/psytican-bot/commit/b974072221510bd8221b8fda2fe12f550c7e2078))

* cicd(Create pipeline #4): Re pre-release attepmt 3 ([`ec719f6`](https://github.com/raider444/psytican-bot/commit/ec719f68ba39622216a624168f3319f9a999dd70))

* cicd(Create pipeline #4): Re pre-release attepmt 2 ([`9645710`](https://github.com/raider444/psytican-bot/commit/9645710e0fe48d85946ad20170cd4e192ce25d47))

* cicd(Create pipeline #4): Re pre-release ([`4dece1c`](https://github.com/raider444/psytican-bot/commit/4dece1ce7b46f40a2f6e2f0ccd65239a1c4d7ec2))

* cicd(Create pipeline #4): fix Check helm chart build ([`bbab8b2`](https://github.com/raider444/psytican-bot/commit/bbab8b2a079ad7a6bca7ff5918d676d73e96ae9d))

* cicd(Create pipeline #4): Check helm chart build ([`dcbfce2`](https://github.com/raider444/psytican-bot/commit/dcbfce275b22c2ea89a2b8160c377091adc47fe0))

* cicd(Create pipeline #4): Follow semantic-release deprecation notes ([`d36c0f5`](https://github.com/raider444/psytican-bot/commit/d36c0f565af44c868a11a70f85c1731e079c68da))

* cicd(Create pipeline #4): Check semantic-release ([`84f897e`](https://github.com/raider444/psytican-bot/commit/84f897e1be4525e4db60f965cfae6b5128573c99))

* cicd(Create pipeline #4): Dirty implementation of semantic-release ([`8bf4a4d`](https://github.com/raider444/psytican-bot/commit/8bf4a4d55c08163653203eaadb00517a4e5a7208))

* cicd(Create pipeline #4): Update cache version ([`0f6fd44`](https://github.com/raider444/psytican-bot/commit/0f6fd44e4d403bb4a42e2d1311a12ccd75fe180a))

* cicd(Create pipeline #4): Limit token permissions ([`d482a72`](https://github.com/raider444/psytican-bot/commit/d482a727a4b1b9a9b6804505a168d9af6db3867f))

* cicd(Create pipeline #4): Fix permissions ([`6da49be`](https://github.com/raider444/psytican-bot/commit/6da49be4c3fa4c6c895bd4b784ac95ce1d7659a3))

* cicd(Create pipeline #4): Try another reporter 2 ([`f810f13`](https://github.com/raider444/psytican-bot/commit/f810f132d0db8adb0988471abb466b396a09f15c))

* cicd(Create pipeline #4): Try another reporter ([`69b2b64`](https://github.com/raider444/psytican-bot/commit/69b2b64511310a47fa89c3a8efdf412a401fc0b7))

* cicd(Create pipeline #4): Fix junit reports ([`af234fa`](https://github.com/raider444/psytican-bot/commit/af234faf9e71e7cf9f3d777b211698d792663b37))

* cicd(Create pipeline #4): Add junit reports ([`2cfee7e`](https://github.com/raider444/psytican-bot/commit/2cfee7e6a6114163d43579b836bca84e56337fcd))

* cicd(Create pipeline #4): Fix some small problems ([`125c17c`](https://github.com/raider444/psytican-bot/commit/125c17c1f52d904366b56b4eab278808541d6afb))

* cicd(Create pipeline #4): Fix env varables for pytest ([`10d81fd`](https://github.com/raider444/psytican-bot/commit/10d81fd447368a4edeae5c92379a2026ced2ae2a))

* cicd(Create pipeline #4): Add pre-build checks ([`8004eda`](https://github.com/raider444/psytican-bot/commit/8004edafc93f95238c4370d83b473846697f2552))

### Fixes

* fix(tg_wrapper): Move pencil to the beginning of the button ([`e88bead`](https://github.com/raider444/psytican-bot/commit/e88bead471e52039a12bf33afe00f66c15ecc1c9))

* fix(all): Increase INFO log verbosity ([`14e10d5`](https://github.com/raider444/psytican-bot/commit/14e10d5403e06e40a3d4c9a827af190062e855b4))

### Unknown

* Merge branch 'main' into fix-logs-and-text-refactor ([`3f7576e`](https://github.com/raider444/psytican-bot/commit/3f7576e91747492e40f7907d4d74b22fe5159a6a))

* Delete .github/workflows/semantic-release.yaml ([`150d985`](https://github.com/raider444/psytican-bot/commit/150d9855f0792e69d351e5c0fdb94890832bf133))

* Merge pull request #15 from raider444/release/123

chore(code of conduct): Add conditions ([`949f0a2`](https://github.com/raider444/psytican-bot/commit/949f0a2b2a15803476031fd64eb172a20c156655))

* Merge pull request #14 from raider444/release/123

Release/123 ([`40b7d37`](https://github.com/raider444/psytican-bot/commit/40b7d37ddaf07a2f3279761a779f0e38ddfa2d8f))

* Merge branch 'main' into cicd ([`cf115ae`](https://github.com/raider444/psytican-bot/commit/cf115ae12fc6f6324124834a624f97f09cfb3ae3))

* Merge pull request #12 from raider444/main

Update develop ([`777f5e5`](https://github.com/raider444/psytican-bot/commit/777f5e540e73ea92f75b937f5de2c202c26d59d2))

* Merge branch 'develop' into main ([`2ecd230`](https://github.com/raider444/psytican-bot/commit/2ecd230e4beb1267725439be23f692a53071f380))

* Merge pull request #10 from raider444/hotfix-regex-and-eventlist

fix(tg_wrapper): Add text description of events, fix regex ([`7ad40c7`](https://github.com/raider444/psytican-bot/commit/7ad40c7c2a6ae010c3e2274c055c53ef69dba7da))

* Merge pull request #11 from raider444/raider444-sponsorship

Create FUNDING.yml ([`8a1b25a`](https://github.com/raider444/psytican-bot/commit/8a1b25a3c96114ef294a02a9c7e060983509f0de))

* Create FUNDING.yml ([`a42093d`](https://github.com/raider444/psytican-bot/commit/a42093d8ce58a7510b759b30d0e120fc10661705))


## v0.2.3 (2024-10-01)

### Fixes

* fix(tg_wrapper): Add text description of events, fix regex
- This fixes problems with the length of inline keyboard buttons
- Fixed regex to accept capital letters in the begining of keywords ([`2f271c5`](https://github.com/raider444/psytican-bot/commit/2f271c5d9e0e451e631823c2943cf23ffc44ed3f))

### Unknown

* Merge pull request #9 from raider444/hotfix-regex-and-eventlist

Hotfix regex and eventlist ([`73ee471`](https://github.com/raider444/psytican-bot/commit/73ee471dd8d245f90be028c07200b10d42ba2c33))

* Merge pull request #7 from raider444/release-0.2.0

Release 0.2.0 ([`7f89dc2`](https://github.com/raider444/psytican-bot/commit/7f89dc27b44fbbe58e0767d240653b8b502412b1))


## v0.2.2 (2024-10-01)

### Feature

* feature(telegram): #2 Dirty implementation of acl draft ([`e4f3a5d`](https://github.com/raider444/psytican-bot/commit/e4f3a5dd195e4d38fcbc47f39d229691bdaea5d7))

### Fixes

* fix(calendar): Fix bug with month selecting ([`57f428d`](https://github.com/raider444/psytican-bot/commit/57f428dac369061f42ee5229c9ba1a94894658de))

### Unknown

* Merge pull request #8 from raider444/release-0.2.0

Release 0.2.0 ([`c95f4b8`](https://github.com/raider444/psytican-bot/commit/c95f4b862d027d8e33e4d8f89382ad2e240ebf66))

* Fix healthz endpoint and dependencies ([`2545337`](https://github.com/raider444/psytican-bot/commit/254533762d09375c7bb1671aa1f14f686bc6d33a))

* Fix helm chart ([`09fc70f`](https://github.com/raider444/psytican-bot/commit/09fc70f1c5b50ffd0075682b267bb7aeb1a98d3e))

* Merge pull request #6 from raider444/feature-chat-acl

Feature chat acl ([`e086dd5`](https://github.com/raider444/psytican-bot/commit/e086dd5e22727d5e6cb9bf73cc371b38ee6d32e8))

* Applied ACLs to telegram handlers, updated heml chart and added healthz endpoint ([`992bdee`](https://github.com/raider444/psytican-bot/commit/992bdee015d4bc36c527d69fcf6016ea53d177e7))

* Dirty implementation of ACLs ([`4dfaa17`](https://github.com/raider444/psytican-bot/commit/4dfaa17fe4168e0e6ec40dc55c1ca1b7693a714d))

* Bump version ([`7992d83`](https://github.com/raider444/psytican-bot/commit/7992d832561fa399c827b6ae2b26305043f64614))

* Small refactoring ([`df82512`](https://github.com/raider444/psytican-bot/commit/df8251267278d5a92b8b47f2c8525abf9b4c9994))

* Merge pull request #5 from raider444/fix-calendar-next-month

fix(calendar): Fix bug with month selecting ([`9719703`](https://github.com/raider444/psytican-bot/commit/97197030cfd62c3fb0c6d6b5e85f6a689a59d923))

* Merge pull request #1 from raider444/pre-commit

Added pre-commit ([`dcab44a`](https://github.com/raider444/psytican-bot/commit/dcab44ab12342ba8c95cd0feb2b3d2e4be666aea))

* Added pre-commit ([`e997fa3`](https://github.com/raider444/psytican-bot/commit/e997fa3197458b136df399810f93df7daf494fb0))

* Published for world ([`f8c6902`](https://github.com/raider444/psytican-bot/commit/f8c6902e09ddf92acd1277a199ff91e71b4f93d4))
