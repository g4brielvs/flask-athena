#!/usr/bin/env python
# -*- coding: utf-8 -*-


def test_index(app):
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_admin(app):
    with app.test_client() as client:
        response = client.get('/admin/')
        assert response.status_code == 200
