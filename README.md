# immobiliare scraper 

## Introduction
This project is aimed at scraping data from the listing page of a real estate website, specifically from http://immobiliare.it/vendita-case/san-benedetto-del-tronto, which is a popular site for real estate listings. The data to be scraped includes the "trovokasa" (a specific field), listing URLs, and image URLs associated with the listings. The scraping process will be accomplished using the powerful Scrapy framework, a popular Python library for web scraping.

## Installation 
To run this project locally, you'll need to have Python and Scrapy installed on your system. If you haven't installed Scrapy before, you can do so using the following command:
```bash
pip install scrapy
```
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/your-repo.git
```

## How to Use

1. Navigate to the project directory:
```bash
cd your-repo-path 
```
2. Run the Scrapy spider:
```bash
scrapy crawl immobiliare
```
The spider will start scraping the listing page and fetch the required data, including "trovokasa," listing URLs, and image URLs. The custom image pipeline will be responsible for downloading and structuring the image URLs, inheriting from the default image pipeline provided by Scrapy.

## Custom Image Pipeline

The custom image pipeline in this project enhances the default Scrapy image pipeline to cater specifically to the needs of this project. It manages the download and storage of images associated with the listings. The custom pipeline inherits functionalities from Scrapy's default image pipeline to maintain the efficiency and robustness of the image handling process.

## License 
This project is licensed under the MIT License. You are free to use, modify, and distribute the code for both commercial and non-commercial purposes. However, kindly provide appropriate attribution to the original authors.

## Acknowledgments
We would like to express our gratitude to the Scrapy development team and the open-source community for their continuous efforts in maintaining and improving the framework. Their contributions have been invaluable to the success of this project.
