#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from app import create_app

@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app
