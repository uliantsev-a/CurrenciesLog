import os
from datetime import datetime, timedelta

import asyncio
import aiohttp
from aiohttp import ClientSession

from sqlalchemy import exc
from logging.handlers import RotatingFileHandler

from project import db, app
from project.models.trades import Currency, Rate


LOAD_PERIOD_BY_DAYS = 10
MS_TO_MICROSEC = 1000
TIME_FRAME = '1D'

URL_API_ROOT = 'https://api-pub.bitfinex.com/v2/'
URL_HIST_TO_USD = URL_API_ROOT + 'candles/trade:{time_frame}:t{currencies}USD/hist'

log_path = app.config['LOGFILE_LOADER']
if not os.path.exists(log_path):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    f = open(log_path, 'a+')
    f.close()

handler = RotatingFileHandler(log_path, maxBytes=1000000, backupCount=1)
app.logger.addHandler(handler)


async def request_api(url: str, session: ClientSession, **kwargs) -> list:
    """GET request wrapper to fetch data the API response.

    kwargs are passed to `session.request()`.
    """

    method = kwargs.pop('method', 'GET')
    resp = await session.request(method=method, url=url, **kwargs)
    resp.raise_for_status()
    app.logger.info("Got response [%s] for URL: %s", resp.status, url)
    data = await resp.json()
    return data


async def get_hist(url: str, session: ClientSession, **kwargs) -> set:
    """Getting history from API with possible processing."""
    resp = set()
    try:
        today = datetime.now().replace(hour=0, second=0, microsecond=0)
        start_ms = int((today - timedelta(days=LOAD_PERIOD_BY_DAYS)).timestamp() * MS_TO_MICROSEC)
        params = {'start': start_ms}
        resp = await request_api(url=url, session=session, params=params, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
        app.logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return resp
    except Exception as e:
        app.logger.exception("Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {}))
        return resp
    else:
        # Possible post processing  and return response data
        return resp


async def load_one_to_usd(currency: object, session=ClientSession) -> None:
    """Load with saving rates by USD to a currency unit."""

    url = URL_HIST_TO_USD.format(time_frame=TIME_FRAME, currencies=currency.name)
    res = await get_hist(url=url, session=session)
    if not res:
        return None

    saving_response_rates(currency, res)


def saving_response_rates(currency: object, rates: list) -> None:
    """Saving response data to DB."""

    bulk_rates = list()
    for item in rates:
        rate_params = {
            'currency_id': currency.id,
            'date': datetime.fromtimestamp(item[0] / MS_TO_MICROSEC).date(),
            'rate': item[3],
            'volume': item[5],
        }
        rate = Rate(**rate_params)
        bulk_rates.append(rate)

    try:
        db.session.bulk_save_objects(bulk_rates)
    except exc.IntegrityError:
        db.session.rollback()
        # Second trying without dates which we have

        new_rate_dates = [rate.date for rate in bulk_rates]
        current_rates = Rate.query.join(Currency.rates).filter(
            Currency.id == currency.id,
            Rate.date.in_(new_rate_dates)
        ).all()

        current_collision_dates = tuple(item.date for item in current_rates)
        bulk_rates = [item for item in bulk_rates if item.date not in current_collision_dates]

        db.session.bulk_save_objects(bulk_rates)

        app.logger.warning(f'By saving did have some collision for {currency.name}')
    else:
        app.logger.info(f'Rates was save for {currency.name}')
    finally:
        db.session.commit()


async def main_crawl_and_save():
    """Crawl & write concurrently to DB for multiple currencies."""

    async with ClientSession() as session:
        tasks = []
        currencies = Currency.query.all()
        for curr in currencies:
            tasks.append(
                load_one_to_usd(currency=curr, session=session)
            )
        await asyncio.gather(*tasks)


def run_load_currencies():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_crawl_and_save())
    finally:
        loop.close()


if __name__ == "__main__":
    run_load_currencies()
