## Twitter Streaming CLI

CLI tool to stream tweets or generate reports based on them. Supports tracking particular phrases.

Generated reports based on all tweets to ```out``` file.


### Requirements

* Twitter App credentials (create them [HERE](https://apps.twitter.com/) )
* Python 2.7 (Not compatible with Python 3)
* SQlite3
* pip

Python dependencies should be installed from the requirements file.

```shell
pip install -r requirements.txt
```

Twitter App credentials should be stored in ```tweetstream/config.py``` file.

### Usage

```shell
twitter.py <command> [<track_phrases>]
```
where command can be ```stream``` or ```report```

Ideally, you should redirect ouput to a file to seperate general runtime errors/warnings from output.

```shell
twitter.py <command> [<track_phrases>] > <output_file>
```
track_phrases should be space seperated phrases. Phrases with space should replace spaces with _

ie ```coldplay the_batman``` searches for tweets containing  *'coldplay'* OR *'the batman'*



#### Examples:
```shell
twitter.py stream > out
```
Writes all tweets to ```out``` file.

```shell
twitter.py report coldplay the_batman > out
```
Generated reports based on tweets containing to *'coldplay'* OR *'the batman'* to ```out``` file.

```shell
twitter.py report > out
```


### License

See LICENSE