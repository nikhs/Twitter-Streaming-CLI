## Twitter Streaming CLI

CLI tool to generate reports based on tweets. 


### Requirements

* Twitter App credentials (create them [HERE](https://apps.twitter.com/) )
* Python 2.7 (Not compatible with Python 3)
* SQlite3
* pip

Python dependencies should be installed from the requirements file.

```shell
pip install -r requirements.txt
```

Twitter App credentials should be stored in ```tweetstream/config.php``` file.

### Usage

```shell
stream.py <track_phrases>
```
where command can be ```stream``` or ```report```

Ideally, you should redirect ouput to a file to seperate general runtime errors/warnings from output.

```shell
stream.py <track_phrases> > <output_file>
```
track_phrases should be space seperated phrases. Phrases with space should replace spaces with _

ie ```coldplay the_batman``` searches for tweets containing  *'coldplay'* OR *'the batman'*



#### Examples:
```shell
stream.py the_batman > out
```
Writes all tweets to ```out``` file.


### License

See LICENSE