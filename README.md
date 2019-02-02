# library2osm
Import Norwegian libraries to OSM

Usage: <code>python library2osm > output_filename.osm</code>

### Notes ###

* Extracts Norwegian libraries from BaseBibliotek and produces an OSM file
* Libraries are identified with their [ref:isil](https://wiki.openstreetmap.org/wiki/Key:ref:isil) number
* Library types are explained [here](http://www.biblev.no/biblioteknummer.html)
* Public libraries ("folkebibliotek") are tagged with *access=yes**
* The National Library of Norway has requested email adresses not to be imported into OSM to avoid spamming
* Many libraries have no coordinates. They may be geocoded using [geocode2osm](https://github.com/osmno/geocode2osm)
* An OSM file with all public libraries has been stored [here](https://drive.google.com/drive/folders/1nhxjciiwOOIWmTlmXsQp-4WoYwZlsGZ6?usp=sharing)


### References ###

* [BaseBibliotek](https://bibliotekutvikling.no/ressurser/tjenester-fra-nasjonalbiblioteket-til-bibliotekene/basebibliotek/)
* [Library types](http://www.biblev.no/biblioteknummer.html)
* [Export feed](https://www.nb.no/baser/bibliotek/eksport/bb-full.xml) (updated Monday-Friday at 9pm)
* [Example REST service](https://www.nb.no/BaseBibliotekSearch/rest/bibnr/NO-0030100)
