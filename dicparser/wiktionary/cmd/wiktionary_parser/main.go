package main

import (
	"encoding/json"
	"log"
	"os"

	"github.com/DexterLB/bookrat/dicparser/wiktionary"
	"github.com/DexterLB/htmlparsing"
	"github.com/DexterLB/mvm/progress"
)

func readDictionary(filename string) []*wiktionary.WordGroup {
	var dictionary []*wiktionary.WordGroup

	f, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	err = json.NewDecoder(f).Decode(&dictionary)
	if err != nil {
		log.Fatalf("unable to decode json: %s", err)
	}

	return dictionary
}

func writeDictionary(dictionary []*wiktionary.WordGroup, filename string) {
	f, err := os.Create(filename)
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()

	err = json.NewEncoder(f).Encode(&dictionary)
	if err != nil {
		log.Fatalf("unable to write json: %s", err)
	}
}

func main() {
	if len(os.Args) != 3 {
		log.Printf("usage: $0 <empty json dictionary> <output dictionary>")
	}

	settings := htmlparsing.SensibleSettings()

	dictionary := readDictionary(os.Args[1])

	bar := progress.NewProgressBar(1)

	err := wiktionary.FillWordGroups(settings, dictionary, 4, bar)
	if err != nil {
		log.Fatal(err)
	}

	writeDictionary(dictionary, os.Args[2])
}
