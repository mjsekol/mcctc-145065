# errors.py
# STARTER FILE for Lab U03-01. The Line 3 error family goes here.
#
# Riverside Fabrication is a composite shop invented for this course.
#
#     PlantError                              catch this to catch all of them
#     |-- ConfigurationError (also ValueError)   a value the model refuses
#     `-- EquipmentError                         stores asset_tag
#         |-- LockoutError                       locked out, or the wrong badge
#         |-- EquipmentStateError                wrong state: guard open, not running
#         `-- UnknownEquipmentError             no such tag on this line
#
# Step 1 writes these six classes. Nothing imports this file until Step 3.
