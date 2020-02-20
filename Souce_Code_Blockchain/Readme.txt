1. Install bitcoin core
	1.1 Install bitcoin-0.19.0.1-win64-setup.exe (https://bitcoin.org/en/download)
	1.2 Start C:\Program Files\Bitcoin\bitcoin-qt.exe
	1.3 Click on (bitcoin-qt) Settings -> Options -> Open Configuration File , after that Close bitcoin-qt
	1.3 Set Up a Bitcoin Regtest Environment
		- Open C:\Users\LENOVO\AppData\Roaming\Bitcoin\bitcoin.conf
		- Add the following line to the configuration file, and then save:
		   
		   regtest=1
		   
	1.4 Open cmd and change to the directory 
		- C:\Program Files\Bitcoin\daemon
	1.5 Start bitcoin
		C:\Program Files\Bitcoin\daemon> bitcoind
	1.6 Open second cmd 
		- Get new (issue) bitcoin address
			C:\Program Files\Bitcoin\daemon> bitcoin-cli getnewaddress "address_name"
		- Get bitcoin (BTC)
			C:\Program Files\Bitcoin\daemon> bitcoin-cli generatetoaddress 101 "address"
		- Get balance
			C:\Program Files\Bitcoin\daemon> bitcoin-cli getbalance
		
2. Install python
	- python-3.8.1-amd64.exe (https://www.python.org/downloads/release/python-381/)
	
3. Open third cmd
	3.1 Check python version
		C:\Users\LENOVO> python --version

4. Issue credential
	4.1 Add the credential to \issue_credential\credential
	4.2 Add bitcoin issue address to issue_credential\issue_conf.json
	4.3 Create credential and manifest file
		- change to the directory '\issue_credential' and run
			\issue_credential> python createCredentialManifest.py
		- credential and manifest file will be located in 
			\issue_credential\data
	4.4 Issue credential, Run
		\issue_credential> python issueCredential.py
	4.5 Confirm the transaction
		- Go to the second cmd and run
			C:\Program Files\Bitcoin\daemon> bitcoin-cli generatetoaddress 1 "address"

5. Select credential
	5.1 Add the credential and manifest file to \select_credential\credential
	5.2 Change to the directory '\select_credential' and run
		\select_credential> python selectCredential.py
	5.3 Selected credential and manifest file will be located in 
		\select_credential\data
	
6. Verify credential
	6.1 Add the credential and manifest file to \verify_credential\data
	6.2 Change the issue bitcoin address in \verify_credential\issuer.json
	6.3 Change to the directory '\verify_credential' and run
		\verify_credential> python verifyCredential.py
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
