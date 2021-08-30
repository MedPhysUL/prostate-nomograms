import logging


def logs_file_setup(file: str, level=logging.INFO):
    import os
    import sys
    import time
    from datetime import date

    today = date.today()
    timestamp = str(time.time()).replace('.', '')
    logs_dir = f"logs/logs-{today.strftime('%d-%m-%Y')}"
    logs_file = f'{logs_dir}/{os.path.splitext(os.path.basename(file))[0]}-{timestamp}.log'
    os.makedirs(logs_dir, exist_ok=True)
    logging.basicConfig(filename=logs_file, filemode='w+', level=level, format='%(message)s')
    sh = logging.StreamHandler(sys.stdout)

    if logging.getLogger().hasHandlers():
        logging.getLogger().handlers.clear()

    logging.getLogger().addHandler(sh)


def section_title_log(section_title: str):
    logging.info("% " + "-"*107 + " %")
    logging.info("% " + " " * 35 + section_title + " " * 35)
    logging.info("% " + "-"*107 + " %")


def sub_section_title_log(sub_section_title: str):
    logging.info("\n" + "% " + "-"*8 + f" {sub_section_title} " + "-"*8 + " %" + "\n")


if __name__ == '__main__':
    logs_file_setup(__file__, logging.DEBUG)
