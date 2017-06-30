# mp3DirectCut #

*	 Tekijät: Abdel, Rémy, Abdellah zineddine, Jean-François COLAS
*	 Lataa [vakaa versio][1]
*	 Lataa [kehitysversio][2]

# Esittely #

Tämä lisäosa parantaa mp3DirectCut-ohjelman esteettömyyttä NVDA:n kanssa.

Toimivuus on testattu mp3DirectCutin versioilla 2.12 - 2.22.

## Pikanäppäimet ##

Tämä lisäosa tarjoaa seuraavat näppäinkomennot, joita voidaan muuttaa
valitsemalla Asetukset-valikosta Syöte-eleet ja mp3DirectCut-kategoria:

*	B
	*	Asettaa valinnan aloitusmerkin sijainnin.
*	Ctrl+Shift+B
	*	Ilmoittaa valinnan aloitusmerkin sijainnin.
	*	Kahdesti painettaessa kerrotaan valinnan kesto.
*	Ctrl+Shift+D
	*	Ilmoittaa keston tiedoston alusta toistokohdistimen nykyiseen sijaintiin saakka.
	*	Kahdesti painettaessa ilmoitetaan koko tiedoston kesto.
*	Ctrl+Shift+R
	*	Ilmoittaa jäljellä olevan ajan toistokohdistimen nykyisestä sijainnista tiedoston loppuun saakka.
*	Ctrl+Shift+N
	*	Ilmoittaa valinnan lopetusmerkin sijainnin.
	*	Antaa kahdesti painettaessa yhteenvedon valinnan aloitus- ja lopetusmerkkien sijainneista sekä ilmoittaa valinnan keston.
*	Ctrl+Shift+P
	*	Ilmoittaa nykyisen osan sekä tiedostossa olevien osien määrän.
*	Ctrl+Shift+Space
	*	Ilmoittaa VU-mittarin nykyisen tason äänityksen aikana.
	*	Kahdesti painaminen nollaa tason.
*	Nuoli alas
	*	Ilmoittaa toistokohdistimen nykyisen sijainnin.
	*	Lisäksi tämä komento siirtää kohdistimen valinnan lopetusmerkin sijaintiin ilmoittaen samalla sen, mikäli valinta on tehty .
	*	Puhuu äänenvoimakkuusvalintaikkunassa seuraavan arvon.
	*	Oletuksena tätä arvoa ei puhuta.
*	End
	*	Siirtää toistokohdistimen nykyisen tiedoston loppuun ja ilmoittaa kokonaiskeston.
*	Home
	*	Siirtää toistokohdistimen nykyisen tiedoston alkuun.
*	Left Arrow
	*	Lets make a brief return back of one second during playback, while giving the current duration.
	*	This duration is configurable in the options of mp3directcut.
*	N
	*	Used to confirm correct placement of the marker of the end of the selection N.
*	Page Down
	*	Lets make a leap forward of 10 seconds during playback, while giving the current duration.
	*	This duration is configurable in the options of mp3directcut.
*	Page Up
	*	Lets make a return back of 10 seconds during playback, while giving the current duration.
	*	This duration is configurable in the options of mp3directcut.
*	R
	*	Allows to prepare a record and whether you can press spacebar to start.
*	Right Arrow
	*	Lets do a brief forward of one second during playback, while giving the current duration.
	*	This duration is configurable in the options of mp3directcut.
*	Ctrl+Right Arrow
	*	Moves to the next splitting point, while giving the current duration.
*	Ctrl+Left Arrow
	*	Moves to the previous splitting point, while giving the current duration.
*	Shift+Right Arrow
	*	Lets do a brief forward of four hundredths of seconds during playback, while giving the current duration.
*	Shift+Left Arrow
	*	Lets do a brief backwards of four hundredths of seconds during playback, while giving the current duration. 
*	S
	*	Used to stop the reading and give the current duration.
