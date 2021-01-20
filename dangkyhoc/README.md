# dangkyhoc

## letmein.py

A script to help with logging in as dkmh website usually deal with high traffic just by hiding the login form.

```
python letmein.py
<RequestsCookieJar[<Cookie __RequestVerificationToken=Bx1tfbILleOSxmTmKVL7WRAn-hxweyUf44kSUtjXShMkipaWGrHnpl5ipb6RxHDGdBh-tgQnii0bqbFzscdO80AuB4s1 for />, <Cookie ASP.NET_SessionId=1r0py2151btzpvljqrmdpxky for dangkyhoc.vnu.edu.vn/>]>
```

then paste the value of `ASP.NET_SessionId` into browser's cookie editor.

## getmappings.py

A script to get `data-rowindex of all` subjects available, save to `out.txt`.

```
python getmappings.py
```

## hasclass.py

Check if any of the account in `../daotao/out.txt` has a specific class or not.

Install `alive_progress`:

```
python -m pip install alive_progress
```

Run:

```
python hasclass.py "INT1337 13"
```

## dangkyhoc.py

Continuously register for a subject. Subject code is the index from `getmappings.py`.

Directly edit the `TARGET` in the file.

```
python dangkyhoc.py
```

## concurrency_in_dkmh.go

A faster way of registering for classes, written in Go.

```
go run concurrency_in_dkmh.go <username> <password> (subjects' indexes, space separated)

Eg. go run concurrency_in_dkmh.go 18021337 testpassword 123 456 789
```

Or build it and run, mind the `$PATH` thing :v

```
go install
dangkyhoc <username> <password> (subjects' indexes, space separated)
```

## ls-la.py

List all registered subjects in accounts from `accounts.txt`. 

In `accounts.txt`:

```
username1:password1
username2:password2
username3:password3
...
```

Run:

```
python ls-la.py
```
