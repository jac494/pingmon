#!/usr/bin/env python3

import datetime
import logging
import sys
import time
from types import SimpleNamespace

import click
import icmplib

CONFIG = SimpleNamespace(
    LOGGING=SimpleNamespace(
        FORMAT="%(asctime)s %(levelname)s:%(message)s",
        LEVEL=logging.DEBUG,
        LOGFILE_TEMPLATE="logs/pingmon.{datestamp}.{monitor_host}.log",
        ENCODING="utf-8",
    ),
    WAIT_SECONDS=1.0,
    ICMPLIB_PING=SimpleNamespace(
        INTERVAL=1,
        COUNT=20,
        TIMEOUT=1,
    ),
)

RESULT_STR_TEMPLATE = " ".join(
    (
        "host={result.address}",
        "packets_sent={result.packets_sent}",
        "packets_received={result.packets_received}",
        "packet_loss={result.packet_loss}",
        "avg_rtt={result.avg_rtt}",
        "jitter={result.jitter}",
        "min_rtt={result.min_rtt}",
        "max_rtt={result.max_rtt}"
    )
)

def iso8601_datetime(datestamp=None):
    now = datestamp or datetime.datetime.now()
    return (
        f"{now.year}{str(now.month).zfill(2)}{str(now.day).zfill(2)}"
        f"{str(now.hour).zfill(2)}{str(now.minute).zfill(2)}"
    )


@click.command()
@click.argument("monitor_host")
def main(monitor_host):
    click.echo(f"Starting monitor for {monitor_host}")
    logging.basicConfig(
        format=CONFIG.LOGGING.FORMAT,
        level=CONFIG.LOGGING.LEVEL,
        filename=CONFIG.LOGGING.LOGFILE_TEMPLATE.format(
            datestamp=iso8601_datetime(), monitor_host=monitor_host
        ),
        encoding=CONFIG.LOGGING.ENCODING,
    )
    results = []
    while True:
        try:
            start = time.time()
            result = ping_host(monitor_host)
            results.append(result)
            end = time.time()
            sleep_time = CONFIG.WAIT_SECONDS - (end - start)
            logging.debug(f"{sleep_time=}")
            if sleep_time > 0:
                time.sleep(sleep_time)
        except KeyboardInterrupt:
            logging.info(
                "received keyboardinterrupt; processing results and exiting..."
            )
            click.echo("Received keyboard interrupt")
            sys.exit(0)


def ping_host(host):
    logging.info(f"sending {CONFIG.ICMPLIB_PING.COUNT} ICMP echo request(s) to {host=}")
    result = icmplib.ping(address=host, interval=CONFIG.ICMPLIB_PING.INTERVAL, count=CONFIG.ICMPLIB_PING.COUNT, timeout=CONFIG.ICMPLIB_PING.TIMEOUT, privileged=False)
    logging.info(RESULT_STR_TEMPLATE.format(result=result))


if __name__ == "__main__":
    main()
