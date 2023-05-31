from scraper import DBScrapper

db_scrapper = DBScrapper(csv_file_path="D:\\Github\\thesis\\dataset\\products.csv", force_skip=False, workers=10)
db_scrapper.scrap()
