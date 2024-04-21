import scraping


def main():
    products = scraping.collect_product()
    print(products)


if __name__ == '__main__':
    main()
