package dicparser

import (
	"bytes"
	"fmt"
	"io"
	"strings"
	"sync"

	"github.com/DexterLB/htmlparsing"
	"github.com/DexterLB/mvm/progress"
	"golang.org/x/text/encoding/charmap"
)

func GetInfo(
	settings *htmlparsing.Settings,
	words []string,
	out io.Writer,
	maxRequests int,
	progress progress.Progress,
) error {
	progress.SetTotal(len(words))
	defer progress.Done()

	parallelRequests := sync.WaitGroup{}
	parallelRequests.Add(maxRequests)

	in := make(chan string)
	errors := make(chan error)
	target := newConcurrentWriter(out, errors)

	go func() {
		for i := range words {
			in <- words[i]
		}
		close(in)
	}()

	go func() {
		parallelRequests.Wait()
		target.Done()
		close(errors)
	}()

	for i := 0; i < maxRequests; i++ {
		go func() {
			getSomeInfo(settings, in, target, progress, errors)
			parallelRequests.Done()
		}()
	}

	return formatErrors(errors)
}

func getSomeInfo(
	settings *htmlparsing.Settings,
	in <-chan string,
	target io.Writer,
	progress progress.Progress,
	errors chan<- error,
) {
	maxSize := 10000
	encoder := charmap.Windows1251.NewEncoder()

	buf := bytes.NewBuffer(make([]byte, 0, maxSize))
	wordsIn := 0

	for word := range in {
		data, err := encoder.Bytes([]byte(word))
		if err != nil {
			errors <- fmt.Errorf("unable to encode word `%s`: %s", word, err)
			progress.Add(1)
			continue
		}

		if buf.Len()+len(data) >= maxSize {
			writeWordInfo(settings, buf.Bytes(), target, errors)
			progress.Add(wordsIn)
			wordsIn = 0
			buf.Truncate(0)
		}

		wordsIn += 1
		buf.Write(data)
		buf.Write([]byte(" "))
	}

	if buf.Len() > 0 {
		writeWordInfo(settings, buf.Bytes(), target, errors)
		progress.Add(wordsIn)
	}
}

func writeWordInfo(
	settings *htmlparsing.Settings,
	words []byte,
	target io.Writer,
	errors chan<- error,
) {
	info, err := getInfoForWordList(settings, string(words))
	if err != nil {
		errors <- fmt.Errorf(
			"unable to get info for words `%s`: %s",
			string(words), err,
		)
		return
	}

	fmt.Fprintf(target, "\n%s\n", info)
}

func getInfoForWordList(
	settings *htmlparsing.Settings, words string,
) (string, error) {
	page, err := htmlparsing.NewClient(settings).ParsePage(
		`http://slovored.com/search/grammar`,
		htmlparsing.URLValues(
			map[string]string{
				"word": words,
			},
		),
	)
	if err != nil {
		return "", fmt.Errorf("unable to open word info page: %s", err)
	}

	dataElement, err := htmlparsing.First(page, `//pre`)
	if err != nil {
		return "", fmt.Errorf("unable to find data on info page: %s", err)
	}

	return dataElement.Content(), nil
}

func encode(data string) (string, error) {
	encoder := charmap.Windows1251.NewEncoder()
	return encoder.String(data)
}

func formatErrors(errors <-chan error) error {
	var messages []string
	for err := range errors {
		messages = append(messages, fmt.Sprintf("  > %s\n", err))
	}

	if len(messages) == 0 {
		return nil
	}

	return fmt.Errorf(
		"the following errors were encountered:\n%s",
		strings.Join(messages, ""),
	)
}
