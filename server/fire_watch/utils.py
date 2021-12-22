import fire_watch


def pagination_utils(page, page_limit):
    if isinstance(page_limit, dict):
        page_limit = (
            page_limit["debug"]
            if fire_watch.flags.in_debug
            else page_limit["production"]
        )
    page = 1 if (page == 0 or page < 0) else page
    skip = (page * page_limit) - page_limit
    return skip, page_limit
