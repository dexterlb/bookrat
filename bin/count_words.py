from ..lib import counting_worker
from ..lib import megatron

def main():
	m = megatron.Megatron("postgres://do@localhost/book-rat-test")
	counting_worker.run(m)

if __name__ == '__main__':
	main()