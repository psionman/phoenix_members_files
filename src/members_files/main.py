"""Main module for Phoenix Members Files."""
import sys

from root import Root

from psiutils.icecream_init import ic_init
ic_init()


def main():
    Root()

    # Temp code to test data
    # from temp import Parent
    # from process import compare

    # compare(Parent())
    # end temp


if __name__ == '__main__':
    main()
