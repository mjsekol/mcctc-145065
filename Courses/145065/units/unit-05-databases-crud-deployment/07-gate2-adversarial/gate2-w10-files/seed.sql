-- seed.sql · invented starting data. Riverside Fabrication is a composite.
-- WR-01 is a spare weld robot with no Line 3 downtime yet. It must show 0 events.

INSERT INTO equipment (code, name) VALUES
    ('PB-02', 'Press Brake 2'),
    ('LC-01', 'Fiber Laser Cutter'),
    ('CV-01', 'Transfer Conveyor'),
    ('WR-01', 'Weld Robot');

INSERT INTO downtime_events (equipment_id, line, reason, minutes, resolved, occurred_at) VALUES
    (1, 3, 'Back gauge lost its home position', 40, 1, '2025-11-10T08:20:00Z'),
    (2, 3, 'Assist gas pressure dropped mid cut', 25, 1, '2025-11-10T13:05:00Z'),
    (3, 3, 'Belt tracking off, guard trip', 90, 0, '2025-11-11T09:40:00Z'),
    (1, 3, 'Hydraulic filter clogged', 35, 1, '2025-11-11T15:10:00Z'),
    (3, 3, 'Drive coupling replaced', 120, 1, '2025-11-12T07:30:00Z'),
    (2, 4, 'Line 4 laser optics cleaned', 15, 1, '2025-11-12T10:00:00Z');
