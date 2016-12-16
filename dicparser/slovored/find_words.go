package dicparser

import (
	"fmt"
	"regexp"
	"strings"

	"github.com/DexterLB/htmlparsing"
	"github.com/DexterLB/htmlparsing/parallel"
	"github.com/DexterLB/mvm/progress"
)

func StripURLs(URLs []string) []string {
	matcher := regexp.MustCompile(
		`[^/]*$`,
	)

	strippedURLs := make([]string, len(URLs))
	for i := range URLs {
		strippedURLs[i] = matcher.FindString(URLs[i])
	}

	return strippedURLs
}

func LinksOnPages(
	settings *htmlparsing.Settings,
	URLs []string,
	root string,
	maxRequests int,
	progress progress.Progress,
) ([]string, error) {
	pages := make([]*pageWithLinks, len(URLs))
	for i := range URLs {
		pages[i] = &pageWithLinks{URL: URLs[i], Root: root}
	}

	pageIn := make(chan parallel.Fillable)
	go func() {
		for i := range pages {
			pageIn <- pages[i]
		}
		close(pageIn)
	}()

	progress.SetTotal(len(pages))

	err := parallel.MapFill(pageIn, maxRequests, progress, settings)
	if err != nil {
		return nil, fmt.Errorf("unable to get links on pages: %s", err)
	}

	var links []string
	for i := range pages {
		links = append(links, pages[i].Links...)
	}

	return links, nil
}

type pageWithLinks struct {
	URL   string
	Links []string
	Root  string
}

func (p *pageWithLinks) Fill(settings *htmlparsing.Settings) error {
	links, err := GetLinks(settings, p.URL, p.Root)
	if err != nil {
		return err
	}

	p.Links = links
	return nil
}

func GetLinks(
	settings *htmlparsing.Settings,
	pageURL string,
	root string,
) ([]string, error) {
	page, err := htmlparsing.NewClient(settings).ParsePage(pageURL, nil)
	if err != nil {
		return nil, fmt.Errorf("unable to parse page: %s", err)
	}

	links, err := page.Search(
		`//div[contains(@class, 'links') or contains(@class, 'words')]/a`,
	)
	if err != nil {
		return nil, fmt.Errorf("unable to find links on page: %s", err)
	}

	URLs := make([]string, len(links))
	for i := range links {
		url, ok := links[i].Attributes()["href"]
		if !ok {
			return nil, fmt.Errorf("link has no href attribute!")
		}
		URLs[i] = setRoot(url.Value(), root)
	}

	return URLs, nil
}

func setRoot(url, root string) string {
	if strings.Contains(url, `//`) {
		return url
	}

	if url[0] == '/' {
		return fmt.Sprintf("%s%s", root, url)
	}

	return fmt.Sprintf("%s/%s", root, url)
}
