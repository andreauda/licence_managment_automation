from .database import extract_data_from_postgres

from .selenium_portal import (
    setup_driver,
    accept_cookies,
    login,
    download_exported_data,
    search_for_email,
    extract_license_key,
    unassign_key
)

from .utils import join_downloaded_with_input