*	Space
	*	If the recording is ready, start this recording.
	*	If a recording is in progress, stop it by positioning the cursor at the beginning.
	*	If a file is loaded, start the reading.
	*	If a read is in progress, allows to do a pause by giving current duration.
	*	If read is paused, allows to restart the reading from the current location.
*	Nuoli ylös
	*	Puhuu toistokohdistimen nykyisen sijainnin.
	*	Lisäksi, mikäli valinta on tehty,  tämä komento siirtää kohdistimen valinnan aloitusmerkin kohdalle ja puhuu sen sijainnin.
	*	In the volume dialog box, vocalise the previous value that can be reached generally with upArrow.
	*	Tätä ei puhuta oletuksena.
*	NVDA+H
	*	Avaa lisäosan ohjeen.

## Muutokset versiossa 2.2 ##

*     Valitun alueen  merkkien sijainnit ilmoittavat skriptit korjattu.

## Muutokset versiossa 2.1.1 ##

*	 Kokonaisajan ilmoittava skripti poistettu ja lisätty sen antamat tiedot
   jäljellä olevan ajan ilmoitukseen;
*	 Lisäosan asetuksiin lisätty mahdollisuus muista ilmoituksista erillisten
   välilyöntinäppäimeen liittyvien ilmoitusten käyttöön ottamiseen tai
   käytöstä poistamiseen;
*	 Lisäosan asetuksiin lisätty mahdollisuus valintamerkkien
   sijainti-ilmoituksen käyttöön ottamiseen tai käytöstä poistamiseen;
*	 Lisätty mahdollisuus nykyisen sijainnin ilmoittamiseen leikkauskohtien
   välillä liikuttaessa;
*	 Korjattu nuoli ylös- ja nuoli alas -näppäimiin liittyvät ilmoitukset;
*	 Lisätty skripti lisäosaohjeen avaamiseen näppäinkomennolla NVDA+H;
*	 Siirretty lisäosan asetusvalintaikkuna Työkalut-valikosta
   Asetukset-valikkoon.

## Muutokset versiossa 2.1 ##

*	 Lisätty skripti, joka puhuu seuraavan leikkauskohdan siirryttäessä siihen
   näppäinkomennolla Control+Nuoli oikealle;
*	 Lisätty skripti, joka puhuu edellisen leikkauskohdan siirryttäessä siihen
   näppäinkomennolla Control+Nuoli vasemmalle;
*	 Lisätty skripti, joka puhuu siirryttäessä neljä sekunnin sadasosaa
   eteenpäin näppäinkomennolla Shift+Nuoli oikealle;
*	 Lisätty skripti, joka puhuu siirryttäessä neljä sekunnin sadasosaa
   taaksepäin näppäinkomennolla Shift+Nuoli vasemmalle;
*	 Korjattu lisäosan yhteenvedoksi "mp3DirectCut".

## Muutokset versiossa 2.0 ##

*	 Lisätty jäljellä olevan ajan ilmoittava komento Control+Shift+R;
*	 Korjattu keston, tunnit mukaan lukien, lukeminen;
*	 Lisätty mahdollisuus sekunnin tuhannes- ja sadasosien erottamiseen
   toisistaan.

## Muutokset versiossa 1.1 ##

*	 Syöte-eleet-valintaikkunaan lisätty mp3DirectCut-kategoria;
	*	 sen sisältämät komennot ovat näkyvissä vain ohjelman ollessa käynnissä.
*	 Lisätty mahdollisuus automaattisten ilmoitusten käyttöön ottamiseen tai käytöstä poistamiseen NVDA:n Työkalut-valikon mp3DirectCut-kohteeseen;

## Muutokset versiossa 1.0 ##

*	 Ensimmäinen versio.

[[!tag dev stable]]

[1]: https://addons.nvda-project.org/files/get.php?file=mp3dc

[2]: https://addons.nvda-project.org/files/get.php?file=mp3dc-dev