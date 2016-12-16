package wiktionary

import (
	"fmt"
	"strings"

	"github.com/DexterLB/htmlparsing"
	"github.com/DexterLB/htmlparsing/parallel"
	"github.com/DexterLB/mvm/progress"
)

type WordGroup struct {
	Type  string   `json:"type"`
	Words []string `json:"words"`
	URL   string   `json:"url"`
}

func FillWordGroups(
	settings *htmlparsing.Settings,
	groups []*WordGroup,
	maxRequests int,
	progress progress.Progress,
) error {
	in := make(chan parallel.Fillable)
	go func() {
		for i := range groups {
			in <- groups[i]
		}
		close(in)
	}()

	progress.SetTotal(len(groups))

	return parallel.MapFill(in, maxRequests, progress, settings)
}

func (w *WordGroup) Fill(settings *htmlparsing.Settings) error {
	words, err := WordsOnPage(settings, w.URL)
	if err != nil {
		return err
	}
	w.Words = words
	return nil
}

func WordsOnPage(settings *htmlparsing.Settings, URL string) ([]string, error) {
	page, err := htmlparsing.NewClient(settings).ParsePage(URL, nil)
	if err != nil {
		return nil, fmt.Errorf("unable to parse page: %s", err)
	}

	links, err := page.Search(
		`//p[count(preceding-sibling::h2)>=1]/a`,
	)
	if err != nil {
		return nil, fmt.Errorf("unable to find links on page: %s", err)
	}

	words := make([]string, len(links))
	for i := range links {
		words[i] = strings.TrimSpace(links[i].Content())
		if words[i] == "" {
			return nil, fmt.Errorf("empty word :(")
		}
	}

	return words, nil
}
