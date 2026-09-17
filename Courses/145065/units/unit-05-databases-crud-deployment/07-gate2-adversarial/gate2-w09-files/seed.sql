-- seed.sql · invented starting data. Riverside Fabrication is a composite.
-- Entries 6 and 7 belong to Line 4. The Line 3 app must never show them.

INSERT INTO parts (number, name) VALUES
    ('BRK-220', 'Mounting bracket, 3 mm'),
    ('PNL-114', 'Side panel, powder coated'),
    ('GRD-031', 'Perforated guard'),
    ('HNG-008', 'Hinge plate');

INSERT INTO scrap_entries (part_id, line, shift, quantity, reason, rework_minutes, logged_at) VALUES
    (1, 3, 'first',  12, 'Bend angle out of tolerance after die change', 45, '2025-11-10T07:40:00Z'),
    (2, 3, 'second',  3, 'Coating orange peel, operator''s call to strip', 75, '2025-11-10T16:05:00Z'),
    (1, 3, 'first',   5, 'Hole position off, wrong program loaded',     30, '2025-11-11T08:15:00Z'),
    (3, 3, 'second',  2, 'Weld spatter on the guard face',              20, '2025-11-11T18:30:00Z'),
    (2, 3, 'first',   1, 'Dent from a forklift tine',                    0, '2025-11-12T09:50:00Z'),
    (4, 4, 'first',  40, 'Line 4 trial run, customer sample rejected',   90, '2025-11-12T10:10:00Z'),
    (3, 4, 'second',  8, 'Line 4 laser dross on cut edge',              15, '2025-11-12T19:25:00Z');
