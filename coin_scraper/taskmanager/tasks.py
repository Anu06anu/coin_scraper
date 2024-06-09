from celery import shared_task
from .models import Job, Task
from .coinmarketcap import CoinMarketCap

@shared_task
def scrape_coin_data(job_id, coin):
    coin_scraper = CoinMarketCap(coin)
    data = coin_scraper.scrape()
    job = Job.objects.get(job_id=job_id)
    Task.objects.create(job=job, coin=coin, output=data)
