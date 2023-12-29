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
    # current config is set to send 60 icmp echo requests ideally within a
    # 60-second window. if they all come back quickly (less than 1 second each)
    # then it will likely take less than 60s, so wait for the remainder of
    # that minute.
    # this is kinda bad because loss could happen in the time that the monitor
    # is sleeping rather than spacing all pings out throughout the 60s window
    # which would see the loss throughout any portion of that timeframe
    # maybe do less here and allow a monitoring system (like prometheus)
    # to make aggreegation and rollup decisions and just send a ping once per second
    # or something and report the values
    WAIT_SECONDS=60.0,
    ICMPLIB_PING=SimpleNamespace(
        INTERVAL=1,
        COUNT=60,
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
        "max_rtt={result.max_rtt}",
    )
)


def iso8601_datetime(datestamp=None):
    now = datestamp or datetime.datetime.now()
    return (
        f"{now.year}"
        f"{str(now.month).zfill(2)}"
        f"{str(now.day).zfill(2)}"
        f"{str(now.hour).zfill(2)}"
        f"{str(now.minute).zfill(2)}"
        f"{str(now.second).zfill(2)}"
    )


def ping_host(host):
    logging.info(f"sending {CONFIG.ICMPLIB_PING.COUNT} ICMP echo request(s) to {host=}")
    start_time = iso8601_datetime()
    result = icmplib.ping(
        address=host,
        interval=CONFIG.ICMPLIB_PING.INTERVAL,
        count=CONFIG.ICMPLIB_PING.COUNT,
        timeout=CONFIG.ICMPLIB_PING.TIMEOUT,
        privileged=False,
    )
    end_time = iso8601_datetime()
    logging_str = (
        f"{start_time=} {end_time=} {RESULT_STR_TEMPLATE.format(result=result)}"
    )
    logging.info(logging_str)


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
    while True:
        try:
            start = time.time()
            ping_host(monitor_host)
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


if __name__ == "__main__":
    main()
