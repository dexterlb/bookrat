package dicparser

import "io"

type concurrentWriter struct {
	writer io.Writer
	in     chan []byte
	done   chan struct{}
	errors chan<- error
}

func newConcurrentWriter(writer io.Writer, errors chan<- error) *concurrentWriter {
	c := &concurrentWriter{
		writer: writer,
		errors: errors,
		in:     make(chan []byte),
		done:   make(chan struct{}),
	}

	go func() {
		for data := range c.in {
			_, err := c.writer.Write(data)
			if err != nil {
				errors <- err
			}
		}
		close(c.done)
	}()
	return c
}

func (c *concurrentWriter) Write(data []byte) (int, error) {
	c.in <- data
	return len(data), nil
}

func (c *concurrentWriter) Done() {
	close(c.in)
	<-c.done
}
