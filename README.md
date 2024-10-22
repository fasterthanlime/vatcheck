# vatcheck

I recently created a new company and the French tax authority assigned me
a tax number. Unfortunately it's not in some database yet, which means
if I try to use it on a European provider like Hetzner, it'll reject my VAT
number.

So I made (with a little help from GPT-4o/Claude 3.5 Sonnet) a Telegram bot
to send me a message when the VAT number finally becomes valid.

![](images/screenie.webp)

I check that using the [VIES API](https://ec.europa.eu/taxation_customs/vies/#/vat-validation)
provided by the European Commission.

Unfortunately you'll need to deploy the bot yourself if you want to run it,
I'm not running it as a general-purpose but right now.

It's fun though!
