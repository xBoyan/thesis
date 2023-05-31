from scraper import DBScrapper

db_scrapper = DBScrapper(csv_file_path="C:\\Users\\Adam\\thesis\\dataset\\products.csv", force_skip=True)
db_scrapper.scrap()
