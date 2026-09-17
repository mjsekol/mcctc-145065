-- seed.sql · Line 3 Maintenance Log · the starting data, as a SQL script
--
-- Riverside Fabrication is a composite. Every name and record here is invented.
--
-- No row gives its own id. The database assigns ids, and each foreign key is
-- looked up by a natural key (a badge, a machine code, an issue title). That
-- keeps this file identical for SQLite and PostgreSQL.

INSERT INTO technicians (badge, display_name, role) VALUES
    ('T-1041', 'Dana Okafor', 'technician'),
    ('T-1057', 'Luis Brennan', 'technician'),
    ('T-1062', 'Priya Castellano', 'technician'),
    ('S-2003', 'Morgan Healey', 'supervisor');

INSERT INTO equipment (code, name, cell, kind) VALUES
    ('PB-01', 'Press Brake 1', 'Forming', 'press'),
    ('PB-02', 'Press Brake 2', 'Forming', 'press'),
    ('LC-01', 'Fiber Laser Cutter', 'Cutting', 'cutter'),
    ('CV-01', 'Transfer Conveyor', 'Transfer', 'conveyor'),
    ('WR-01', 'Weld Robot', 'Welding', 'robot'),
    ('OV-01', 'Powder Coat Cure Oven', 'Finishing', 'oven');

INSERT INTO issues (equipment_id, reported_by, title, description, severity, status,
                    downtime_minutes, locked_out, reported_at, closed_at) VALUES
    ((SELECT id FROM equipment WHERE code = 'PB-01'),
     (SELECT id FROM technicians WHERE badge = 'T-1041'),
     'Back gauge drifts 2 mm after warm-up',
     'Parts from the second hour measure long. Re-zeroing the back gauge fixes it for about forty minutes.',
     'medium', 'open', 25, 0, '2025-11-10T07:42:00Z', NULL),
    ((SELECT id FROM equipment WHERE code = 'OV-01'),
     (SELECT id FROM technicians WHERE badge = 'T-1057'),
     'Zone 2 heater slow to reach setpoint',
     'Zone 2 takes 35 minutes to reach 200 C. Zone 1 takes 20. Cure times on the first rack were extended.',
     'high', 'in_progress', 60, 0, '2025-11-10T08:15:00Z', NULL),
    ((SELECT id FROM equipment WHERE code = 'CV-01'),
     (SELECT id FROM technicians WHERE badge = 'T-1062'),
     'Guard interlock trips with the guard closed',
     'The conveyor stops every few minutes and shows a guard-open fault. The guard is closed and latched.',
     'critical', 'open', 90, 1, '2025-11-10T09:03:00Z', NULL),
    ((SELECT id FROM equipment WHERE code = 'LC-01'),
     (SELECT id FROM technicians WHERE badge = 'T-1041'),
     'Nozzle camera image is dim',
     'The centering camera image is too dark to read. Cleaning the lens did not help.',
     'low', 'closed', 0, 0, '2025-11-07T13:20:00Z', '2025-11-08T09:20:00Z'),
    ((SELECT id FROM equipment WHERE code = 'WR-01'),
     (SELECT id FROM technicians WHERE badge = 'T-1057'),
     'Wire feed stutters on long seams',
     'Seams longer than 300 mm show porosity near the end. The feed motor sounds uneven.',
     'high', 'open', 40, 0, '2025-11-11T06:55:00Z', NULL),
    ((SELECT id FROM equipment WHERE code = 'PB-02'),
     (SELECT id FROM technicians WHERE badge = 'T-1062'),
     'Foot pedal cover cracked',
     'The pedal still works. The cover has a crack along the hinge and could pinch a boot lace.',
     'low', 'open', 0, 0, '2025-11-11T10:30:00Z', NULL),
    ((SELECT id FROM equipment WHERE code = 'OV-01'),
     (SELECT id FROM technicians WHERE badge = 'T-1041'),
     'Exhaust fan belt squeal',
     'Belt squeals for the first ten minutes after start. Tension looks low.',
     'medium', 'closed', 15, 1, '2025-11-06T11:05:00Z', '2025-11-06T14:35:00Z');

INSERT INTO work_notes (issue_id, technician_id, note, minutes_spent, created_at) VALUES
    ((SELECT id FROM issues WHERE title = 'Nozzle camera image is dim'),
     (SELECT id FROM technicians WHERE badge = 'T-1041'),
     'Replaced the camera ring light. Image is clear.', 45, '2025-11-08T09:15:00Z'),
    ((SELECT id FROM issues WHERE title = 'Exhaust fan belt squeal'),
     (SELECT id FROM technicians WHERE badge = 'T-1057'),
     'Locked out, re-tensioned the belt to spec, tested for fifteen minutes.', 50, '2025-11-06T14:30:00Z'),
    ((SELECT id FROM issues WHERE title = 'Zone 2 heater slow to reach setpoint'),
     (SELECT id FROM technicians WHERE badge = 'T-1057'),
     'Zone 2 thermocouple reads 12 C low against a reference probe. Replacement ordered.', 30, '2025-11-10T10:00:00Z'),
    ((SELECT id FROM issues WHERE title = 'Guard interlock trips with the guard closed'),
     (SELECT id FROM technicians WHERE badge = 'T-1062'),
     'Interlock switch actuator is loose. Waiting on the supervisor before any adjustment.', 20, '2025-11-10T09:40:00Z'),
    ((SELECT id FROM issues WHERE title = 'Guard interlock trips with the guard closed'),
     (SELECT id FROM technicians WHERE badge = 'S-2003'),
     'Reviewed with the technician. Replace the switch, do not adjust it.', 15, '2025-11-10T10:10:00Z');
