# PyChromium

###*Short Important Note*
There is no point for abstract classes to be present in the script at the current state. I was planning to include **Linux** at some point but haven't had the time yet. Please ignore this small issue.

Thank you!

--

###*Description*
***PyChromium*** allows the user to extract login data from the login database used by chromium ( **Google Chrome** ) in *three* simple steps.

--

###*Options*
Switch | Action | Description
--- | --- | ---
--action | check | Checks whether the chromium login database contains any data.
--action | retrieve | Attempts to copy over the chromium login database to the scripts temp folder.
--action | harvest | Extracts and decrypts any login data that resides inside the chromium login database.

--

###*Usage*
Use ***PyChromium*** in the following order;
```
$ PyChromium.py --action=check
$ PyChromium.py --action=retrieve
$ PyChromium.py --action=harvest
```

--

###*Example Output*
####--action=check
```
$ PyChromium ( Version 0.1 Build 11102016 )

$ [+] Verifying Chromium Database...
$ [+] Connecting To Database...
$ [+] Executing Query...
$ [+] Fetching Data From Table...

$ [!] Total of 1 record(s) found!
```

####--action=retrieve
```
$ PyChromium ( Version 0.1 Build 11102016 )

$ [+] Verifying Chromium Database...
$ [+] Generating UUID...
$ [+] Copying Database To 'F:\Python\Chromium\temp\' As '9af21828bf3451c79b693cab2f6cac35'

$ [!] Database Successfully Copied!
```

####--action=harvest
```
$ PyChromium ( Version 0.1 Build 11102016 )

$ [+] Parsing File '9af21828bf3451c79b693cab2f6cac35'
$ [+] Connecting To '9af21828bf3451c79b693cab2f6cac35'
$ [+] Executing Query...
$ [+] Fetching Data From Table
$   [!] Decrypting -$ 'Fafnir' @ 'http://www.spelpunt.nl/login.php'
$ [+] Creating Output File '9af21828bf3451c79b693cab2f6cac35' @ 'F:\Python\Chromium\storage\'
$ [+] Writing To Output File '9af21828bf3451c79b693cab2f6cac35'

$ [!] Database '9af21828bf3451c79b693cab2f6cac35' Harvested! :-)
```

--
