package main

import (
	"io"
	"log"
	"os"

	"github.com/DexterLB/bookrat/dicparser/slovored"
	"github.com/DexterLB/htmlparsing"
	"github.com/DexterLB/mvm/progress"
)

func getLinks(message string, pages []string) []string {
	settings := htmlparsing.SensibleSettings()
	settings.Encoding = []byte("cp1251")

	bar := progress.StartProgressBar(1, message)
	links, err := dicparser.LinksOnPages(
		settings,
		pages,
		`http://slovored.com`,
		2,
		bar,
	)
	if err != nil {
		log.Fatalf("unable to get two-letter links: %s", err)
	}

	return links
}

func getWords() []string {
	letterLinks := getLinks(
		"getting letter links    ",
		[]string{`http://slovored.com/sitemap/grammar`},
	)

	twoLetterLinks := getLinks(
		"getting two-letter links",
		letterLinks,
	)

	wordLinks := getLinks(
		"getting word links      ",
		twoLetterLinks,
	)

	return dicparser.StripURLs(wordLinks)
}

func getInfo(words []string, target io.Writer) {
	settings := htmlparsing.SensibleSettings()
	settings.Encoding = []byte("cp1251")

	bar := progress.StartProgressBar(1, "getting info for words")

	err := dicparser.GetInfo(settings, words, target, 4, bar)
	if err != nil {
		log.Fatalf("error getting info: %s", err)
	}
}

func main() {
	out, err := os.Create("/tmp/word_info")
	if err != nil {
		log.Fatalf("unable to open file: %s", err)
	}
	defer out.Close()

	getInfo(getWords(), out)
}
