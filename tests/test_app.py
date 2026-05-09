import pytest
import time
from app import mock_packages

def test_track_valid_en_reparto(client):
    response = client.get('/api/track/TRK12345')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['status'] == 'En reparto'

def test_track_valid_entregado(client):
    response = client.get('/api/track/TRK11111')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['status'] == 'Entregado'

def test_track_valid_en_transito(client):
    response = client.get('/api/track/TRK98765')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['status'] == 'En tránsito'

def test_track_not_found(client):
    response = client.get('/api/track/TRKINVALID')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == 'Número de guía no encontrado.'

def test_track_lowercase(client):
    response_lower = client.get('/api/track/trk12345')
    response_upper = client.get('/api/track/TRK12345')
    assert response_lower.status_code == 200
    assert response_lower.get_json() == response_upper.get_json()

def test_track_whitespace(client):
    response_space = client.get('/api/track/ TRK12345 ')
    response_normal = client.get('/api/track/TRK12345')
    assert response_space.status_code == 200
    assert response_space.get_json() == response_normal.get_json()

def test_track_invalid_format(client):
    response = client.get('/api/track/INV@L!D')
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == 'Formato de número de guía inválido.'

def test_track_response_structure(client):
    response = client.get('/api/track/TRK12345')
    data = response.get_json()
    assert 'success' in data
    assert 'data' in data
    assert 'status' in data['data']
    assert 'origin' in data['data']
    assert 'destination' in data['data']
    assert 'estimatedDelivery' in data['data']
    assert 'events' in data['data']

def test_track_events_ordered(client):
    response = client.get('/api/track/TRK12345')
    events = response.get_json()['data']['events']
    
    # Assuming dates are in format 'YYYY-MM-DD HH:MM' and sorted from newest to oldest
    for i in range(len(events) - 1):
        assert events[i]['date'] >= events[i+1]['date']

def test_track_has_origin_destination(client):
    response = client.get('/api/track/TRK12345')
    data = response.get_json()['data']
    assert data['origin'] == 'Bogotá, COL'
    assert data['destination'] == 'Medellín, COL'
    assert data['estimatedDelivery'] == '2026-05-03'

def test_track_valid_statuses(client):
    valid_statuses = ['En tránsito', 'En reparto', 'Entregado']
    for tracking_number, package in mock_packages.items():
        assert package['status'] in valid_statuses

def test_track_min_events(client):
    for tracking_number, package in mock_packages.items():
        assert len(package['events']) >= 3

def test_index_returns_html(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data

def test_api_response_time(client):
    start_time = time.time()
    response = client.get('/api/track/TRK12345')
    end_time = time.time()
    assert response.status_code == 200
    assert (end_time - start_time) < 2.0
